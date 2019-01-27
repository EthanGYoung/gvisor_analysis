#!/bin/bash

#### Main Code ####

FOLDER_PATH=$1

echo "Changing directory to test directory $FOLDER_PATH"
HOME_DIR=$(pwd)
cd $HOME_DIR$(echo "/")$FOLDER_PATH

source test_config.sh # To get NUM_ARGS and USAGE_CMD

if [ "$#" -ne $NUM_ARGS ]; then
	echo "Usage: $USAGE_CMD"
	cd $HOME_DIR
	exit 1
fi

APP_NAME=$2
RUNTIME=$3
shift 3 # FOLDER_PATH, RUNTIME and APP_NAME not included in args

echo "Sourcing config and function files"
source funcs.sh
source test_config.sh $APP_NAME

PARAMS=$(join_by ' ' "$@")

# Executes this test
echo "Executing test.sh for $APP_NAME throughput test"

# Can add more cases for test in future
case $RUNTIME in
	"bare")
		echo "Compiling $APP_NAME binary"
		echo "Executing: $COMPILE_CMD"
		$COMPILE_CMD

		echo "Running test on bare metal"
		Run_Bare_Metal $PARAMS

		echo "Removing old binary"
		rm $APP_NAME
		;;
	"runc" | "runsc")
		echo "Building $APP_NAME image"
		echo "Executing: $BUILD_CMD"
		$BUILD_CMD

		echo "Running test on docker ($RUNTIME)"
		Run_Docker_Container $RUNTIME $PARAMS
		
		echo "Removing container"
		$RM_CMD
		;;
	*)
		echo "$RUNTIME is not a valid RUNTIME arg for $APP_NAME. Not executing test."
		;;
esac

echo "Test completed. Returning to $HOME_DIR"
cd $HOME_DIR
