#!/bin/bash

#### Constants ####

TEST_EXECUTE_LIST=()
TEST_IMPORT_LIST=()
TEST_LIFECYCLE_LIST=()
TEST_SPINUP_LIST=()

TEST_FILE="test.sh"

#### Execute ####


# getpid_throughput
GETPID_FOLDER_PATH="experiments/execute/getpid_throughput/"
GETPID_APP_NAME="getpid"
GETPID_NUM_CALLS=(1000 10000 100000)

# network_throughput
NETWORK_FOLDER_PATH="experiments/execute/network_throughput/"
NETWORK_APP_NAME="net"
NETWORK_TRIALS=2
NETWORK_URL=("http://speedtest.wdc01.softlayer.com/downloads/test10.zip" "http://speedtest.wdc01.softlayer.com/downloads/test100.zip" "http://speedtest.wdc01.softlayer.com/downloads/test1000.zip")

# read_throughput
READ_FOLDER_PATH="experiments/execute/read_throughput/"
READ_APP_NAME="read"
READ_TRIALS=10000
READ_READ_SIZE=(10 100) # Product of Trials and read size must be less than 10MB
READ_FILE="./file.txt"

# write_throughput
WRITE_FOLDER_PATH="experiments/execute/write_throughput/"
WRITE_APP_NAME="write"
WRITE_TRIALS=10000
WRITE_WRITE_SIZE=(100 1000)
WRITE_FILE="./file.txt"


#### lifecycle ####


# thread_spinup_throughput
THREAD_FOLDER_PATH="experiments/execute/thread_spinup_throughput/"
THREAD_APP_NAME="spinup"
THREAD_SPINUP_NUM_THREADS=1
THREAD_SPINUP_NUM_TRAILS=2
THREAD_SPINUP_NUM_SPINUPS_PER_THREAD=1

# Generate list of tests

#### import ####


# import django
DJANGO_FOLDER_PATH="experiments/import/django/"
DJANGO_APP_NAME="django"
DJANGO_NUM_TRAILS=1

# import flask
FLASK_FOLDER_PATH="experiments/import/flask/"
FLASK_APP_NAME="flask"
FLASK_NUM_TRAILS=1

# import jinja2
JINJA2_FOLDER_PATH="experiments/import/jinja2/"
JINJA2_APP_NAME="jinja2"
JINJA2_NUM_TRAILS=1

# import matplotlib
MATPLOTLIB_FOLDER_PATH="experiments/import/matplotlib/"
MATPLOTLIB_APP_NAME="matplotlib"
MATPLOTLIB_NUM_TRAILS=1

# import numpy
NUMPY_FOLDER_PATH="experiments/import/numpy/"
NUMPY_APP_NAME="numpy"
NUMPY_NUM_TRAILS=1

# import pip
PIP_FOLDER_PATH="experiments/import/pip/"
PIP_APP_NAME="pip"
PIP_NUM_TRAILS=1

# import requests
REQUESTS_FOLDER_PATH="experiments/import/requests/"
REQUESTS_APP_NAME="requests"
REQUESTS_NUM_TRAILS=1

# import setuptools
SETUPTOOLS_FOLDER_PATH="experiments/import/setuptools/"
SETUPTOOLS_APP_NAME="setuptools"
SETUPTOOLS_NUM_TRAILS=1

# import sqlalchemy
SQLALCHEMY_FOLDER_PATH="experiments/import/sqlalchemy/"
SQLALCHEMY_APP_NAME="sqlalchemy"
SQLALCHEMY_NUM_TRAILS=1

# import Standard
STANDARD_FOLDER_PATH="experiments/import/Standard/"
STANDARD_APP_NAME="requests"
STANDARD_NUM_TRAILS=1

# import werkzeug
WERKZEUG_FOLDER_PATH="experiments/import/werkzeug/"
WERKZEUG_APP_NAME="werkzeug"
WERKZEUG_NUM_TRAILS=1

# spinup c
C_SPINUP_FOLDER_PATH="experiments/spinup/c_spinup/"
C_SPINUP_APP_NAME="c_spinup"
C_SPINUP_NUM_TRAILS=1

