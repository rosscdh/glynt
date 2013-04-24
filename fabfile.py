from __future__ import with_statement
from fabric.api import *
from fabric.contrib.console import confirm
from fabric.contrib import files

import os
import json
import getpass
import datetime
import time
import requests
from termcolor import colored
from pprint import pprint

debug = True

env.local_project_path = os.path.dirname(os.path.realpath(__file__))
env.SHA1_FILENAME = None
env.timestamp = time.time()
env.is_predeploy = False
env.local_user = getpass.getuser()


@task
def filestore_prod():
    env.environment = 'production'
    env.environment_class = 'filesystem'
    env.local_project_path = os.path.dirname(os.path.realpath(__file__))
    env.remote_project_path = None
    env.deploy_archive_path = None
    env.virtualenv_path = None

    env.newrelic_api_token = None
    env.newrelic_app_name = None
    env.newrelic_application_id = None

    # change from the default user to 'vagrant'
    env.user = 'ubuntu'
    env.application_user = None
    # connect to the port-forwarded ssh
    env.hosts = ['ec2-54-241-224-100.us-west-1.compute.amazonaws.com']
    env.key_filename = '%s/../lawpal-chef/chef-machines.pem' % env.local_project_path

    env.start_service = None
    env.stop_service = None
    env.light_restart = None


@task
def production():
    env.project = 'glynt'
    env.environment = 'production'
    env.environment_class = 'production'
    env.local_project_path = os.path.dirname(os.path.realpath(__file__))
    env.remote_project_path = '/var/apps/lawpal/'
    env.deploy_archive_path = '/var/apps/'
    env.virtualenv_path = '/var/apps/.lawpal-live-venv/'

    env.newrelic_api_token = 'ec2a185854e15d572186b246961e0ed11378cc249d0a0cd'
    env.newrelic_app_name = 'Lawpal'
    env.newrelic_application_id = '1858111'

    # change from the default user to 'vagrant'
    env.user = 'ubuntu'
    env.application_user = 'app'
    # connect to the port-forwarded ssh
    env.hosts = ['ec2-204-236-152-5.us-west-1.compute.amazonaws.com', 'ec2-184-72-21-48.us-west-1.compute.amazonaws.com', 'ec2-54-241-224-100.us-west-1.compute.amazonaws.com']
    env.key_filename = '%s/../lawpal-chef/chef-machines.pem' % env.local_project_path

    env.start_service = 'supervisorctl start uwsgi'
    env.stop_service = 'supervisorctl stop uwsgi'
    env.light_restart = "kill -HUP `cat /tmp/lawpal.pid`"

@task
def preview():
    env.project = 'glynt'
    env.environment = 'preview'
    env.environment_class = 'production'
    env.local_project_path = os.path.dirname(os.path.realpath(__file__))
    env.remote_project_path = '/var/apps/preview-lawpal/'
    env.deploy_archive_path = '/var/apps/'
    env.virtualenv_path = '/var/apps/.lawpal-preview-venv/'

    env.newrelic_api_token = 'ec2a185854e15d572186b246961e0ed11378cc249d0a0cd'
    env.newrelic_app_name = 'Lawpal'
    env.newrelic_application_id = '1858111'

    # change from the default user to 'vagrant'
    env.user = 'ubuntu'
    env.application_user = 'app'
    # connect to the port-forwarded ssh
    env.hosts = ['ec2-204-236-152-5.us-west-1.compute.amazonaws.com', 'ec2-184-72-21-48.us-west-1.compute.amazonaws.com', 'ec2-54-241-224-100.us-west-1.compute.amazonaws.com']
    env.key_filename = '%s/../lawpal-chef/chef-machines.pem' % env.local_project_path

    env.start_service = 'supervisorctl start uwsgi'
    env.stop_service = 'supervisorctl stop uwsgi'
    env.light_restart = "kill -HUP `cat /tmp/lawpal.pid`"

