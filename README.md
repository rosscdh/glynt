# The Glynt Project #

LawPal is platform that aims to make certain legal process simpler and give both the client and the lawyer a clear overview of what has and what is yet to be done.

Read more topics at: http://discourse.lawpal.com

The platform can be described as:

Every user of LawPal.com has a:

"**user**" account  
    which has a "**client**" profile

a "**user**" can be a  
    "**customer**"  
    who has 1 "**company**"

OR a "**user**" can be a  
    "**lawyer**"  
    who has 1 "**firm**"

a "**customer**"
    can create 1 or more  
    "**project**"(s)
    each project has 1 or more "**transact**"(ions)  
    each "**transact**"(ion) has many "**todo**" items  
    the "**project**" has 1 "**lawyer**" (or more ?tbd) assigned to it  

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

10. ```fab rebuild_local``` : will perform the following steps automatically:

    1. ````cp conf/dev.local_settings.py glynt/local_settings.py```
    2. ```python manage.py syncdb``` : sync the database; and create the default user if there is not already one
    3. ```python manage.py migrate``` : perform the rest of the migrations
    4. ```python manage.py loaddata sites cities_light transact```
    5. ```python manage.py check_permissions``` # Creates the userena permissions
    6. Thats it you can now ```python manage.py runserver_plus```
    7. access http://local.weareml.com:8000/ (you may need to add 127.0.0.1 local.weareml.com to your /etc/hosts file)

## Autoenv

```brew install autoenv```

1. cd into glynt dir and the .env file will do its magic

## Update requirments

1. ```pip install --upgrade pip``` - ensure latest version
2. ```pip install -r requirements.txt``` : install update the required libraries (append --upgrade if you are not sure)


## Webhook Callbacks - Crocdoc

1. install https://ngrok.com
2. run ```ngrok 127.0.0.1:8000```
3. this will give you a url like: http://19b51bbe.ngrok.com
4. register this url at the crocdoc url: https://crocodoc.com/settings/webhook/
5. interact with an uploaded crocdoc item attachment
    

## Start Celery Worker

```python manage.py celery worker --loglevel=info```


## Geos

```brew install geos```


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


## Markdown

1. For a complete overview of markdown: http://stackoverflow.com/editing-help
2. Install html2text to convert html to Markdown (pip install html2text)

## Docs

1. found in the /docs folder


## EC2 Account signin

```https://562971026743.signin.aws.amazon.com/console/ec2```


## Deployment ##

Valid environemnts are: staging|preview|production

```
export TARGET_ENV='staging'
fab $TARGET_ENV deploy assets
fab $TARGET_ENV requirements clean_pyc syncdb migrate
```

