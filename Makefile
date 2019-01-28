release = $(shell lsb_release -cs)

all:
	make docker gvisor

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

test-all:
	make test-bare test-runc test-runsc-ptrace test-runsc-kvm

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
