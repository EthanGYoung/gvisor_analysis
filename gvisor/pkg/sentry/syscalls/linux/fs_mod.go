package linux

var FilePtr = -1
const TESTFD = 100;

func WriteToUserMem(interface{} addr, int size){
  *FilePtr = *addr;
}
func CheckFD(int FD){
  return (FD == TESTFD);
}
func ReadToUserMem(interface{} addr, int size){
  addr := make([]byte, size);
  copy(addr, FilePtr);
}