@task
def staging():
    env.project = 'glynt'
    env.environment = 'staging'
    env.environment_class = 'webfaction'
    env.local_project_path = os.path.dirname(os.path.realpath(__file__))
    env.remote_project_path = '/home/stard0g101/webapps/glynt/'
    env.deploy_archive_path = '~/'
    env.virtualenv_path = '/home/stard0g101/.virtualenvs/glynt/'

    env.newrelic_api_token = 'a7b966785ff101a80eb02bf2a92a3fa6400b284139f964f'
    env.newrelic_app_name = 'Lawpal'
    env.newrelic_application_id = '2058809'

    # change from the default user to 'vagrant'
    env.user = 'stard0g101'
    env.application_user = 'stard0g101'

    # connect to the port-forwarded ssh
    env.hosts = ['stard0g101.webfactional.com']
    env.key_filename = None

    env.start_service = '%sapache2/bin/start' % env.remote_project_path
    env.stop_service = '%sapache2/bin/stop' % env.remote_project_path
    env.light_restart = None


@task
def virtualenv(cmd):
  # change to base dir
  with cd(env.remote_project_path):
    # activate the virtualenv, run scripts as app user
    if env.environment_class is 'webfaction':
        # webfaction
        run("source %sbin/activate && %s" % (env.virtualenv_path, cmd,))
    else:
        sudo("source %sbin/activate && %s" % (env.virtualenv_path, cmd,), user=env.application_user)


def cli(cmd, as_who='user'):
    sudo(cmd) if as_who == 'sudo' and env.environment_class is not 'webfaction' else run(cmd)

@task
def clean_pyc():
    virtualenv('python %s%s/manage.py clean_pyc' % (env.remote_project_path, env.project))


def get_sha1():
  cd(env.local_project_path)
  return local('git rev-parse --short --verify HEAD', capture=True)

@task
def git_export(branch='master'):
  env.SHA1_FILENAME = get_sha1()
  if not os.path.exists('/tmp/%s.zip' % env.SHA1_FILENAME):
      local('git archive --format zip --output /tmp/%s.zip --prefix=%s/ %s' % (env.SHA1_FILENAME, env.SHA1_FILENAME, branch,), capture=False)

@task
def prepare_deploy():
    git_export()

@task
def migrations():
    virtualenv('python %s/%s/manage.py migrate' % (env.remote_project_path, env.project))

@task
def syncdb():
    virtualenv('python %s/%s/manage.py syncdb' % (env.remote_project_path, env.project))

@task
def clean_versions():
    current_version = get_sha1()
    versions_path = '%sversions' % env.remote_project_path
    sudo('find %s/* ! -iname %s -print0 | xargs -0 rm -rf' % (versions_path ,current_version,))

@task
def supervisord_restart():
    if env.environment_class is 'webfaction':
        execute(restart_service)
    else:
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

@task
def filesystem_chores():
    sudo('aptitude --assume-yes update')
    sudo('aptitude --assume-yes install build-essential python-setuptools python-dev easy_install nmap htop vim')
    sudo('aptitude --assume-yes install nfs-kernel-server')

@task
def nfs_reload():
    sudo('service nfs-kernel-server reload')

def env_run(cmd):
    return sudo(cmd) if env.environment_class is 'production' else run(cmd)

@task
def deploy_archive_file():
    filename = env.get('SHA1_FILENAME', None)
    if filename is None:
        filename = env.SHA1_FILENAME = get_sha1()
    file_name = '%s.zip' % filename
    if not files.exists('%s/%s' % (env.deploy_archive_path, file_name)):
        as_sudo = env.environment_class is 'production'
        put('/tmp/%s' % file_name, env.deploy_archive_path, use_sudo=as_sudo)


def clean_zip():
    file_name = '%s.zip' % env.SHA1_FILENAME
    if files.exists('%s%s' % (env.deploy_archive_path, file_name)):
        env_run('rm %s%s' % (env.deploy_archive_path, file_name,))

