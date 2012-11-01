# The Glynt Project #

## Basic Installation

1. easy_install pip
2. pip install virtualenv virtualenvwrapper
3. Perform these steps

    export WORKON_HOME=~/.virtualenvs
    mkdir -p $WORKON_HOME
    source /usr/local/bin/virtualenvwrapper.sh
    echo "source /usr/local/bin/virtualenvwrapper.sh" >> ~/.bash_profile

4. mkvirtualenv --no-site-packages glynt
5. cd /path/to/glynt
6. pip install -r requirements.txt : install update the required libraries (append --upgrade if you are not sure)
7. python manage.py syncdb : sync the database; and create teh default user if there is not already one
7a. python manage.py migrate socialregistration --fake : there is a small issue with socialregistration at the moment and its migration needs to be faked
8. python manage.py migrate : perform the rest of the migrations
9. python manage.py loaddata sites document_category document_flyform : load default fixtures
10. Thats it you can now python manage.py runserver_plus
11. access http://local.weareml.com:8000/ (you may need to add 127.0.0.1 local.weareml.com to your /etc/hosts file)

## Update requirments

1. pip install -r requirements.txt : install update the required libraries (append --upgrade if you are not sure)

## Default fixtures

1. python manage.py loaddata sites document_category document_flyform