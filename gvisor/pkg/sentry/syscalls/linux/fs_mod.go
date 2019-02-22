package linux

import (
  "gvisor.googlesource.com/gvisor/pkg/sentry/kernel"
  "gvisor.googlesource.com/gvisor/pkg/sentry/usermem"

)

// Initailize constant values
const (BLOCK_SIZE = 1000000)
const (TESTFD = 100)
const (NUM_FDS = 10)
const (FD_OFFSET = 100) // This is the start FD claimed for in-mem files
const (NUM_INODES = 10)
const (NUM_FILES = 2)
var STATIC_FILES = [NUM_FILES]string {"foo.txt", "bop.txt"}

// Define structs
type inmem_inode_entry struct {
	inode []byte
	used bool
}

type fd_entry struct {
	fd int
	used bool
	inode_entry *inmem_inode_entry
}

type dir_entry struct {
	key string
	inode_entry *inmem_inode_entry
}

var dir_table = []dir_entry{}
var fd_table = []fd_entry{}
var inode_table = []inmem_inode_entry{}

// Initialize all structs and tables
func init() {
	init_dir_table()
	init_fd_table()
	init_inode_table()
}

func init_dir_table() {
	// Add all static file names to dir table with not pointing to an inode entry
	for i:= 0; i < NUM_FILES; i++ {
		kv := dir_entry{key: STATIC_FILES[i], inode_entry: nil}
		dir_table = append(dir_table, kv)
	}
}

func init_fd_table() {
	for i:=0; i< NUM_FDS; i++ {
		fd := fd_entry{fd: FD_OFFSET + i, used: false, inode_entry: nil}
		fd_table =append(fd_table, fd)
	}
}

func init_inode_table() {
	for i:=0; i<NUM_INODES; i++ {
		inode := inmem_inode_entry{inode: make([]byte, BLOCK_SIZE), used: false}
		inode_table = append(inode_table, inode)
	}
}

// Helper functions for system calls
func CheckFD(FD int) bool{
  return (FD == int(TESTFD))
}

func WriteToUserMem(t *kernel.Task,addr usermem.Addr, size int){


 // t.CopyInBytes(addr, FilePtr)
}

func ReadFromUserMem(t *kernel.Task,addr usermem.Addr, size int) {
 // t.CopyOutBytes(addr, FilePtr)
}
