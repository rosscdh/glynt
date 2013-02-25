from __future__ import with_statement
from fabric.api import *
from fabric.contrib.console import confirm
from fabric.contrib import files
from time import gmtime, strftime

debug = True

PROJECT = 'glynt'

PROJECT_PATH = '/home/rossc/Projects/Personal/RuleNumberOne/%s' % (PROJECT,)
#PROJECT_PATH = '/home/rossc/Projects/Personal/%s' % (PROJECT,)

PROJECT_DEPLOY_INSTANCE = (('glynt', 'glynt'),)

REMOTE_PROJECT_PATHS = []
for app, project in PROJECT_DEPLOY_INSTANCE:
  REMOTE_PROJECT_PATHS.append( (app, project, '/home/stard0g101/webapps/%s' % (project,)) )

HOSTS = {
    'staging': [],
    'production': ['stard0g101@stard0g101.webfactional.com']
}

env.user = 'stard0g101'
env.SHA1_FILENAME = None
env.DEPLOY_ARCHIVE_PATH = '~/'

FILENAME_TIMESTAMP = strftime("%m-%d-%Y-%H:%M:%S", gmtime())


@task
def git_export():
  cd(PROJECT_PATH)
  env.SHA1_FILENAME = local('git rev-parse --short --verify HEAD', capture=True)
  local('git archive --format zip --output /tmp/%s.zip --prefix=%s/ master' % (env.SHA1_FILENAME, env.SHA1_FILENAME,), capture=False)


def prepare_deploy():
    git_export()


def deploy_archive_file():
    put('/tmp/%s.zip'%(env.SHA1_FILENAME,), env.DEPLOY_ARCHIVE_PATH)

def conclude_deploy():
    run('unlink %s%s.zip' % (env.DEPLOY_ARCHIVE_PATH, env.SHA1_FILENAME,))


@task
def do_deploy():
    environment = env.environment
    app_name = env.app_name
    project_name =env.project_name
    remote_project_path = env.remote_project_path

    if env.SHA1_FILENAME is None:
        raise Exception('Must have a SHA1_FILENAME defined. Ensure you have run @git_export')

    version_path = '%s/versions' % (remote_project_path,)
    project_path = '%s/%s' % (remote_project_path, project_name,)

    if not files.exists(version_path):
        run('mkdir %s'%(version_path,))

    deploy_archive_file()

    # extract project zip file:into a staging area and link it in
    with cd('%s/' % (version_path,)):
        run('unzip %s%s.zip' % (env.DEPLOY_ARCHIVE_PATH, env.SHA1_FILENAME,))

        if files.exists(project_path):
            run('unlink %s'%(project_path,))

        run('ln -s %s/%s %s'%(version_path, env.SHA1_FILENAME, project_path,))

    # copy the live local_settings
    with cd(project_path):
        run('cp %s/%s/conf/%s.local_settings.py %s/%s/%s/local_settings.py' % (remote_project_path, PROJECT, environment, remote_project_path, PROJECT, app_name,))
        run('cp %s/%s/conf/%s.wsgi.py %s/%s/%s/wsgi.py' % (remote_project_path, PROJECT, environment, remote_project_path, PROJECT, app_name,))

    run('%s/apache2/bin/restart' % (remote_project_path,))


@task
def do_fixtures():
    # Activate virtualenv
    with prefix('workon %s' % (env.project_name,)):
        run('python %s/%s/manage.py loaddata sites document_category documenttemplate public/fixtures/cms.json' % (env.remote_project_path, PROJECT,))

@task
def fixtures(deploy_to_env='staging'):
    if deploy_to_env in HOSTS:

        env.hosts = HOSTS[deploy_to_env]

        for app_name, project_name, remote_project_path in REMOTE_PROJECT_PATHS:
            env.environment = deploy_to_env
            env.app_name = app_name
            env.project_name = project_name
            env.remote_project_path = remote_project_path
            execute(do_fixtures, hosts=env.hosts)
    else:
        raise Exception('%s is not defined in HOSTS' %(env,) )

@task
def do_assets():
    # Activate virtualenv
    with prefix('workon %s' % (env.project_name,)):
        run('python %s/%s/manage.py collectstatic --noinput' % (env.remote_project_path, PROJECT,))
        run('python %s/%s/manage.py compress --force' % (env.remote_project_path, PROJECT,))

@task
def assets(deploy_to_env='staging'):
    if deploy_to_env in HOSTS:

        env.hosts = HOSTS[deploy_to_env]

        for app_name, project_name, remote_project_path in REMOTE_PROJECT_PATHS:
            env.environment = deploy_to_env
            env.app_name = app_name
            env.project_name = project_name
            env.remote_project_path = remote_project_path
            execute(do_assets, hosts=env.hosts)
    else:
        raise Exception('%s is not defined in HOSTS' %(env,) )


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
    if deploy_to_env in HOSTS:

        env.hosts = HOSTS[deploy_to_env]

        for app_name, project_name, remote_project_path in REMOTE_PROJECT_PATHS:
            env.environment = deploy_to_env
            env.app_name = app_name
            env.project_name = project_name
            env.remote_project_path = remote_project_path
            execute(do_requirements, hosts=env.hosts)
    else:
        raise Exception('%s is not defined in HOSTS' %(env,) )

@task
def deploy(deploy_to_env='staging'):
    if deploy_to_env in HOSTS:
        env.hosts = HOSTS[deploy_to_env]

        prepare_deploy()

        for app_name, project_name, remote_project_path in REMOTE_PROJECT_PATHS:
            env.environment = deploy_to_env
            env.app_name = app_name
            env.project_name = project_name
            env.remote_project_path = remote_project_path

            execute(do_deploy, hosts=env.hosts)
            execute(conclude_deploy, hosts=env.hosts)

    else:
        raise Exception('%s is not defined in HOSTS' %(env,) )