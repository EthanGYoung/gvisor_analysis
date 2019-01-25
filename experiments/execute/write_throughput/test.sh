#!/bin/bash

#### Constants ####
if [ "$#" -ne 3 ]; then
	echo "Usage: sh tests.sh <TRIALS> <WRITE_SIZE> <FILE>"
	exit 1
fi

TRIALS=$1
WRITE_SIZE=$2
FILE=$3
SLEEP_DUR=5
 
#### Functions ####

# Expects  arg1 = (number of trials), arg2 = (size to be write), arg3 = (file to write)
Run_Bare_Metal() {
	if [ "$#" -ne 2 ]; then
		echo "Invalid args to Run_Bare_Metal"
		exit 1
	fi
	
	TEST_TRIALS=$1
	TEST_WRITE_SIZE=$2

	cmd="./write $TEST_TRIALS $TEST_WRITE_SIZE $FILE"
	echo "Executing: $cmd"
	$cmd
}

# Expects arg1 = (runc or runsc), arg2 = (number of trials), arg3 = (size to be write)
Run_Docker_Container() {
	if [ "$#" -ne 3 ]; then
		echo "Invalid args to Run_Docker_Container"
		exit 1
	fi

	RUNTIME=$1
	TEST_TRIALS=$2
	TEST_WRITE_SIZE=$3

	cmd="docker run --runtime=$RUNTIME --rm --tmpfs /myapp write $TEST_TRIALS $TEST_WRITE_SIZE $FILE"
	
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

	sleep $SLEEP_DUR # Sleep to avoid error restarting docker too much
	cmd="systemctl restart docker"
	echo "Executing $cmd"
        $cmd
}


#### Main Code ####

# Executes this test
echo "Executing test.sh for write throughput test"

# Build the materials (Could make write a variable)
echo "Building write image"
docker image rm write
docker build -t write .

echo "Compiling write binary"
gcc -o write -std=gnu99 write.c

# Run the tests
echo "Running tests"

echo "Running tests on bare metal"
Run_Bare_Metal $TRIALS $WRITE_SIZE

echo "Running tests on docker (runc)"
TEST_RUNTIME="runc"
Run_Docker_Container $TEST_RUNTIME $TRIALS $WRITE_SIZE

echo "Running tests on docker (runsc)"
TEST_RUNTIME="runsc"
TEST_PLATFORM="ptrace"
Update_Docker_Config $TEST_PLATFORM
Run_Docker_Container $TEST_RUNTIME $TRIALS $WRITE_SIZE

echo "Running tests on docker (runsc)"
TEST_RUNTIME="runsc"
TEST_PLATFORM="kvm"
Update_Docker_Config $TEST_PLATFORM
Run_Docker_Container $TEST_RUNTIME $TRIALS $WRITE_SIZE
