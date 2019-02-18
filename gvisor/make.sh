bazel build runsc --verbose_failures
sudo cp ./bazel-bin/runsc/linux_amd64_pure_stripped/runsc /usr/local/bin
sudo systemctl restart docker
sudo rm -rf /tmp/runsc/
sudo docker run --runtime=runsc --rm --tmpfs /myapp correct
