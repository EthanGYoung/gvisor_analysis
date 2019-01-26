#!/bin/bash

#Usage
NUM_ARGS=4
USAGE_CMD="sh test.sh <FOLDER_PATH> <APP_NAME> <RUNTIME> <NUM_TRAILS>"

# Building the programs
BUILD_CMD="docker build -t $APP_NAME ."
REMOVE_CMD="docker image rm -f $APP_NAME"
