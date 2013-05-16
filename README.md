# The Glynt Project #

## Basic Installation

1. ```easy_install pip```
2. ```pip install virtualenv virtualenvwrapper```
3. Perform these steps

    export WORKON_HOME=~/.virtualenvs
    mkdir -p $WORKON_HOME
    source /usr/local/bin/virtualenvwrapper.sh
    echo "source /usr/local/bin/virtualenvwrapper.sh" >> ~/.bash_profile

4. mkvirtualenv --no-site-packages glynt
5. ```mkdir -p ~/Projects```
6. ```cd ~/Projects```
7. ```git clone git@github.com:rosscdh/glynt.git```
8. ```cd glynt```
9. ```pip install -r requirements.txt``` : install update the required libraries (append --upgrade if you are not sure)
10. ```python manage.py syncdb``` : sync the database; and create the default user if there is not already one
10a. ```python manage.py migrate socialregistration --fake``` : there is a small issue with socialregistration at the moment and its migration needs to be faked
11. ```python manage.py migrate``` : perform the rest of the migrations
12. ```python manage.py loaddata sites lawyers legal cities_light```
13. ```python manage.py check_permissions``` # Creates the userena permissions
14. Thats it you can now ```python manage.py runserver_plus```
15. access http://local.weareml.com:8000/ (you may need to add 127.0.0.1 local.weareml.com to your /etc/hosts file)

## Update requirments

1. ```pip install --upgrade pip``` - ensure latest version
2. ```pip install -r requirements.txt``` : install update the required libraries (append --upgrade if you are not sure)

## Cities

Load all the city data

```manage.py cities_light --force-all```

## Creating Fixtures

** Document Templates **

`./manage.py dumpdata document.documenttemplate > glynt/apps/document/fixtures/documenttemplate.json`
`./manage.py dumpdata lawyer auth > public/fixtures/lawyers.json`
`./manage.py dumpdata firm deal endorsement > public/fixtures/legal.json`


## Model Graphs ##

```./manage.py graph_models -g -o  ~/Desktop/glynt-models.png firm lawyer deal endorsement auth```

## Fix Fixtures

### When manage.py dumpdata flyform.flyform --format=xml > ~/flyform.xml

Remember to replace bad json:

```vim glynt/apps/flyform/fixtures/flyform.xml```

    :%s/u'/"/gc
    :%s/',/\",/gc
    :%s/':/\":/gc
    :%s/'\}/\"\}/gc

### When manage.py dumpdata document.document --format=xml > ~/document.xml

Remember to remove invalid xml return characters using vim:

```vim glynt/apps/document/fixtures/document.xml```

    :%s/\%x0c/\r/gc


## Markdown

1. For a complete overview of markdown: http://stackoverflow.com/editing-help
2. Install html2text to convert html to Markdown (pip install html2text)

## Docs

1. found in the /docs folder


## EC2 Account signin

```https://562971026743.signin.aws.amazon.com/console/ec2```


## Postgres Backup and Restore

    sudo -u postgres -s pg_dump --no-owner --no-acl -Fc lawpal_prelaunch > lawpal_prelaunch.bak
    pg_restore -U rosscdh -h localhost -d lawpal_prelaunch -Fc lawpal_prelaunch.bak