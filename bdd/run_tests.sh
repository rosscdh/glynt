#!/bin/bash
source $WORKON_HOME/glynt/bin/activate

# Kill previously running testserver_plus server
kill -9 `ps -aef | grep "glynt/bin/python manage.py testserver" | grep -v grep | awk '{print $2}'`

cd ../
$WORKON_HOME/glynt/bin/python manage.py testserver &

cd bdd/
./bin/behat -f junit --out results

# Kill the testserver_plus server
kill -9 `ps -aef | grep "glynt/bin/python manage.py testserver" | grep -v grep | awk '{print $2}'`