@task
def relink():
    if not env.SHA1_FILENAME:
        env.SHA1_FILENAME = get_sha1()

    version_path = '%sversions' % env.remote_project_path
    full_version_path = '%s/%s' % (version_path, env.SHA1_FILENAME)
    project_path = '%s%s' % (env.remote_project_path, env.project,)

    if not env.is_predeploy:
        if files.exists('%s/%s' % (version_path, env.SHA1_FILENAME)): # check the sha1 dir exists
            #if files.exists(project_path, use_sudo=True): # unlink the glynt dir
            virtualenv('unlink %s' % project_path)
            virtualenv('ln -s %s/%s %s' % (version_path, env.SHA1_FILENAME, project_path,)) # relink


def do_deploy():
    if env.SHA1_FILENAME is None:
        raise Exception('Must have a SHA1_FILENAME defined. Ensure you have run @git_export')

    version_path = '%sversions' % env.remote_project_path
    full_version_path = '%s/%s' % (version_path, env.SHA1_FILENAME)
    project_path = '%s%s' % (env.remote_project_path, env.project,)

    if env.environment == 'production':
        if not files.exists(version_path):
            env_run('mkdir -p %s' % version_path )
        env_run('chown -R %s:%s %s' % (env.application_user, env.application_user, env.remote_project_path) )

    deploy_archive_file()

    # extract project zip file:into a staging area and link it in
    if not files.exists('%s/manage.py'%full_version_path):
        unzip_archive()

    execute(relink)

    if not env.is_predeploy:
        # copy the live local_settings
        with cd(project_path):
            virtualenv('cp %s/conf/%s.local_settings.py %s/%s/local_settings.py' % (project_path, env.environment, project_path, env.project))
            virtualenv('cp %s/conf/%s.wsgi.py %s/%s/wsgi.py' % (project_path, env.environment, project_path, env.project))
            virtualenv('cp %s/conf/%s.newrelic.ini %s/%s/newrelic.ini' % (project_path, env.environment, project_path, env.project))

@task
def unzip_archive():
    version_path = '%sversions' % env.remote_project_path
    with cd('%s' % version_path):
        virtualenv('unzip %s%s.zip -d %s' % (env.deploy_archive_path, env.SHA1_FILENAME, version_path,))
@task
def restart_lite():
    sudo(env.light_restart)

@task
def restart_service():
    execute(stop_service)
    execute(start_service)

@task
def start_service():
    env_run(env.start_service)

@task
def stop_service():
    env_run(env.stop_service)

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

    virtualenv('pip install -r %s' % requirements_path )

@task
def newrelic_note():
    if not hasattr(env, 'deploy_desc'):
        env.deploy_desc = prompt(colored('Hi %s, Please provide a Deployment Note:' % env.local_user, 'yellow'))

@task
def newrelic_deploynote():
    description = '[env:%s][%s@%s] %s' % (env.environment, env.user, env.host, env.deploy_desc)
    headers = {
        'x-api-key': env.newrelic_api_token
    }

    payload = {
        #'deployment[app_name]': env.newrelic_app_name, # new relc wants either app_name or application_id not both
        'deployment[application_id]': env.newrelic_application_id,
        'deployment[description]': description,
        'deployment[user]': env.local_user,
        'deployment[revision]': get_sha1()
    }
    
    colored('Sending Deployment Message to NewRelic', 'blue')

    r = requests.post('https://rpm.newrelic.com/deployments.xml', data=payload, headers=headers, verify=False)

    is_ok = r.status_code in [200,201]
    text = 'DeploymentNote Recorded OK' if is_ok is True else 'DeploymentNote Recorded Not OK: %s' % r.text
    color = 'green' if is_ok else 'red'

    print colored('%s (%s)' % (text, r.status_code), color)


@task
def deploy(is_predeploy='False'):
    """
    :is_predeploy=True - will deploy the latest MASTER SHA but not link it in: this allows for assets collection
    and requirements update etc...
    """

    env.is_predeploy = True if is_predeploy.lower() in ['true','t','y','yes','1',1] else False

    execute(newrelic_note)
    prepare_deploy()
    execute(do_deploy)
    execute(clean_pyc)

    if env.environment_class == 'webfaction':
        execute(restart_service)
    else:
        execute(supervisord_restart)
    execute(clean_zip)
    execute(newrelic_deploynote)
