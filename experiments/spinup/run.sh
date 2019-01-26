#!/bin/bash

SLEEP_DUR=5
RUN_ITERATIONS=100
Update_Docker_Config() {
	if [ "$#" -ne 1 ]; then
                echo "Invalid args to Update_Docker_Config"
                exit 1
        fi

	suffix=".json"
	config="$1$suffix"

	cmd="cp $config  /etc/docker/daemon.json"
	echo "Executing $cmd"
	$cmd

	sleep $SLEEP_DUR # Sleep to avoid docker restarting too fast
	cmd="systemctl restart docker"
	echo "Executing $cmd"
        $cmd
}

Run_Docker_Container() {
	if [ "$#" -ne 2 ]; then
		echo "Invalid args to Run_Docker_Container"
		exit 1
	fi

	RUNTIME=$1
  CONTAINER_NAME=$2
  IMAGE=$3
  for (( i=1; i <= $RUN_ITERATIONS; ++i ))
  do
      docker rm /$CONTAINER_NAME
      docker run --name=$CONTAINER_NAME --security-opt seccomp:unconfined --runtime=$RUNTIME $IMAGE
      bash ./c_spinup/measure_startup.sh
  done
}
#Creating images
docker build -t c_spinup ./c_spinup/
docker build -t python_spinup_clean ./python_spinup/

#Running on normal docker
echo "This is for C_SPINUP with RUNC runtime setup."
Run_Docker_Container runc continer_c_spinup c_spinup

echo " "

echo "This is for PYTHON_SPINUP with RUNC runtime setup."
Run_Docker_Container runc continer_python_spinup_clean python_spinup_clean

TEST_PLATFORM="ptrace"
Update_Docker_Config $TEST_PLATFORM

echo "This is for C_SPINUP with RUNSC runtime setup in PTRACE."
Run_Docker_Container runsc continer_c_spinup c_spinup

echo " "

echo "This is for PYTHON_SPINUP with RUNSC runtime setup in PTRACE."
Run_Docker_Container runsc continer_python_spinup_clean python_spinup_clean

TEST_PLATFORM="kvm"
Update_Docker_Config $TEST_PLATFORM

echo "This is for C_SPINUP with RUNSC runtime setup in KVM."
Run_Docker_Container runsc continer_c_spinup c_spinup

echo " "

echo "This is for PYTHON_SPINUP with RUNSC runtime setup in KVM."
Run_Docker_Container runsc continer_python_spinup_clean python_spinup_clean

#Clean Up
docker image rm -f c_spinup
docker image rm -f python_spinup_clean
