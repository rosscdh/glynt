from __future__ import with_statement
from fabric.api import *
from fabric.contrib.console import confirm
from fabric.context_managers import settings
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
def prod_db():
    env.project = 'glynt'
    env.environment = 'production'
    env.environment_class = 'db'

    env.remote_project_path = None
    env.deploy_archive_path = None
    env.virtualenv_path = None

    env.newrelic_api_token = None
    env.newrelic_app_name = None
    env.newrelic_application_id = None

    # change from the default user to 'vagrant'
    env.user = 'ubuntu'
    env.application_user = 'app'
    # connect to the port-forwarded ssh
    env.hosts = ['ec2-50-18-97-221.us-west-1.compute.amazonaws.com'] if not env.hosts else env.hosts
    env.key_filename = '%s/../lawpal-chef/chef-machines.pem' % env.local_project_path

    env.start_service = None
    env.stop_service = None
    env.light_restart = None

@task
def production():
    env.project = 'glynt'
    env.environment = 'production'
    env.environment_class = 'production'

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
    env.hosts = ['ec2-204-236-152-5.us-west-1.compute.amazonaws.com', 'ec2-184-72-21-48.us-west-1.compute.amazonaws.com', 'ec2-54-241-224-100.us-west-1.compute.amazonaws.com'] if not env.hosts else env.hosts
    env.db_host = env.hosts[0]

    env.key_filename = '%s/../lawpal-chef/chef-machines.pem' % env.local_project_path

    env.start_service = 'supervisorctl start uwsgi'
    env.stop_service = 'supervisorctl stop uwsgi'
    env.light_restart = "kill -HUP `cat /tmp/lawpal.pid`"

@task
def preview():
    env.project = 'glynt'
    env.environment = 'preview'
    env.environment_class = 'production'

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
    env.hosts = ['ec2-204-236-152-5.us-west-1.compute.amazonaws.com', 'ec2-184-72-21-48.us-west-1.compute.amazonaws.com', 'ec2-54-241-224-100.us-west-1.compute.amazonaws.com'] if not env.hosts else env.hosts
    env.db_host = env.hosts[0]

    env.key_filename = '%s/../lawpal-chef/chef-machines.pem' % env.local_project_path

    env.start_service = 'supervisorctl start uwsgi'
    env.stop_service = 'supervisorctl stop uwsgi'
    env.light_restart = "kill -HUP `cat /tmp/preview-lawpal.pid`"

@task
def staging():
    env.project = 'glynt'
    env.environment = 'staging'
    env.environment_class = 'webfaction'

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
    env.db_host = env.hosts[0]

    env.key_filename = None

    env.start_service = '%sapache2/bin/start' % env.remote_project_path
    env.stop_service = '%sapache2/bin/stop' % env.remote_project_path
    env.light_restart = None

@task
def virtualenv(cmd, **kwargs):
  # change to base dir
  #with cd(env.remote_project_path):
    if env.environment_class is 'webfaction':
        # webfaction
        run("source %sbin/activate && %s" % (env.virtualenv_path, cmd,), **kwargs)
    else:
        sudo("source %sbin/activate && %s" % (env.virtualenv_path, cmd,), user=env.application_user, **kwargs)

@task
def pip_install():
    virtualenv('pip install simplejson==3.2.0 --upgrade')

@task
def clear_cache():
    virtualenv(cmd='python %s%s/manage.py clear_cache' % (env.remote_project_path, env.project))

@task
def clean_pyc():
    virtualenv('python %s%s/manage.py clean_pyc' % (env.remote_project_path, env.project))

@task
def manage(cmd='validate'):
    virtualenv('python %s%s/manage.py %s' % (env.remote_project_path, env.project, cmd))

def get_sha1():
  cd(env.local_project_path)
  return local('git rev-parse --short --verify HEAD', capture=True)

@task
def db_backup(db='lawpal_prelaunch'):
    db_backup_name = '%s.bak' % db
    sudo('pg_dump --no-owner --no-acl -Fc %s > /tmp/%s' % (db, db_backup_name,), user='postgres')
    local('scp -i %s %s@%s:/tmp/%s /tmp/' % (env.key_filename, env.user, env.host, db_backup_name,))

