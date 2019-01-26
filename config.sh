#!/bin/bash

# getpid_throughput
GETPID_FOLDER_PATH="experiments/execute/getpid_throughput/"
GETPID_APP_NAME="getpid"
GETPID_NUM_CALLS=0

# network_throughput
NETWORK_FOLDER_PATH="experiments/execute/network_throughput/"
NETWORK_APP_NAME="net"
NETWORK_TRAILS=0
NETWORK_URL=0

# read_throughput
READ_FOLDER_PATH="experiments/execute/read_throughput/"
READ_APP_NAME="read"
READ_TRAILS=0
READ_READ_SIZE=0
READ_FILE=0

# write_throughput
WRITE_FOLDER_PATH="experiments/execute/write_throughput/"
WRITE_APP_NAME="write"
WRITE_TRAILS=0
WRITE_WRITE_SIZE=0
WRITE_FILE=0

# thread_spinup_throughput
THREAD_FOLDER_PATH="experiments/execute/thread_spinup_throughput/"
THREAD_APP_NAME="spinup"
THREAD_SPINUP_NUM_THREADS=0
THREAD_SPINUP_NUM_TRAILS=0
THREAD_SPINUP_NUM_SPINUPS_PER_THREAD=0

# import django
DJANGO_FOLDER_PATH="experiments/import/django/"
DJANGO_APP_NAME="django"
DJANGO_NUM_TRAILS=100

# import flask
FLASK_FOLDER_PATH="experiments/import/flask/"
FLASK_APP_NAME="flask"
FLASK_NUM_TRAILS=100

# import jinja2
JINJA2_FOLDER_PATH="experiments/import/jinja2/"
JINJA2_APP_NAME="jinja2"
JINJA2_NUM_TRAILS=100

# import matplotlib
MATPLOTLIB_FOLDER_PATH="experiments/import/matplotlib/"
MATPLOTLIB_APP_NAME="matplotlib"
MATPLOTLIB_NUM_TRAILS=100

# import numpy
NUMPY_FOLDER_PATH="experiments/import/numpy/"
NUMPY_APP_NAME="numpy"
NUMPY_NUM_TRAILS=100

# import pip
PIP_FOLDER_PATH="experiments/import/pip/"
PIP_APP_NAME="pip"
PIP_NUM_TRAILS=100

# import requests
REQUESTS_FOLDER_PATH="experiments/import/requests/"
REQUESTS_APP_NAME="requests"
REQUESTS_NUM_TRAILS=100

# import setuptools
SETUPTOOLS_FOLDER_PATH="experiments/import/setuptools/"
SETUPTOOLS_APP_NAME="setuptools"
SETUPTOOLS_NUM_TRAILS=100

# import sqlalchemy
SQLALCHEMY_FOLDER_PATH="experiments/import/sqlalchemy/"
SQLALCHEMY_APP_NAME="sqlalchemy"
SQLALCHEMY_NUM_TRAILS=100

# import Standard
STANDARD_FOLDER_PATH="experiments/import/Standard/"
STANDARD_APP_NAME="requests"
STANDARD_NUM_TRAILS=100

# import werkzeug
WERKZEUG_FOLDER_PATH="experiments/import/werkzeug/"
WERKZEUG_APP_NAME="werkzeug"
WERKZEUG_NUM_TRAILS=100

# spinup c
C_SPINUP_FOLDER_PATH="experiments/spinup/c_spinup/"
C_SPINUP_APP_NAME="c_spinup"
C_SPINUP_NUM_TRAILS=100

# spinup python
PYTHON_FOLDER_PATH="experiments/spinup/python_spinup/"
PYTHON_SPINUP_APP_NAME="python_spinup"
PYTHON_SPINUP_NUM_TRAILS=100
