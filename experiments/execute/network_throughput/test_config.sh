#!/bin/bash

#Usage
NUM_ARGS=5
USAGE_CMD="sh test.sh <FOLDER_PATH> <APP_NAME> <RUNTIME> <NUM_TRIALS> <URL>"

# Building the programs
COMPILE_CMD="gcc -o $APP_NAME -std=gnu99 $APP_NAME$(echo ".c")"
RM_CMD="docker image rm $APP_NAME"
BUILD_CMD="docker build -t $APP_NAME ."
