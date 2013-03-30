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
5. ```cd /path/to/glynt```
6. ```pip install -r requirements.txt``` : install update the required libraries (append --upgrade if you are not sure)
7. ```python manage.py syncdb``` : sync the database; and create the default user if there is not already one
7a. ```python manage.py migrate socialregistration --fake``` : there is a small issue with socialregistration at the moment and its migration needs to be faked
8. ```python manage.py migrate``` : perform the rest of the migrations
9. ```python manage.py loaddata sites document_category documenttemplate lawyers legal```
10. ```python manage.py check_permissions``` # Creates the userena permissions
11. Thats it you can now ```python manage.py runserver_plus```
12. access http://local.weareml.com:8000/ (you may need to add 127.0.0.1 local.weareml.com to your /etc/hosts file)

## Update requirments

1. ```pip install --upgrade pip``` - ensure latest version
2. ```pip install -r requirements.txt``` : install update the required libraries (append --upgrade if you are not sure)


## Creating Fixtures

** Document Templates **

    `./manage.py dumpdata document.documenttemplate > glynt/apps/document/fixtures/documenttemplate.json`


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