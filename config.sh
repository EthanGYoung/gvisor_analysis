#!/bin/bash

# getpid_throughput
GETPID_FOLDER_PATH="experiments/execute/getpid_throughput/"
GETPID_APP_NAME="getpid"
GETPID_NUM_CALLS=100000

# network_throughput
NETWORK_FOLDER_PATH="experiments/execute/network_throughput/"
NETWORK_APP_NAME="net"
NETWORK_TRAILS=2
NETWORK_URL="http://speedtest.wdc01.softlayer.com/downloads/test10.zip"

# read_throughput
READ_FOLDER_PATH="experiments/execute/read_throughput/"
READ_APP_NAME="read"
READ_TRAILS=10000
READ_READ_SIZE=100 # Product of Trials and read size must be less than 10MB 
READ_FILE="./file.txt"

# write_throughput
WRITE_FOLDER_PATH="experiments/execute/write_throughput/"
WRITE_APP_NAME="write"
WRITE_TRAILS=10010
WRITE_WRITE_SIZE=10000
WRITE_FILE="./file.txt"

# thread_spinup_throughput
THREAD_FOLDER_PATH="experiments/execute/thread_spinup_throughput/"
THREAD_APP_NAME="spinup"
THREAD_SPINUP_NUM_THREADS=1
THREAD_SPINUP_NUM_TRAILS=2
THREAD_SPINUP_NUM_SPINUPS_PER_THREAD=1
