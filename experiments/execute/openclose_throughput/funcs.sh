#!/bin/bash

#### Functions ####

function join_by { local IFS="$1"; shift; echo "$*"; }

DIR_PATH=""
get_dir_path() {
  #Get correct path to log
  DIR_PATH=$(echo $1 | cut -d' ' -f 1)
}

Run_Bare_Metal() {
  if [[ ($FOLDER_PATH == *"import"*) ]]; then
    cmd="python3 ./python_spinup_imports.py"
     for (( i=1; i <= $PARAMS; ++i ))
    do
      echo "Executing: $cmd"
      $cmd
    done
  elif [[ $FOLDER_PATH == *"thread"* ]]; then
    echo "Omitting thread related tests for bare metal."
  elif [[ $FOLDER_PATH == *"spinup"* ]]; then
    echo "Omitting spinup related tests for bare metal."
  else
    cmd="./$APP_NAME $PARAMS"
    echo "Executing: $cmd"
    $cmd
  fi
}

Run_Docker_Container() {
        if [[ ($FOLDER_PATH == *"import"*) ]]; then
          cmd="sudo docker run --runtime=$RUNTIME --rm --tmpfs /myapp $APP_NAME"
	         for (( i=1; i <= $PARAMS; ++i ))
          do
            $cmd
          done
	elif [[ $FOLDER_PATH == *"thread"* ]]; then
		if [[ $PARAMS == *"ptrace"* ]]; then
			Setup_Ptrace
		elif [[ $PARAMS == *"kvm"* ]]; then
			Setup_KVM
		fi
		echo "Special case for this test. It runs the docker containers internally"
		echo "Compiling $APP_NAME binary"
                echo "Executing: $COMPILE_CMD"
                $COMPILE_CMD
		cmd="./$APP_NAME $PARAMS"
		echo "Executing: $cmd"
		$cmd
        elif [[ $FOLDER_PATH == *"spinup"* ]]; then
          CONTAINER_NAME=$APP_NAME$(echo "_container")
          cmd="sudo docker run --name=$CONTAINER_NAME --runtime=$RUNTIME --tmpfs /myapp $APP_NAME"
          for (( i=1; i <= $PARAMS; ++i ))
          do
            docker rm $CONTAINER_NAME
            $cmd
            bash measure_startup.sh $CONTAINER_NAME
          done
        elif [[ $FOLDER_PATH == *"thread"* ]]; then
	  echo "Omitting thread spinup from docker tests."
	else
          cmd="sudo docker run --runtime=$RUNTIME --rm --tmpfs /myapp $APP_NAME $PARAMS"
          platform=$(grep -w "platform" /etc/docker/daemon.json)
	  echo "Platform: $platform"
	  echo "executing: $cmd"
          $cmd
        fi
}

Setup_Ptrace() {
	echo "Setting up docker for gvisor-ptrace"
	cp ptrace.json daemon.json
        sudo mv daemon.json /etc/docker/
        sudo systemctl restart docker
}

Setup_KVM() {
	echo "Setting up docker for gvisor-kvm"
	cp kvm.json daemon.json
        sudo mv daemon.json /etc/docker/
        sudo systemctl restart docker
}
