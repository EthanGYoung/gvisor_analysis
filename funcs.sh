#!/bin/bash

#### Functions ####

function join_by { local IFS="$1"; shift; echo "$*"; }

Run_Bare_Metal() {
        cmd="./$APP_NAME $PARAMS"
        echo "Executing: $cmd"
        $cmd
}

Run_Docker_Container() {
        cmd="docker run --runtime=$RUNTIME --rm --tmpfs /myapp $APP_NAME $PARAMS"

        echo "Executing: $cmd"
        $cmd
}

