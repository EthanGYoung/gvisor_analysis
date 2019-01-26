#!/bin/bash


#### Main Code ####

if [ "$#" -ne 3 ]; then
	echo "Usage: sh test.sh <APP_NAME> <RUNTIME> <NUM_CALLS>"
	exit 1
fi

APP_NAME=$1
RUNTIME=$2
shift 2 # RUNTIME and APP_NAME not included in args

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
		;;
	*)
		echo "$RUNTIME is not a valid RUNTIME arg for $APP_NAME. Not executing test."
		;;
esac
