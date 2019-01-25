#!/bin/bash

#### Constants ####
if [ "$#" -ne 3 ]; then
	echo "Usage: sh tests.sh <NUM_THREADS> <NUM_TRAILS> <NUM_SPINUPS_PER_THREAD>"
	exit 1
fi

NUM_THREADS=$1
NUM_TRIALS=$2
NUM_SPINUPS=$3
SLEEP_DUR=5
 
#### Functions ####

# Expects  arg1 = (number of trials), arg2 = (size to be spinup), arg3 = (file to spinup)
Run_Bare_Metal() {
	if [ "$#" -ne 4 ]; then
		echo "Invalid args to Run_Bare_Metal"
		exit 1
	fi

	TEST_NUM_THREADS=$1
	TEST_NUM_TRIALS=$2
	TEST_RUNTIME=$3
	TEST_NUM_SPINUPS=$4

	cmd="./spinup $TEST_NUM_THREADS $TEST_NUM_TRIALS $TEST_RUNTIME $TEST_NUM_SPINUPS"
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
echo "Executing test.sh for spinup throughput test"

# Build the materials (Could make spinup a variable)
echo "Building spinup image"
docker image rm spinup
docker build -t spinup .

echo "Compiling spinup binary"
gcc -pthread -o spinup -std=gnu99 spinup.c

# Run the tests
echo "Running tests"

echo "Running tests runc"
TEST_RUNTIME="runc"
Run_Bare_Metal $NUM_THREADS $NUM_TRIALS $TEST_RUNTIME $NUM_SPINUPS 

echo "Running tests runsc ptrace"
TEST_RUNTIME="runsc"
TEST_PLATFORM="ptrace"
Update_Docker_Config $TEST_PLATFORM
Run_Bare_Metal $NUM_THREADS $NUM_TRIALS $TEST_RUNTIME $NUM_SPINUPS 

echo "Running tests runsc kvm"
TEST_RUNTIME="runsc"
TEST_PLATFORM="kvm"
Update_Docker_Config $TEST_PLATFORM
Run_Bare_Metal $TEST_RUNTIME $NUM_THREADS $NUM_TRIALS $NUM_SPINUPS 
