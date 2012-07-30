#!/bin/sh
export SAHI_HOME=/Users/rossc/Projects/sahi
SAHI_DIR=$SAHI_HOME/bin
PID_FILE=/tmp/.sahi

if [ "$1" = "start" ]; then
  #execute some command in the background here, using
  #the "&"-sign at the end of the command
  $SAHI_DIR/sahi.sh &
  PID=$!
  echo "$PID" > $PID_FILE
elif [ "$1" = "stop" ]; then
  kill -9 `cat $PID_FILE`
  rm $PID_FILE
else
  echo "Usage: <sahi.sh> start|stop"
  exit 1
fi