# spinup python
PYTHON_FOLDER_PATH="experiments/spinup/python_spinup/"
PYTHON_SPINUP_APP_NAME="python_spinup"
PYTHON_SPINUP_NUM_TRAILS=1


generate_cmds() {
        RUNTIME=$1

        # Import
        TEST_IMPORT_LIST[0]="$DJANGO_FOLDER_PATH$(echo "test.sh")
                                                        $DJANGO_FOLDER_PATH
                                                        $DJANGO_APP_NAME
                                                        $RUNTIME
                                                        $DJANGO_NUM_TRAILS"
        TEST_IMPORT_LIST[1]="$FLASK_FOLDER_PATH$(echo "test.sh")
                                                        $FLASK_FOLDER_PATH
                                                        $FLASK_APP_NAME
                                                        $RUNTIME
                                                        $FLASK_NUM_TRAILS"
        TEST_IMPORT_LIST[2]="$JINJA2_FOLDER_PATH$(echo "test.sh")
                                                        $JINJA2_FOLDER_PATH
                                                        $JINJA2_APP_NAME
                                                        $RUNTIME
                                                        $JINJA2_NUM_TRAILS"
        TEST_IMPORT_LIST[3]="$MATPLOTLIB_FOLDER_PATH$(echo "test.sh")
                                                        $MATPLOTLIB_FOLDER_PATH
                                                        $MATPLOTLIB_APP_NAME
                                                        $RUNTIME
                                                        $MATPLOTLIB_NUM_TRAILS"
        TEST_IMPORT_LIST[4]="$NUMPY_FOLDER_PATH$(echo "test.sh")
                                                        $NUMPY_FOLDER_PATH
                                                        $NUMPY_APP_NAME
                                                        $RUNTIME
                                                        $NUMPY_NUM_TRAILS"
        TEST_IMPORT_LIST[5]="$PIP_FOLDER_PATH$(echo "test.sh")
                                                        $PIP_FOLDER_PATH
                                                        $PIP_APP_NAME
                                                        $RUNTIME
                                                        $PIP_NUM_TRAILS"
         TEST_IMPORT_LIST[6]="$REQUESTS_FOLDER_PATH$(echo "test.sh")
                                                        $REQUESTS_FOLDER_PATH
                                                        $REQUESTS_APP_NAME
                                                        $RUNTIME
                                                        $REQUESTS_NUM_TRAILS"
         TEST_IMPORT_LIST[7]="$SETUPTOOLS_FOLDER_PATH$(echo "test.sh")
                                                        $SETUPTOOLS_FOLDER_PATH
                                                        $SETUPTOOLS_APP_NAME
                                                        $RUNTIME
							$SETUPTOOLS_NUM_TRAILS"
         TEST_IMPORT_LIST[8]="$SQLALCHEMY_FOLDER_PATH$(echo "test.sh")
                                                        $SQLALCHEMY_FOLDER_PATH
                                                        $SQLALCHEMY_APP_NAME
                                                        $RUNTIME
                                                        $SQLALCHEMY_NUM_TRAILS"
         TEST_IMPORT_LIST[9]="$STANDARD_FOLDER_PATH$(echo "test.sh")
                                                        $STANDARD_FOLDER_PATH
                                                        $STANDARD_APP_NAME
                                                        $RUNTIME
                                                        $STANDARD_NUM_TRAILS"
         TEST_IMPORT_LIST[10]="$WERKZEUG_FOLDER_PATH$(echo "test.sh")
                                                        $WERKZEUG_FOLDER_PATH
                                                        $WERKZEUG_APP_NAME
                                                        $RUNTIME
                                                        $WERKZEUG_NUM_TRAILS"

	# Generate list of tests
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

	# Thread_throughput
	#TEST_LIFECYCLE_LIST+="$THREAD_FOLDER_PATH $THREAD_APP_NAME $THREAD_SPINUP_NUM_THREADS $THREAD_SPINUP_NUM_TRIALS $THREAD_SPINUP_NUM_SPINUPS_PER_THREAD"

}
