#!/bin/bash
PROJECT_DIR=$PWD/../
BDD_DIR=$PWD

source $WORKON_HOME/glynt/bin/activate

echo "Kill Previous Servers"
# Kill previously running testserver_plus server
kill -9 `ps -aef | grep "manage.py testserver" | grep -v grep | awk '{print $2}'` > /dev/null 2>&1
# Kill previously running sahi server
kill -9 `ps -aef | grep "sahi" | grep -v grep | awk '{print $2}'` > /dev/null 2>&1

cd $PROJECT_DIR
# Run the project unit tests
python manage.py jenkins

rm /tmp/testserver.db

# Run the testserver so that behat can find and use it
python manage.py testserver --noinput --addrport 127.0.0.1:8001 sites.json test_users.json guardian_permissions.json document_category.json &

# echo "Starting Sahi Server"
$BDD_DIR/sahi.sh start


echo "Starting Behat Tests"
cd $BDD_DIR
./bin/behat -f junit --out ../reports

echo "Kill Servers"
# Kill the testserver_plus server
kill -9 `ps -aef | grep "manage.py testserver" | grep -v grep | awk '{print $2}'` > /dev/null 2>&1
# Kill running sahi server
kill -9 `ps -aef | grep "sahi" | grep -v grep | awk '{print $2}'` > /dev/null 2>&1

echo "Tests complete"
