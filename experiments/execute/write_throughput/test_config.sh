#!/bin/bash


#Usage
NUM_ARGS=6
USAGE_CMD="sh test.sh <FOLDER_PATH> <APP_NAME> <RUNTIME> <NUM_TRIALS> <WRITE_SIZE> <WRITE_FILE_PATH>"

# Building the programs
COMPILE_CMD="gcc -o $APP_NAME -std=gnu99 $APP_NAME$(echo ".c")"
RM_CMD="sudo docker image rm $APP_NAME"
BUILD_CMD="sudo docker build -t $APP_NAME ."
