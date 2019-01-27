#!/bin/bash

#### Functions ####

function join_by { local IFS="$1"; shift; echo "$*"; }

Run_Bare_Metal() {
        cmd="./$APP_NAME $PARAMS"
        echo "Executing: $cmd"
        $cmd
}

Run_Docker_Container() {
        if [[ ($FOLDER_PATH == *"import"*) ]]; then
          cmd="docker run --runtime=$RUNTIME --rm --tmpfs /myapp $APP_NAME"
	  for (( i=1; i <= $PARAMS; ++i ))
          do
            $cmd
          done
        elif [[ $FOLDER_PATH == *"spinup"* ]]; then
          CONTAINER_NAME=$APP_NAME$(echo "_container")
          cmd="docker run --name=$CONTAINER_NAME --runtime=$RUNTIME --tmpfs /myapp $APP_NAME"
          for (( i=1; i <= $PARAMS; ++i ))
          do
            docker rm $CONTAINER_NAME
            $cmd
            bash measure_startup.sh $CONTAINER_NAME
          done
        else
          cmd="docker run --runtime=$RUNTIME --rm --tmpfs /myapp $APP_NAME $PARAMS"
          echo "Executing: $cmd"
        fi
}
