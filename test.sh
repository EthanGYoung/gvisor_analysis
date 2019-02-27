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


echo "Sourcing config and function files"
source funcs.sh
source test_config.sh $APP_NAME

# Generate paths to logs
get_dir_path $@
LOG_PATH=$HOME_DIR$(echo "/logs/")$DIR_PATH$(echo "test.log")

# Generate parameters used by test scripts
shift 3 # FOLDER_PATH, RUNTIME and APP_NAME not included in args
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
		Run_Bare_Metal $PARAMS >> $LOG_PATH
		echo " " >> $LOG_PATH
		echo "Saved log to $LOG_PATH"

		echo "Removing old binary"
		rm $APP_NAME
		;;
	"runc" | "runsc")
		echo "Building $APP_NAME image"
		# if [ $BUILD ]
		# then
			echo "Executing: $BUILD_CMD"
			$BUILD_CMD
		# fi

		echo "Running test on docker ($RUNTIME)"
		Run_Docker_Container $RUNTIME $PARAMS >> $LOG_PATH
		echo " " >> $LOG_PATH
		echo "Saved log to $LOG_PATH"

		# if [ $RM ]
		# then
			echo "Removing build"
			$RM_CMD
		# fi
		;;
	*)
		echo "$RUNTIME is not a valid RUNTIME arg for $APP_NAME. Not executing test."
		;;
esac
