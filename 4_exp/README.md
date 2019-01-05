# Experiment Description

This experiment tests the network throughput that can be achieved on bare metal, Docker (runc), Docker (runsc) with ptrace, Docker (runsc) with KVM. This is important because we would like to know the cost of using gVisor in network heavy applications.

## Experiment Methods

1) Spin up container, REPEAT( curl a specific size file)
2) Run in different types of containers

# Current State

Finished. Future: May include writing on tmpfs for bare metal. Run with network passthrough option on gVisor to see if it is the network stack gvisor's redirection.

## Notes


## Author

Ethan Young
