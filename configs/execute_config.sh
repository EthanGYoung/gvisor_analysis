#!/bin/bash

#### Constants ####

TEST_EXECUTE_LIST=()

TEST_FILE="test.sh"

#### Execute ####

# getpid_throughput
GETPID_FOLDER_PATH="experiments/execute/GetpidThroughput/"
GETPID_APP_NAME="getpid"
GETPID_NUM_CALLS=(1000 10000 100000)

# network_throughput
NETWORK_FOLDER_PATH="experiments/execute/NetworkThroughput/"
NETWORK_APP_NAME="net"
NETWORK_TRIALS=2
NETWORK_URL=("http://speedtest.wdc01.softlayer.com/downloads/test10.zip" "http://speedtest.wdc01.softlayer.com/downloads/test100.zip" "http://speedtest.wdc01.softlayer.com/downloads/test1000.zip")

# read_throughput
READ_FOLDER_PATH="experiments/execute/ReadThroughput/"
READ_APP_NAME="read"
READ_TRIALS=10000
READ_READ_SIZE=(10 100) # Product of Trials and read size must be less than 10MB
READ_FILE="./file.txt"

# write_throughput
WRITE_FOLDER_PATH="experiments/execute/WriteThroughput/"
WRITE_APP_NAME="write"
WRITE_TRIALS=10000
WRITE_WRITE_SIZE=(100 1000)
WRITE_FILE="./file.txt"

	# Generate list of tests
gen_execute_cmds() {
  	RUNTIME=$1
	# Write throughput
	for i in ${WRITE_WRITE_SIZE[@]}
	do
		TEST_EXECUTE_LIST+=("$WRITE_FOLDER_PATH$TEST_FILE $WRITE_FOLDER_PATH $WRITE_APP_NAME $RUNTIME $WRITE_TRIALS $i $WRITE_FILE")
	done

	#Getpid_throughput
	for i in ${GETPID_NUM_CALLS[@]}
	do
		TEST_EXECUTE_LIST+=("$GETPID_FOLDER_PATH$TEST_FILE $GETPID_FOLDER_PATH $GETPID_APP_NAME $RUNTIME $i")
	done

	#Network_throughput
	for i in ${NETWORK_URL[@]}
	do
		TEST_EXECUTE_LIST+=("$NETWORK_FOLDER_PATH$TEST_FILE $NETWORK_FOLDER_PATH $NETWORK_APP_NAME $RUNTIME $NETWORK_TRIALS $i")
	done

	# Read_throughput
	for i in ${READ_READ_SIZE[@]}
	do
		TEST_EXECUTE_LIST+=("$READ_FOLDER_PATH$TEST_FILE $READ_FOLDER_PATH $READ_APP_NAME $RUNTIME $READ_TRIALS $i $READ_FILE")
	done
}
