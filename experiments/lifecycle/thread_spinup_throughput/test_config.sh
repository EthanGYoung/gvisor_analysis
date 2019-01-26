#!/bin/bash

#Usage
NUM_ARGS=7
USAGE_CMD="sh test.sh <FOLDER_PATH> <APP_NAME> <RUNTIME> <NUM_THREADs> <NUM_TRIALS> <RUNTIME> <NUM_SPINUPS_PER_THREAD>"

# Building the programs
COMPILE_CMD="gcc -o $APP_NAME -std=gnu99 -pthread $APP_NAME$(echo ".c")"
RM_CMD="docker image rm $APP_NAME"
BUILD_CMD="docker build -t $APP_NAME ."