@task
def db_local_restore(db='lawpal_prelaunch'):
    with settings(warn_only=True): # only warning as we will often have errors importing
        db_backup_name = '%s.bak' % db
        local('echo "DROP DATABASE %s;" | psql -h localhost -U %s' % (db, env.local_user,))
        local('echo "CREATE DATABASE %s WITH OWNER %s ENCODING \'UTF8\';" | psql -h localhost -U %s' % (db, env.local_user, env.local_user,))
        local('pg_restore -U %s -h localhost -d %s -Fc /tmp/%s' % (env.local_user, db, db_backup_name,))

@task
def git_export(branch='master'):
  env.SHA1_FILENAME = get_sha1()
  if not os.path.exists('/tmp/%s.zip' % env.SHA1_FILENAME):
      local('git archive --format zip --output /tmp/%s.zip --prefix=%s/ %s' % (env.SHA1_FILENAME, env.SHA1_FILENAME, branch,), capture=False)

@task
def celery_restart():
    execute(celery_stop)
    execute(celery_start)

@task
def celery_start(loglevel='info'):
    pid_path = "%sceleryd.pid" % env.remote_project_path
    with settings(warn_only=True): # only warning as we will often have errors importing
        if files.exists(pid_path):
            execute(celery_stop)
        virtualenv('python %s%s/manage.py celeryd_detach worker --loglevel=%s --pidfile=%s' % (env.remote_project_path, env.project, loglevel, pid_path,), warn_only=True)

@task
def celery_stop():
    with settings(warn_only=True): # only warning as we will often have errors importing
        pid_path = "%sceleryd.pid" % env.remote_project_path
        sudo("cat %s | xargs kill -9" % pid_path, user=env.application_user, warn_only=True, shell=False)
        # if files.exists(pid_path):
        #     sudo("rm %s" % pid_path , shell=False, warn_only=True)

@task
def prepare_deploy():
    git_export()

@task
def update_index():
    with settings(host_string=env.db_host):
        #for i in ['default lawyer', 'firms firm']:
        for i in ['default lawyer',]:
            virtualenv('python %s%s/manage.py update_index -a 100000 -u %s' % (env.remote_project_path, env.project, i))

@task
def rebuild_index():
    with settings(host_string=env.db_host):
        #for i in ['default lawyer', 'firms firm']:
        for i in ['default lawyer',]:
            virtualenv('python %s%s/manage.py rebuild_index --noinput' % (env.remote_project_path, env.project,))

@task
def migrate():
    with settings(host_string=env.db_host):
        virtualenv('python %s%s/manage.py migrate' % (env.remote_project_path, env.project))

@task
def syncdb():
    with settings(host_string=env.db_host):
        virtualenv('python %s%s/manage.py syncdb' % (env.remote_project_path, env.project))

@task
def clean_versions():
    current_version = get_sha1()
    versions_path = '%sversions' % env.remote_project_path
    cmd = 'ls %s/* | grep -v %s | xargs rm -Rf' % (versions_path ,current_version,)
    if env.environment_class is 'webfaction':
        run(cmd)
    else:
        sudo(cmd)

# ------ RESTARTERS ------#
@task
def supervisord_restart():
    with settings(warn_only=True):
        if env.environment_class is 'webfaction':
            execute(restart_service)
        else:
            sudo('supervisorctl restart uwsgi')

@task
def restart_lite():
    with settings(warn_only=True):
        sudo(env.light_restart)

@task
def restart_service(heavy_handed=False):
    with settings(warn_only=True):
        if env.environment_class not in ['celery']: # dont restart celery nginx services
            if env.environment_class == 'webfaction':
                execute(stop_service)
                execute(start_service)
            else:
                if not heavy_handed:
                    execute(restart_lite)
                else:
                    execute(supervisord_restart)

# ------ END-RESTARTERS ------#

# ------ SOURCE-VALIDATION ------#
@task
def mispelling():
    words = ['of council', 'teh']
    output = []
    for w in words:
        grp = local('cd %s;git grep "%s"' % (env.local_project_path, w,), capture=True)
        output.append(grp)
    print output

# ------ END-SOURCE-VALIDATION ------#
@task
def chores():
    sudo('aptitude --assume-yes install build-essential python-setuptools python-dev apache2-utils uwsgi-plugin-python libjpeg8 libjpeg62-dev libfreetype6 libfreetype6-dev easy_install nmap htop vim unzip')
    sudo('aptitude --assume-yes install git-core mercurial subversion')
    sudo('aptitude --assume-yes install libtidy-dev postgresql-client libpq-dev python-psycopg2')

    # GEO
    sudo('aptitude --assume-yes install libgeos-dev')

    sudo('easy_install pip')
    sudo('pip install virtualenv virtualenvwrapper pillow')

    put('conf/.bash_profile', '~/.bash_profile')


