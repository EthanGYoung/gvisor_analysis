# gvisor_analysis
A collection of programs used for benchmarking gVisor performance.

# Experiment Guide
## Implemented
1) Read Throughput
2) Write Throughput
3) Thread Spinup Throughput
4) Network Throughput
5) getpid Throughput
6) Container Spinup Speed
7) Import Speed (Python)

## Future
* Google Cloud Functions performance

# Installing

To install all dependencies run the following command

```
$ make all
```

This will install all required dependencies for running gvisor_analysis on Ubuntu. This includes installing and configuring gvsior and docker.

# Usage

The following commands are available to execute the tests:

To execute all tests..
```
$ make test-all
```

To execute a subset of test configurations..

```
$ make test-bare           # To execute tests on only bare metal

$ make test-runc           # To execute tests only on docker's default runc runtime

$ make test-runsc-ptrace   # To execute tests only on gvisors runtime runsc using its ptrace platform

$ make test-runsc-kvm      # To execute tests only on gvisors runtime runsc using its kvm platform
```
