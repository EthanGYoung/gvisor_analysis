package linux

import (
  "gvisor.googlesource.com/gvisor/pkg/sentry/kernel"
  "gvisor.googlesource.com/gvisor/pkg/sentry/usermem"
  "fmt"
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

// In-Mem specific helper functions
func FindFDEntry(fd int) (fd_entry,int) {
	var f fd_entry
	// Search fd_table to find corresponding fd_entry. If not found, return nil
	for i:=0; i<NUM_FDS; i++ {
		if (fd_table[i].used && fd_table[i].fd == fd) {
			f = fd_table[i]
			return f, 0
		}
	}

	return f, -1
}

func FindDirEntry(filename string) (dir_entry,int) {
	var d dir_entry
	// Search dir_table to find entry cooresponding to filename. Returns nil if not found.
	for i:=0; i<NUM_FILES; i++ {
		if (dir_table[i].key == filename) {
			d = dir_table[i]
			return d, 0
		}
	}

	return d, -1
}
// Return errors for each
func FindUnusedInode() (*inmem_inode_entry) {
	var in inmem_inode_entry
        // Search inode_table to find unused inode_entry. Returns nil if not found.
        for i:=0; i<NUM_INODES; i++ {
                if (inode_table[i].used == false) {
                        return &(inode_table[i])
                }
        }

        return &in
}

func FindUnusedFD() (fd_entry, int) {
	var f fd_entry

	// Search for first unused fd and init for use by a file
	for i:=0; i<NUM_FDS; i++ {
		if (!fd_table[i].used) {
			f = fd_table[i]
			return f, 0
                }
        }

        return f, -1
}

// Helper functions for system calls
func CheckFdRange(FD int) bool{
	return (FD >= FD_OFFSET && FD < FD_OFFSET + NUM_FDS)
}

// Checks if this file is an inmem file and does appropriate steps if it is and returns fd. Else returns nil
func InmemOpen(filename string) int {
	var n dir_entry
	var err int

	fmt.Println("InmemOpen for filename: ", filename)

	// Check if listed statically and/or open already
	n,err = FindDirEntry(filename)

	// Open file to host, not in-mem
	if (err == -1) {
		return -1
	}

	var f fd_entry
	// Find unused FD and use as this files FD
	f,err = FindUnusedFD()
	f.used = true

	if (n.inode_entry == nil) {
		fmt.Println("InmemOpen: Attempting to find a new inode")

		// Find unused inode to use
		var in *inmem_inode_entry
		in = FindUnusedInode()
		(*in).used = true
		f.inode_entry = in
	} else {
		fmt.Println("InmemOpen: Reusing existing inode inode")
		// Reuse pointer from dir_entry
		f.inode_entry = n.inode_entry
	}

	// File is now open
	return f.fd

}

func WriteToUserMem(t *kernel.Task, fd int, addr usermem.Addr, size int) (bool){
	if (!CheckFdRange(fd)) {
		fmt.Println("FD not in range in write")
		return false
	}

	fmt.Println("About to write to fd", fd)
	t.CopyInBytes(addr, fd_table[fd-FD_OFFSET].inode_entry.inode)
	fmt.Println("Successfully wrote to fd", fd)
	return true
}

func ReadFromUserMem(t *kernel.Task, fd int, addr usermem.Addr, size int) (bool){
	if (!CheckFdRange(fd)) {
		fmt.Println("FD not in range in read")
		return false
	}

	fmt.Println("About to read to fd", fd)
	t.CopyOutBytes(addr, fd_table[fd-FD_OFFSET].inode_entry.inode)
	return true
}
