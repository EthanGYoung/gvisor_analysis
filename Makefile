release = $(shell lsb_release -cs)

make docker:
	sudo apt-get update
	sudo apt-get install apt-transport-https ca-certificates curl gnupg-agent software-properties-common
	curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
	sudo apt-key fingerprint 0EBFCD88
	sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(release) stable"
	sudo apt-get update
	sudo apt-get install docker-ce
	#apt-cache madison docker-ce
	sudo apt-get install docker-ce=5:18.09.1~3-0~ubuntu-xenial

make gvisor:
	wget https://storage.googleapis.com/gvisor/releases/nightly/latest/runsc
	wget https://storage.googleapis.com/gvisor/releases/nightly/latest/runsc.sha512
	sha512sum -c runsc.sha512
	chmod a+x runsc
	sudo mv runsc /usr/local/bin
	rm runsc.*
	cp kvm.json daemon.json
	sudo mv daemon.json /etc/docker/
	sudo systemctl restart docker

make all:
	make docker gvisor
