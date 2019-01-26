#!/bin/bash

SLEEP_DUR=5
RUN_ITERATIONS=100

Run_Docker_Container() {
	if [ "$#" -ne 2 ]; then
		echo "Invalid args to Run_Docker_Container"
		exit 1
	fi

	RUNTIME=$1
  IMAGE=$2
  for (( i=1; i <= $RUN_ITERATIONS; ++i ))
  do
      docker run  --security-opt seccomp:unconfined --runtime=$RUNTIME $IMAGE
  done
}

TEST_PLATFORM="ptrace"
Update_Docker_Config $TEST_PLATFORM

echo ---------This is for STANDARD with RUNC runtime setup.----------
cd Standard
docker build -t python_spinup_with_imports .
Run_Docker_Container runc python_spinup_with_imports

echo " "

echo This is for STANDARD with RUNSC runtime setup in PTRACE env.
Run_Docker_Container runsc python_spinup_with_imports
docker image rm -f python_spinup_with_imports:latest
cd ..
echo " "

echo ---------This is for DJANGO with RUNC runtime setup.----------
cd django
docker build -t python_spinup_with_imports .
Run_Docker_Container runc python_spinup_with_imports

echo " "

echo This is for DJANGO with RUNSC runtime setup in PTRACE env.
Run_Docker_Container runsc python_spinup_with_imports
docker image rm -f python_spinup_with_imports:latest
cd ..
echo " "

echo ---------This is for NUMPY with RUNC runtime setup.----------
cd numpy
docker build -t python_spinup_with_imports .
Run_Docker_Container runc python_spinup_with_imports

echo " "

echo This is for NUMPY with RUNSC runtime setup in PTRACE env.
Run_Docker_Container runsc python_spinup_with_imports
docker image rm -f python_spinup_with_imports:latest
cd ..
echo " "

echo ---------This is for SETUPTOOLS with RUNC runtime setup.----------
cd setuptools
docker build -t python_spinup_with_imports .
Run_Docker_Container runc python_spinup_with_imports

echo " "

echo This is for SETUPTOOLS with RUNSC runtime setup in PTRACE env.
Run_Docker_Container runsc python_spinup_with_imports
docker image rm -f python_spinup_with_imports:latest
cd ..
echo " "

echo ---------This is for PIP with RUNC runtime setup.----------
cd pip
docker build -t python_spinup_with_imports .
Run_Docker_Container runc python_spinup_with_imports

echo " "

echo This is for PIP with RUNSC runtime setup in PTRACE env.
Run_Docker_Container runsc python_spinup_with_imports
docker image rm -f python_spinup_with_imports:latest
cd ..
echo " "

echo ---------This is for FLASK with RUNC runtime setup.----------
cd flask
docker build -t python_spinup_with_imports .
Run_Docker_Container runc python_spinup_with_imports

echo " "

echo This is for FLASK with RUNSC runtime setup in PTRACE env.
Run_Docker_Container runsc python_spinup_with_imports
docker image rm -f python_spinup_with_imports:latest
cd ..
echo " "

echo ---------This is for MATPLOTLIB with RUNC runtime setup.----------
cd matplotlib
docker build -t python_spinup_with_imports .
Run_Docker_Container runc python_spinup_with_imports

echo " "

echo This is for MATPLOTLIB with RUNSC runtime setup in PTRACE env.
Run_Docker_Container runsc python_spinup_with_imports
docker image rm -f python_spinup_with_imports:latest
cd ..
echo " "

echo ---------This is for WERKZEUG with RUNC runtime setup.----------
cd werkzeug
docker build -t python_spinup_with_imports .
Run_Docker_Container runc python_spinup_with_imports

echo " "

echo This is for WERKZEUG with RUNSC runtime setup in PTRACE env.
Run_Docker_Container runsc python_spinup_with_imports
docker image rm -f python_spinup_with_imports:latest
cd ..
echo " "

echo ---------This is for REQUESTS with RUNC runtime setup.----------
cd requests
docker build -t python_spinup_with_imports .
Run_Docker_Container runc python_spinup_with_imports

echo " "

