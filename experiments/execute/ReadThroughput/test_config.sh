#!/bin/bash

#Usage
NUM_ARGS=6
USAGE_CMD="sh test.sh <FOLDER_PATH> <APP_NAME> <RUNTIME> <NUM_TRIALS> <READ_SIZE> <READ_FILE_PATH>"

# Building the programs
COMPILE_CMD="gcc -o $APP_NAME -std=gnu99 $APP_NAME$(echo ".c")"
RM_CMD="docker image rm $APP_NAME"
BUILD_CMD="docker build -t $APP_NAME ."