def env_run(cmd):
    return sudo(cmd) if env.environment_class in ['production', 'celery'] else run(cmd)

@task
def deploy_archive_file():
    filename = env.get('SHA1_FILENAME', None)
    if filename is None:
        filename = env.SHA1_FILENAME = get_sha1()
    file_name = '%s.zip' % filename
    if not files.exists('%s/%s' % (env.deploy_archive_path, file_name)):
        as_sudo = env.environment_class in ['production', 'celery']
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

@task
def clean_start():
    execute(clean_pyc)
    execute(clear_cache)
    execute(restart_service)

    execute(clean_zip)


def do_deploy():
    if env.SHA1_FILENAME is None:
        env.SHA1_FILENAME = get_sha1()

    version_path = '%sversions' % env.remote_project_path
    full_version_path = '%s/%s' % (version_path, env.SHA1_FILENAME)
    project_path = '%s%s' % (env.remote_project_path, env.project,)

    if env.environment_class in ['production', 'celery']:
        if not files.exists(version_path):
            env_run('mkdir -p %s' % version_path )
        env_run('chown -R %s:%s %s' % (env.application_user, env.application_user, env.remote_project_path) )

    deploy_archive_file()

    # extract project zip file:into a staging area and link it in
    if not files.exists('%s/manage.py'%full_version_path):
        unzip_archive()


@task
def update_env_conf():
    if env.SHA1_FILENAME is None:
        env.SHA1_FILENAME = get_sha1()

    version_path = '%sversions' % env.remote_project_path
    full_version_path = '%s/%s' % (version_path, env.SHA1_FILENAME)
    project_path = '%s%s' % (env.remote_project_path, env.project,)

    if not env.is_predeploy:
        # copy the live local_settings
        with cd(project_path):
            virtualenv('cp %s/conf/%s.local_settings.py %s/%s/local_settings.py' % (full_version_path, env.environment, full_version_path, env.project))
            virtualenv('cp %s/conf/%s.wsgi.py %s/%s/wsgi.py' % (full_version_path, env.environment, full_version_path, env.project))
            virtualenv('cp %s/conf/%s.newrelic.ini %s/%s/newrelic.ini' % (full_version_path, env.environment, full_version_path, env.project))

@task
def unzip_archive():
    version_path = '%sversions' % env.remote_project_path
    with cd('%s' % version_path):
        virtualenv('unzip %s%s.zip -d %s' % (env.deploy_archive_path, env.SHA1_FILENAME, version_path,))

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
    sha = env.get('SHA1_FILENAME', None)
    if sha is None:
        env.SHA1_FILENAME = get_sha1()
    
    project_path = '%sversions/%s' % (env.remote_project_path, env.SHA1_FILENAME,)
    requirements_path = '%s/requirements.txt' % (project_path, )

    virtualenv('pip install -r %s' % requirements_path )

@task
@serial
def newrelic_note():
    if not hasattr(env, 'deploy_desc'):
        env.deploy_desc = prompt(colored('Hi %s, Please provide a Deployment Note:' % env.local_user, 'yellow'))

@task
@serial
def newrelic_deploynote():
    if not env.deploy_desc:
        print colored('No env.deploy_desc was defined cant post to new relic', 'yellow')
    else:
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
def conclude():
    execute(newrelic_deploynote)

@task
def deploy(is_predeploy='False',full='False',db='False',search='False'):
    """
    :is_predeploy=True - will deploy the latest MASTER SHA but not link it in: this allows for assets collection
    and requirements update etc...
    """
    true_list = ['true','t','y','yes','1',1]
    env.is_predeploy = True if is_predeploy.lower() in true_list else False
    full = True if full.lower() in true_list else False
    db = True if db.lower() in true_list else False
    search = True if search.lower() in true_list else False

    execute(newrelic_note)
    prepare_deploy()
    execute(do_deploy)
    execute(update_env_conf)
    #execute(celery_stop)

    if full:
        execute(requirements)
    if full or db:
        execute(syncdb)
        execute(migrate)
    if full or search:
        execute(update_index)

    execute(relink)
    execute(assets)
    execute(clean_start)
    #execute(celery_start)