echo This is for REQUESTS with RUNSC runtime setup in PTRACE env.
Run_Docker_Container runsc python_spinup_with_imports
docker image rm -f python_spinup_with_imports:latest
cd ..
echo " "

echo ---------This is for SQLALCHEMY with RUNC runtime setup.----------
cd sqlalchemy
docker build -t python_spinup_with_imports .
Run_Docker_Container runc python_spinup_with_imports

echo " "

echo This is for SQLALCHEMY with RUNSC runtime setup in PTRACE env.
Run_Docker_Container runsc python_spinup_with_imports
docker image rm -f python_spinup_with_imports:latest
cd ..
echo " "

echo ---------This is for JINJA2 with RUNC runtime setup.----------
cd jinja2
docker build -t python_spinup_with_imports .
Run_Docker_Container runc python_spinup_with_imports

echo " "

echo This is for JINJA2 with RUNSC runtime setup in PTRACE env.
Run_Docker_Container runsc python_spinup_with_imports
docker image rm -f python_spinup_with_imports:latest
cd ..
echo " "

TEST_PLATFORM="kvm"
Update_Docker_Config $TEST_PLATFORM

echo This is for STANDARD with RUNSC runtime setup in KVM ENV.
cd Standard
docker build -t python_spinup_with_imports .
Run_Docker_Container runsc python_spinup_with_imports
docker image rm -f python_spinup_with_imports:latest
cd ..
echo " "

echo This is for DJANGO with RUNSC runtime setup in KVM ENV.
cd django
docker build -t python_spinup_with_imports .
Run_Docker_Container runsc python_spinup_with_imports
docker image rm -f python_spinup_with_imports:latest
cd ..
echo " "

echo This is for NUMPY with RUNSC runtime setup in KVM ENV.
cd numpy
docker build -t python_spinup_with_imports .
Run_Docker_Container runsc python_spinup_with_imports
docker image rm -f python_spinup_with_imports:latest
cd ..
echo " "

echo This is for SETUPTOOLS with RUNSC runtime setup in KVM ENV.
cd setuptools
docker build -t python_spinup_with_imports .
Run_Docker_Container runsc python_spinup_with_imports
docker image rm -f python_spinup_with_imports:latest
cd ..
echo " "

echo This is for PIP with RUNSC runtime setup in KVM ENV.
cd pip
docker build -t python_spinup_with_imports .
Run_Docker_Container runsc python_spinup_with_imports
docker image rm -f python_spinup_with_imports:latest
cd ..
echo " "

echo This is for FLASK with RUNSC runtime setup in KVM ENV.
cd flask
docker build -t python_spinup_with_imports .
Run_Docker_Container runsc python_spinup_with_imports
docker image rm -f python_spinup_with_imports:latest
cd ..
echo " "

echo This is for MATPLOTLIB with RUNSC runtime setup in KVM ENV.
cd matplotlib
docker build -t python_spinup_with_imports .
Run_Docker_Container runsc python_spinup_with_imports
docker image rm -f python_spinup_with_imports:latest
cd ..
echo " "

echo This is for WERKZEUG with RUNSC runtime setup in KVM ENV.
cd werkzeug
docker build -t python_spinup_with_imports .
Run_Docker_Container runsc python_spinup_with_imports
docker image rm -f python_spinup_with_imports:latest
cd ..
echo " "

echo This is for REQUESTS with RUNSC runtime setup in KVM ENV.
cd requests
docker build -t python_spinup_with_imports .
Run_Docker_Container runsc python_spinup_with_imports
docker image rm -f python_spinup_with_imports:latest
cd ..
echo " "

echo This is for SQLALCHEMY with RUNSC runtime setup in KVM ENV.
cd sqlalchemy
docker build -t python_spinup_with_imports .
Run_Docker_Container runsc python_spinup_with_imports
docker image rm -f python_spinup_with_imports:latest
cd ..
echo " "

echo This is for JINJA2 with RUNSC runtime setup in KVM ENV.
cd jinja2
docker build -t python_spinup_with_imports .
Run_Docker_Container runsc python_spinup_with_imports
docker image rm -f python_spinup_with_imports:latest
cd ..
echo " "
