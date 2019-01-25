#!/bin/bash

#### Constants ####
if [ "$#" -ne 3 ]; then
	echo "Usage: sh tests.sh <TRIALS> <READ_SIZE> <FILE>"
	exit 1
fi

TRIALS=$1
READ_SIZE=$2
FILE=$3
 
#### Functions ####

# Expects  arg1 = (number of trials), arg2 = (size to be read), arg3 = (file to read)
Run_Bare_Metal() {
	if [ "$#" -ne 2 ]; then
		echo "Invalid args to Run_Bare_Metal"
		exit 1
	fi
	
	TEST_TRIALS=$1
	TEST_READ_SIZE=$2

	cmd="./read $TEST_TRIALS $TEST_READ_SIZE $FILE"
	echo "Executing: $cmd"
	$cmd
}

# Expects arg1 = (runc or runsc), arg2 = (number of trials), arg3 = (size to be read)
Run_Docker_Container() {
	if [ "$#" -ne 3 ]; then
		echo "Invalid args to Run_Docker_Container"
		exit 1
	fi

	RUNTIME = $1
	TEST_TRIALS = $2
	TEST_READ_SIZE = $3

	cmd = "docker run --runtime=$RUNTIME --rm --tmpfs /myapp read $TEST_TRIALS $TEST_READ_SIZE ./file.txt"
	
	echo "Executing: $cmd"
	$cmd
}

#### Main Code ####

# Executes this test
echo "Executing test.sh for read throughput test"

# Build the materials (Could make read a variable)
echo "Building read image"
#docker image rm read
#docker build -t read .

echo "Compiling read binary"
gcc -o read -std=gnu99 read.c

# Run the tests
echo "Running tests"

Run_Bare_Metal $TRIALS $READ_SIZE $FILE
