from __future__ import with_statement
import os
from fabric.api import *
from fabric.contrib.console import confirm
from fabric.contrib import files

import datetime
import time

debug = True

env.SHA1_FILENAME = None

env.timestamp = time.time()


@task
def production():
    env.project = 'glynt'
    env.environment = 'production'
    env.local_project_path = os.path.dirname(os.path.realpath(__file__))
    env.remote_project_path = '/var/apps/lawpal/'
    env.deploy_archive_path = '/var/apps/'

    # change from the default user to 'vagrant'
    env.user = 'ubuntu'
    env.application_user = 'app'
    # connect to the port-forwarded ssh
    env.hosts = ['ec2-204-236-152-5.us-west-1.compute.amazonaws.com', 'ec2-184-72-21-48.us-west-1.compute.amazonaws.com']
    env.key_filename = '%s/../lawpal-chef/chef-machines.pem' % env.local_project_path

    env.start_service = 'supervisorctl start uwsgi'
    env.stop_service = 'supervisorctl stop uwsgi'
    #env.stop_service = "kill -HUP `cat /tmp/lawpal.pid`"

@task
def staging():
    env.project = 'glynt'
    env.environment = 'staging'
    env.local_project_path = os.path.dirname(os.path.realpath(__file__))
    env.remote_project_path = '/home/stard0g101/webapps/glynt/'
    env.deploy_archive_path = '~/'

    # change from the default user to 'vagrant'
    env.user = 'stard0g101'
    env.application_user = 'stard0g101'

    # connect to the port-forwarded ssh
    env.hosts = ['stard0g101.webfactional.com']
    env.key_filename = None

    env.start_service = '%sapache2/bin/start' % env.remote_project_path
    env.stop_service = '%sapache2/bin/stop' % env.remote_project_path


def virtualenv(cmd):
  # change to base dir
  with cd("/var/apps/lawpal"):
    # activate the virtualenv, run scripts as app user
    sudo("source /var/apps/.bashrc && %s" % cmd, user=env.application_user)


def git_export():
  cd(env.local_project_path)
  env.SHA1_FILENAME = local('git rev-parse --short --verify HEAD', capture=True)
  if not files.exists('/tmp/%s.zip' % env.SHA1_FILENAME):
      local('git archive --format zip --output /tmp/%s.zip --prefix=%s/ master' % (env.SHA1_FILENAME, env.SHA1_FILENAME,), capture=False)


def prepare_deploy():
    git_export()


@task
def supervisord_restart():
    sudo('supervisorctl restart uwsgi')

@task
def chores():
    sudo('aptitude --assume-yes install build-essential python-setuptools python-dev uwsgi-plugin-python libjpeg8 libjpeg62-dev libfreetype6 libfreetype6-dev easy_install nmap htop vim')
    sudo('aptitude --assume-yes install git-core mercurial subversion')
    sudo('aptitude --assume-yes install libtidy-dev python-psycopg2')
    #sudo('aptitude --assume-yes install rabbitmq-server')

    sudo('easy_install pip')
    sudo('pip install virtualenv virtualenvwrapper pillow')

    put('conf/.bash_profile', '~/.bash_profile')


def deploy_archive_file():
    file_name = '%s.zip' % env.SHA1_FILENAME
    if not files.exists('%s/%s' % (env.deploy_archive_path, file_name)):
        put('/tmp/%s' % file_name, env.deploy_archive_path, use_sudo=True)


def conclude_deploy():
    file_name = '%s.zip' % env.SHA1_FILENAME
    if files.exists('%s%s' % (env.deploy_archive_path, file_name)):
        sudo('rm %s%s' % (env.deploy_archive_path, file_name,))


def do_deploy():
    if env.SHA1_FILENAME is None:
        raise Exception('Must have a SHA1_FILENAME defined. Ensure you have run @git_export')

    version_path = '%sversions' % env.remote_project_path
    full_version_path = '%s/%s' % (version_path, env.SHA1_FILENAME)

    project_path = '%s%s' % (env.remote_project_path, env.project,)

    if env.environment == 'production':
        if not files.exists(version_path, use_sudo=True):
            sudo('mkdir -p %s' % version_path )
        sudo('chown -R %s:%s %s' % (env.application_user, env.application_user, env.remote_project_path) )

    deploy_archive_file()


    # extract project zip file:into a staging area and link it in
    if not files.exists(full_version_path, use_sudo=True):
        with cd('%s' % version_path):
            virtualenv('unzip %s%s.zip -d %s' % (env.deploy_archive_path, env.SHA1_FILENAME, version_path,))

    if not env.is_predeploy:
        if files.exists(project_path, use_sudo=True):
            virtualenv('unlink %s' % project_path)
        virtualenv('ln -s %s/%s %s' % (version_path, env.SHA1_FILENAME, project_path,))

    if not env.is_predeploy:
        # copy the live local_settings
        with cd(project_path):
            virtualenv('cp %s/conf/%s.local_settings.py %s/%s/local_settings.py' % (project_path, env.environment, project_path, env.project))
            virtualenv('cp %s/conf/%s.wsgi.py %s/%s/wsgi.py' % (project_path, env.environment, project_path, env.project))
            virtualenv('cp %s/conf/%s.newrelic.ini %s/%s/newrelic.ini' % (project_path, env.environment, project_path, env.project))


@task
def restart_service():
    execute(stop_service)
    execute(start_service)

@task
def start_service():
    run(env.start_service)

@task
def stop_service():
    run(env.stop_service)

@task
def fixtures():
    # Activate virtualenv
    virtualenv('python %s/%s/manage.py loaddata sites document_category documenttemplate legal lawyers' % (env.remote_project_path, env.project,))


@task
def assets():
    # Activate virtualenv
    virtualenv('python %s%s/manage.py collectstatic --noinput' % (env.remote_project_path, env.project,))
    virtualenv('python %s%s/manage.py compress --force' % (env.remote_project_path, env.project,))

@task
def requirements():
    project_path = '%s%s' % (env.remote_project_path, env.project, )
    requirements_path = '%s/requirements.txt' % (project_path, )

    virtualenv('pip install -r %s' %(requirements_path,) )

    if env.environment == 'production':
        virtualenv('pip install psycopg2')


@task
def deploy(is_predeploy='False'):
    """
    :is_predeploy=True - will deploy the latest MASTER SHA but not link it in: this allows for assets collection
    and requirements update etc...
    """

    env.is_predeploy = True if is_predeploy.lower() in ['true','t','y','yes','1',1] else False

    prepare_deploy()
    execute(do_deploy)
    execute(restart_service)
    execute(conclude_deploy)