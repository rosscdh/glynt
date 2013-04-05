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
    #env.hosts = ['ec2-204-236-152-5.us-west-1.compute.amazonaws.com', 'ec2-184-72-21-48.us-west-1.compute.amazonaws.com']
    env.hosts = ['ec2-184-72-21-48.us-west-1.compute.amazonaws.com']
    env.key_filename = '/Users/rossc/Projects/lawpal/lawpal-chef/chef-machines.pem'

    env.restart_service = "kill -HUP `cat /tmp/lawpal.pid`"

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


def git_export():
  cd(env.local_project_path)
  env.SHA1_FILENAME = local('git rev-parse --short --verify HEAD', capture=True)
  local('git archive --format zip --output /tmp/%s.zip --prefix=%s/ master' % (env.SHA1_FILENAME, env.SHA1_FILENAME,), capture=False)


def prepare_deploy():
    git_export()


@task
def chores():
    sudo('aptitude install unzip')

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
    with cd('%s' % env.remote_project_path):
        run('unzip %s%s.zip' % (env.deploy_archive_path, env.SHA1_FILENAME,))

        run('unlink %s'%(project_path,))

        run('ln -s %s/%s %s'%(version_path, env.SHA1_FILENAME, project_path,))

    # copy the live local_settings
    with cd(project_path):
        print project_path
        # run('cp conf/%s.local_settings.py %s/%s/%s/local_settings.py' % (environment, project_path, env.project, app_name,))
        # run('cp conf/%s.newrelic.ini %s/newrelic.ini' % (environment, project_path,))
        # run('cp conf/%s.wsgi.py %s/%s/wsgi.py' % (environment, project_path, env.project, app_name,))

    run(env.restart_service)


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
def do_assets():
    # Activate virtualenv
    with prefix('workon %s' % (env.project_name,)):
        run('python %s/%s/manage.py collectstatic --noinput' % (env.remote_project_path, PROJECT,))
        run('python %s/%s/manage.py compress --force' % (env.remote_project_path, PROJECT,))

@task
def assets():
    for app_name, project_name, remote_project_path in env.remote_project_path:
        env.app_name = app_name
        env.project_name = project_name
        env.remote_project_path = remote_project_path
        execute(do_assets, hosts=env.hosts)

@task
def do_requirements():
    project_path = '%s/%s' % (env.remote_project_path, env.project_name, )
    requirements_path = '%s/requirements.txt' % (project_path, )

    with prefix('workon %s' % (env.project_name,)):
        if files.exists(requirements_path):
            run('pip install -r %s' %(requirements_path,) )
        else:
            raise Exception('requirements.exe does not exist at: %s' %(requirements_path,) )

@task
def requirements(deploy_to_env='staging'):
    for app_name, project_name, remote_project_path in env.remote_project_path:
        env.app_name = app_name
        env.project_name = project_name
        env.remote_project_path = remote_project_path
        execute(do_requirements, hosts=env.hosts)

@task
def deploy():
    prepare_deploy()
    execute(do_deploy)
    execute(conclude_deploy)