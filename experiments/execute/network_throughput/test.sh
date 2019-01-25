#!/bin/bash

#### Constants ####
if [ "$#" -ne 2 ]; then
	echo "Usage: sh tests.sh <TRIALS> <URL>"
	exit 1
fi

TRIALS=$1
URL=$2
SLEEP_DUR=5
 
#### Functions ####

# Expects  arg1 = (number of trials), arg2 = (size to be net), arg3 = (file to net)
Run_Bare_Metal() {
	if [ "$#" -ne 1 ]; then
		echo "Invalid args to Run_Bare_Metal"
		exit 1
	fi
	
	TEST_TRIALS=$1

	cmd="./net $TEST_TRIALS $URL"
	echo "Executing: $cmd"
	$cmd
}

# Expects arg1 = (runc or runsc), arg2 = (number of trials), arg3 = (size to be net)
Run_Docker_Container() {
	if [ "$#" -ne 2 ]; then
		echo "Invalid args to Run_Docker_Container"
		exit 1
	fi

	RUNTIME=$1
	TEST_TRIALS=$2

	cmd="docker run --runtime=$RUNTIME --rm --tmpfs /myapp net $TEST_TRIALS $URL"
	
	echo "Executing: $cmd"
	$cmd
}

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


#### Main Code ####

# Executes this test
echo "Executing test.sh for net throughput test"

# Build the materials (Could make net a variable)
echo "Building net image"
docker image rm net
docker build -t net .

echo "Compiling net binary"
gcc -o net -std=gnu99 net.c

# Run the tests
echo "Running tests"

echo "Running tests on bare metal"
Run_Bare_Metal $TRIALS 

echo "Running tests on docker (runc)"
TEST_RUNTIME="runc"
Run_Docker_Container $TEST_RUNTIME $TRIALS 

echo "Running tests on docker (runsc)"
TEST_RUNTIME="runsc"
TEST_PLATFORM="ptrace"
Update_Docker_Config $TEST_PLATFORM
Run_Docker_Container $TEST_RUNTIME $TRIALS 

echo "Running tests on docker (runsc)"
TEST_RUNTIME="runsc"
TEST_PLATFORM="kvm"
Update_Docker_Config $TEST_PLATFORM
Run_Docker_Container $TEST_RUNTIME $TRIALS 
