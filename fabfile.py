from __future__ import with_statement
from fabric.api import *
from fabric.contrib.console import confirm
from fabric.contrib import files
from time import gmtime, strftime

debug = True

PROJECT = 'glynt'

PROJECT_PATH = '/home/rossc/Projects/Personal/RuleNumberOne/%s' % (PROJECT,)
#PROJECT_PATH = '/home/rossc/Projects/Personal/%s' % (PROJECT,)

PROJECT_DEPLOY_INSTANCE = ( ('glynt', 'cartvine_shoppers'),)

REMOTE_PROJECT_PATHS = []
for app, project in PROJECT_DEPLOY_INSTANCE:
  REMOTE_PROJECT_PATHS.append( (app, project, '/home/stard0g101/webapps/%s' % (project,)) )

live_hosts = ('stard0g101@stard0g101.webfactional.com')

FILENAME_TIMESTAMP = strftime("%m-%d-%Y-%H:%M:%S", gmtime())


@hosts(['localhost'])
def git_export():
  cd(PROJECT_PATH)
  local('git archive --format zip --output /tmp/%s.zip --prefix=%s/ master'%(PROJECT, PROJECT,), capture=False)


def prepare_deploy():
    git_export()
    put('/tmp/'+ PROJECT +'.zip', '/tmp/')


def conclude_deploy():
    run('unlink /tmp/%s.zip'%(PROJECT,))

def deploy(hard_deploy, env, app_name, project_name, remote_project_path):

    if hard_deploy == True:
      print 'IS A HARD DEPLOY'
      # run('rm -Rf %s/%s' %(remote_project_path, PROJECT,))
      # run('mkdir -p %s/%s' %(remote_project_path, PROJECT,))
    else:
      print 'IS A SOFT DEPLOY'

    # extract project zip file
    with cd('%s/'%(remote_project_path,)):
      run('unzip /tmp/%s.zip'%(PROJECT,))
      cd( '%s/%s'%(remote_project_path, project_name,))
      run('cp %s/%s/conf/%s.local_settings.py %s/%s/%s/local_settings.py'%(remote_project_path, PROJECT, env, remote_project_path, PROJECT, app_name,))
      run('cp %s/%s/conf/%s.wsgi.py %s/%s/%s/wsgi.py'%(remote_project_path, PROJECT, env, remote_project_path, PROJECT, app_name,))
      run('%s/apache2/bin/restart'%(remote_project_path,))
      # run('rm -Rf %s/%s/media'%(remote_project_path, project_name,))
      # run('rm -Rf %s/%s/static'%(remote_project_path, project_name,))


@hosts(live_hosts)
def deploy_live(hard=True):
  if hard in ['True', 'true', True]:
    hard_deploy = True
  else:
    hard_deploy = False

  env = 'live'
  prepare_deploy()

  for app_name, project, project_path in REMOTE_PROJECT_PATHS:
    deploy(hard_deploy, env, app_name, project, project_path)

  conclude_deploy()

