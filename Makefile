release = $(shell lsb_release -cs)

all:
	make docker gvisor python_libs

docker:
	sudo apt-get update
	sudo apt-get install apt-transport-https ca-certificates curl gnupg-agent software-properties-common
	curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
	sudo apt-key fingerprint 0EBFCD88
	sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(release) stable"
	sudo apt-get update
	sudo apt-get install docker-ce
	#apt-cache madison docker-ce
	sudo apt-get install docker-ce=5:18.09.1~3-0~ubuntu-xenial

gvisor:
	wget https://storage.googleapis.com/gvisor/releases/nightly/latest/runsc
	wget https://storage.googleapis.com/gvisor/releases/nightly/latest/runsc.sha512
	sha512sum -c runsc.sha512
	chmod a+x runsc
	sudo mv runsc /usr/local/bin
	rm runsc.*
	cp kvm.json daemon.json
	sudo mv daemon.json /etc/docker/
	sudo systemctl restart docker

python_libs:
	sudo apt-get update
	#Currently the latest version of python
	sudo apt-get install python3
	sudo apt-get install python3-pip
	python3 --version
	bash -i -c alias python=python3
	pip install django
	pip install flask
	pip install jinja2
	pip install matplotlib
	pip install numpy
	pip install pip
	pip install requests
	pip install setuptools
	pip install --user sqlalchemy
	pip install werkzeug

test-all:
	make test-bare test-runc test-runsc-ptrace test-runsc-kvm
	sudo chown -R $USER: logs/

test-bare:
	sudo bash run.sh bare configs/config.sh

test-runc:
	sudo bash run.sh runc configs/config.sh

test-runsc-ptrace:
	cp ptrace.json daemon.json
	sudo mv daemon.json /etc/docker/
	sudo systemctl restart docker
	sudo bash run.sh runsc configs/config.sh

test-runsc-kvm:
	cp kvm.json daemon.json
	sudo mv daemon.json /etc/docker/
	sudo systemctl restart docker
	sudo bash run.sh runsc configs/config.sh
