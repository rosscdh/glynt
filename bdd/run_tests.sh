#!/bin/bash
PROJECT_DIR=$PWD/../
BDD_DIR=$PWD
SAHI_DIR=$HOME/sahi/bin

source $WORKON_HOME/glynt/bin/activate

echo "Kill Previous Servers"
# Kill previously running testserver_plus server
kill -9 `ps -aef | grep "glynt/bin/python manage.py testserver" | grep -v grep | awk '{print $2}'` > /dev/null 2>&1
# Kill previously running sahi server
kill -9 `ps -aef | grep "/usr/bin/java -classpath :../lib/sahi.jar:" | grep -v grep | awk '{print $2}'` > /dev/null 2>&1

cd $PROJECT_DIR
# Run the project unit tests
python manage.py jenkins

# Run the testserver so that behat can find and use it
python manage.py testserver &

# echo "Starting Sahi Server"
cd $SAHI_DIR
./sahi.sh &

echo "Starting Behat Tests"
cd $BDD_DIR
./bin/behat -f junit --out ../reports

echo "Kill Servers"
# Kill the testserver_plus server
kill -9 `ps -aef | grep "glynt/bin/python manage.py testserver" | grep -v grep | awk '{print $2}'` > /dev/null 2>&1
# Kill running sahi server
kill -9 `ps -aef | grep "/usr/bin/java -classpath :../lib/sahi.jar:" | grep -v grep | awk '{print $2}'` > /dev/null 2>&1

echo "Tests complete"