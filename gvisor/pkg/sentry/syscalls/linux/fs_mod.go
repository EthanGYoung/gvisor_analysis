package linux

import (
  "gvisor.googlesource.com/gvisor/pkg/sentry/kernel"
  "gvisor.googlesource.com/gvisor/pkg/sentry/usermem"

)

var FilePtr []byte
const (TESTFD = 100)
const (BLOCK_SIZE = 1000000)

func init() {
  FilePtr = make([]byte, BLOCK_SIZE)
}

func WriteToUserMem(t *kernel.Task,addr usermem.Addr, size int){
  t.CopyInBytes(addr, FilePtr)
}
func CheckFD(FD int) bool{
  return (FD == int(TESTFD))
}
func ReadFromUserMem(t *kernel.Task,addr usermem.Addr, size int) {
  t.CopyOutBytes(addr, FilePtr)
}
