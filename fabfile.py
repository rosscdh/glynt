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
    env.deploy_archive_path = '~/'

    # change from the default user to 'vagrant'
    env.user = 'ubuntu'
    # connect to the port-forwarded ssh
    env.hosts = ['ec2-204-236-152-5.us-west-1.compute.amazonaws.com', 'ec2-184-72-21-48.us-west-1.compute.amazonaws.com']
    env.key_filename = '/Users/rossc/Projects/lawpal/lawpal-chef/chef-machines.pem'

    env.start_service = 'uwsgi --http :9090 --module main --callable app -H ~/.virtualenvs/%s/' % env.project
    env.stop_service = "kill -HUP `cat /tmp/lawpal.pid`"

@task
def stage():
    env.project = 'glynt'
    env.environment = 'stage'
    env.local_project_path = os.path.dirname(os.path.realpath(__file__))
    env.remote_project_path = '/home/stard0g101/webapps/%s' % env.project
    env.deploy_archive_path = '~/'

    # change from the default user to 'vagrant'
    env.user = 'stard0g101'
    # connect to the port-forwarded ssh
    env.hosts = ['stard0g101.webfactional.com']
    env.key_filename = None

    env.start_service = None
    env.stop_service = None

def git_export():
  cd(env.local_project_path)
  env.SHA1_FILENAME = local('git rev-parse --short --verify HEAD', capture=True)
  local('git archive --format zip --output /tmp/%s.zip --prefix=%s/ master' % (env.SHA1_FILENAME, env.SHA1_FILENAME,), capture=False)


def prepare_deploy():
    git_export()


@task
def chores():
    sudo('aptitude --assume-yes install build-essential python-setuptools python-dev uwsgi-plugin-python libjpeg8 libjpeg62-dev libfreetype6 libfreetype6-dev easy_install nmap htop vim')
    sudo('aptitude --assume-yes install git-core mercurial subversion')
    sudo('aptitude --assume-yes install rabbitmq-server')

    sudo('easy_install pip')
    sudo('pip install virtualenv virtualenvwrapper pillow')

    put('conf/.bash_profile', '~/.bash_profile')

@task
def virtualenv():
    if not files.exists('~/.virtualenvs'):
        with shell_env(WORKON_HOME='~/.virtualenvs'):
            run('export WORKON_HOME=~/.virtualenvs')
            run('mkdir -p $WORKON_HOME')

    if not files.exists('~/.virtualenvs/%s' % env.project):
        with shell_env(WORKON_HOME='~/.virtualenvs'):
            run('export WORKON_HOME=~/.virtualenvs')
            run('mkvirtualenv %s' % env.project)

def deploy_archive_file():
    put('/tmp/%s.zip'%(env.SHA1_FILENAME,), env.deploy_archive_path)

def conclude_deploy():
    run('unlink %s%s.zip' % (env.deploy_archive_path, env.SHA1_FILENAME,))


def do_deploy():
    if env.SHA1_FILENAME is None:
        raise Exception('Must have a SHA1_FILENAME defined. Ensure you have run @git_export')

    version_path = '%sversions' % env.remote_project_path
    project_path = '%s%s' % (env.remote_project_path, env.project,)

    if not files.exists(version_path):
        sudo('mkdir -p %s' % version_path )
    sudo('chown -R %s:%s %s' % (env.user,env.user, version_path) )

    deploy_archive_file()

    # extract project zip file:into a staging area and link it in
    with cd('%s' % version_path):
        run('unzip %s%s.zip' % (env.deploy_archive_path, env.SHA1_FILENAME,))

    with cd('%s' % env.remote_project_path):
        if files.exists(project_path):
            run('unlink %s' % project_path)

        run('ln -s %s/%s %s'%(version_path, env.SHA1_FILENAME, project_path,))

    # copy the live local_settings
    with cd(project_path):
        run('cp conf/%s.local_settings.py %s/local_settings.py' % (env.environment, env.project,))
        run('cp conf/%s.wsgi.py %s/wsgi.py' % (env.environment, env.project,))
        run('cp conf/%s.newrelic.ini newrelic.ini' % (env.environment,))

    execute(restart_service)


@task
def restart_service():
    execute(stop_service)
    execute(start_service)

@task
def start_service():
    run(env.start_service)

@task
def stop_service():
    run(env.start_service)

@task
def do_fixtures():
    # Activate virtualenv
    with prefix('workon %s' % (env.project_name,)):
        run('python %s/%s/manage.py loaddata sites document_category documenttemplate public/fixtures/cms.json' % (env.remote_project_path, PROJECT,))

@task
def fixtures():
    for app_name, project_name, remote_project_path in env.remote_project_path:
        env.app_name = app_name
        env.project_name = project_name
        env.remote_project_path = remote_project_path
        execute(do_fixtures, hosts=env.hosts)

@task
def assets():
    # Activate virtualenv
    with prefix('workon %s' % (env.project,)):
        run('python %s/%s/manage.py collectstatic --noinput' % (env.remote_project_path, PROJECT,))
        run('python %s/%s/manage.py compress --force' % (env.remote_project_path, PROJECT,))

@task
def requirements():
    project_path = '%s%s' % (env.remote_project_path, env.project, )
    requirements_path = '%s/requirements.txt' % (project_path, )

    with prefix('workon %s' % (env.project,)):
        run('pip install -r %s' %(requirements_path,) )
        if env.environment == 'production':
            run('pip install psycopg2')


@task
def deploy():
    prepare_deploy()
    execute(do_deploy)
    execute(conclude_deploy)