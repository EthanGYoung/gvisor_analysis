release = $(shell lsb_release -cs)

all:
	make docker gvisor python_libs email

docker:
	sudo apt-get update
	sudo apt-get -y install apt-transport-https ca-certificates curl gnupg-agent software-properties-common
	curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
	sudo apt-key fingerprint 0EBFCD88
	sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(release) stable"
	sudo apt-get update
	sudo apt-get -y install docker-ce
	#apt-cache madison docker-ce
	sudo apt-get -y install docker-ce=5:18.09.1~3-0~ubuntu-xenial

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

email:
	sudo apt-get -y install mutt

python_libs:
	sudo apt-get update
	#Currently the latest version of python
	sudo apt-get -y install python3
	sudo apt-get -y install python3-pip
	sudo apt-get -y install python-setuptools
	#sudo easy_install pip
	sudo apt-get -y install python3-dev
	sudo pip3 install  django
	sudo pip3 install  flask
	sudo pip3 install  matplotlib
	sudo pip3 install  sqlalchemy
	python3 --version

read_exp:
	dd if=/dev/urandom of=experiments/execute/read_throughput/file.txt bs=1M count=1000

test-all:
	make clean
	make read_exp
	make test-bare test-runc test-runsc-ptrace test-runsc-kvm
	python3 parse.py
	$(shell zip -r logs.zip logs/)
	$(shell echo "Message Body Here" | mutt -s "Log zip" -a logs.zip -- "eyoung8@wisc.edu")

test-bare:
	sudo bash run.sh bare configs/config.sh

test-email:
	$(shell echo "Message Body Here" | mutt -s "Subject Here" -a "./test.sh" eyoung8@wisc.edu)

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

test-dev:
	make clean
	sudo bash run.sh bare configs/dev_config.sh
	sudo bash run.sh runc configs/dev_config.sh
	sudo bash run.sh runsc configs/dev_config.sh

parse_logs:
	python3 parse.py

clean:
	sudo rm -rf logs/	
	sudo rm -f experiments/execute/read_throughput/file.txt
