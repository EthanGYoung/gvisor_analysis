#!/bin/bash

COMPILE_CMD="gcc -o $APP_NAME -std=gnu99 $APP_NAME$(echo ".c")"
BUILD_CMD="docker image rm $APP_NAME ; docker build -t read ."
