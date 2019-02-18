package linux

import (
  "gvisor.googlesource.com/gvisor/pkg/sentry/kernel"
  "gvisor.googlesource.com/gvisor/pkg/sentry/usermem"

)

var FilePtr []byte
const (TESTFD = 100)

func WriteToUserMem(t *kernel.Task,addr usermem.Addr, size int){
  FilePtr = make([]byte, size)
  t.CopyIn(addr, FilePtr)
}
func CheckFD(FD int) bool{
  return (FD == int(TESTFD))
}
func ReadFromUserMem(t *kernel.Task,addr usermem.Addr, size int) {
  t.CopyOut(addr, FilePtr)
}
