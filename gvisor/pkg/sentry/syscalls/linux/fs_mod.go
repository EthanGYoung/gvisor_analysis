package linux

import (
  "unsafe"
	"gvisor.googlesource.com/gvisor/pkg/sentry/usermem"
)

var FilePtr *uint64
const (TESTFD = 100)

func WriteToUserMem(addr usermem.Addr, size int){
  ptrFromSystem := (*uint64)(unsafe.Pointer(addr))
  *FilePtr = *ptrFromSystem;
}
func CheckFD(FD int) bool{
  return (FD == int(TESTFD))
}
func ReadFromUserMem(addr usermem.Addr, size int){
  *(*uint64)(unsafe.Pointer(addr)) = *FilePtr
}
