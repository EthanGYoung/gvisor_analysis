#!/bin/bash

#### Constants ####
if [ "$#" -ne 1 ]; then
	echo "Usage: sh tests.sh <NUM_CALLS>"
	exit 1
fi

NUM_CALLS=$1
SLEEP_DUR=5
 
#### Functions ####

# Expects  arg1 = (number of trials), arg2 = (size to be getpid), arg3 = (file to getpid)
Run_Bare_Metal() {
	if [ "$#" -ne 1 ]; then
		echo "Invalid args to Run_Bare_Metal"
		exit 1
	fi
	
	TEST_NUM_CALLS=$1

	cmd="./getpid $TEST_NUM_CALLS"
	echo "Executing: $cmd"
	$cmd
}

# Expects arg1 = (runc or runsc), arg2 = (number of trials), arg3 = (size to be getpid)
Run_Docker_Container() {
	if [ "$#" -ne 2 ]; then
		echo "Invalid args to Run_Docker_Container"
		exit 1
	fi

	RUNTIME=$1
	TEST_NUM_CALLS=$2

	cmd="docker run --runtime=$RUNTIME --rm --tmpfs /myapp getpid $TEST_NUM_CALLS"
	
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
echo "Executing test.sh for getpid throughput test"

# Build the materials (Could make getpid a variable)
echo "Building getpid image"
docker image rm getpid
docker build -t getpid .

echo "Compiling getpid binary"
gcc -o getpid -std=gnu99 getpid.c

# Run the tests
echo "Running tests"

echo "Running tests on bare metal"
Run_Bare_Metal $NUM_CALLS 

echo "Running tests on docker (runc)"
TEST_RUNTIME="runc"
Run_Docker_Container $TEST_RUNTIME $NUM_CALLS 

echo "Running tests on docker (runsc)"
TEST_RUNTIME="runsc"
TEST_PLATFORM="ptrace"
Update_Docker_Config $TEST_PLATFORM
Run_Docker_Container $TEST_RUNTIME $NUM_CALLS 

echo "Running tests on docker (runsc)"
TEST_RUNTIME="runsc"
TEST_PLATFORM="kvm"
Update_Docker_Config $TEST_PLATFORM
Run_Docker_Container $TEST_RUNTIME $NUM_CALLS 
