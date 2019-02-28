package linux

import (
  "gvisor.googlesource.com/gvisor/pkg/sentry/kernel"
  "gvisor.googlesource.com/gvisor/pkg/sentry/usermem"
)

// Initailize constant values
const (BLOCK_SIZE = 1100000)
const (NUM_FDS = 100)
const (FD_OFFSET = 100) // This is the start FD claimed for in-mem files
const (NUM_INODES = 100)

// Define structs
type inode_entry struct {
	inode []byte
	used bool
	ref_count int		// Number of unique FD's referring to this inode
}

type fd_entry struct {
	fd int
	used bool
	inodes *[]inode_entry
	file_offset int	// Current offset into file
	file_size int
	append_f bool // True if passed in O_APPEND flag on open
}

type dir_entry struct {
	key string
	inodes *[]inode_entry
}

var dir_table = []dir_entry{}
var fd_table = []fd_entry{}
var inode_table = []inode_entry{}

// Initialize all structs and tables
func init() {
	init_fd_table()
	init_inode_table()
}

func init_fd_table() {
	for i:=0; i< NUM_FDS; i++ {
		fd := fd_entry{fd: FD_OFFSET + i, used: false, inodes: &[]inode_entry{}, file_offset: 0, file_size: 0, append_f: false}
		fd_table =append(fd_table, fd)
	}
}

func init_inode_table() {
	for i:=0; i<NUM_INODES; i++ {
		inode_table = append(inode_table, inode_entry{inode: make([]byte, BLOCK_SIZE), used: false, ref_count: 0})
	}
}

func addDirEntry(filename string) {
	kv := dir_entry{key: filename, inodes: nil}
	dir_table = append(dir_table, kv)
}

// In-Mem specific helper functions
func FindFDEntry(fd int) (*fd_entry,int) {
	var f *fd_entry
	// Search fd_table to find corresponding fd_entry. If not found, return nil
	for i:=0; i<NUM_FDS; i++ {
		if (fd_table[i].used && fd_table[i].fd == fd) {
			f = &fd_table[i]
			return f, 0
		}
	}

	return f, -1
}

func FindDirEntry(filename string) (*dir_entry,int) {
	var d *dir_entry
  if(dir_table != nil){
    // Search dir_table to find entry cooresponding to filename. Returns nil if not found.
  	for i:=0; i<len(dir_table); i++ {
  		if (dir_table[i].key == filename) {
  			return &dir_table[i], 0
  		}
  	}
  }
	return d, -1
}

func FindUnusedInode() (*inode_entry) {
	var in inode_entry
        // Search inode_table to find unused inode_entry. Returns nil if not found.
        for i:=0; i<NUM_INODES; i++ {
                if (inode_table[i].used == false) {
                        return &(inode_table[i])
                }
        }

        return &in
}

func FindUnusedFD() (*fd_entry, int) {
	var f *fd_entry

	// Search for first unused fd and init for use by a file
	for i:=0; i<NUM_FDS; i++ {
		if (!fd_table[i].used) {
			f = &(fd_table[i])
			return f, 0
                }
        }

        return f, -1
}

func AddInodeToFD(entry *fd_entry) {
	var in *inode_entry
	in = FindUnusedInode()
	(*in).used = true
	(*in).ref_count += 1

	*(*entry).inodes = append(*(*entry).inodes, *in)
}

// Helper functions for system calls
func CheckFdRange(FD int) bool{
	return (FD >= FD_OFFSET && FD < FD_OFFSET + NUM_FDS)
}

func SeekFD(fd int, offset int, whence int) (int) {
	if (!CheckFdRange(fd)) {
		return -1
	}

	var f_entry = &fd_table[fd-FD_OFFSET]

	switch whence {
		case 0:
			// Seekset -> set file_offset to offset
			f_entry.file_offset = offset
		case 1:
			// Seekcurr -> set to current file_offset + offset
			f_entry.file_offset += offset
		case 2:
			// Seekend -> set to fileend (Not implementing + offset)
			f_entry.file_offset = f_entry.file_size
	}

	return f_entry.file_offset
}

// Checks if this file is an inmem file and does appropriate steps if it is and returns fd. Else returns nil
func InmemOpen(filename string, o_append bool, o_create bool) int {
	var d_entry *dir_entry
	var err int

	// Check if listed statically and/or open already
	d_entry,err = FindDirEntry(filename)

	// Add dir_entry to table
	if (err == -1) {
		addDirEntry(filename)

		// Search again for DirEntry
		d_entry,err = FindDirEntry(filename)
	}

	var f_entry *fd_entry
	// Find unused FD and use as this files FD
	f_entry,err = FindUnusedFD()
	(*f_entry).used = true
	(*f_entry).append_f = o_append

	if ((*d_entry).inodes == nil) {
		// Find unused inode to use
		AddInodeToFD(f_entry)

		(*d_entry).inodes = (*f_entry).inodes
	} else {
		// Reuse pointer from dir_entry
		f_entry.inodes = d_entry.inodes
	}

	// File is now open
	return f_entry.fd
}

//
func InmemClose(fd int) int {
  //Clean up fd entry
  var f_entry *fd_entry
  var err int

	f_entry, err = FindFDEntry(fd)
  // Cannot find file in fd table, error
  if (err == -1) {
		return -1
	}
  CleanFDEntry(f_entry)

  dir_table = UpdateDirTable(f_entry.inodes)

	// File is now closed
	return 0
}

func UpdateDirTable(i_entries *[]inode_entry) []dir_entry{

  for index, dir_entry := range dir_table {
    if(i_entries == dir_entry.inodes && (*i_entries)[0].used == false){
      if (len(dir_table) <= 1){
        return nil
      }
      if(index == 0){
        return dir_table[1:]
      }
      if (index == len(dir_table) - 1){
        return dir_table[0:index]
      }
      return append(dir_table[:index], dir_table[index+1:]...)
    }
  }
  return dir_table
}

func CleanFDEntry(f_entry *fd_entry){
  (*f_entry).used = false
  (*f_entry).append_f = false
  for index, _ := range *(*f_entry).inodes {
    // i_entry is the inode_entry from inodes
    i_entry := &(*(*f_entry).inodes)[index]
    (*i_entry).ref_count--
    if((*i_entry).ref_count <= 0){
      //No need to clean the inode content because overwriting anyway
      (*i_entry).ref_count = 0
      (*i_entry).used = false
    }
  }
  (*f_entry).file_offset = 0
  (*f_entry).file_size = 0
}
func CheckValidFd(fd int) bool{
  for _, f_entry := range fd_table {
    if(f_entry.used && f_entry.fd == fd){
      return true
    }
  }
  return false
}
func CheckValidRead(fd int) bool{
  f_entry, err := FindFDEntry(fd)
  if (err == -1){
    return false
  }
  return (*f_entry).file_size != 0
}

func WriteToUserMem(t *kernel.Task, fd int, addr usermem.Addr, size int) (bool){
	if (!CheckFdRange(fd)) {
		return false
	}
  if(!CheckValidFd(fd)){
    return false
  }

	var f_entry = &fd_table[fd-FD_OFFSET]

	// Set offset to end of file for appendable files
	if (f_entry.append_f) {
		f_entry.file_offset = f_entry.file_size
	}

	var start = f_entry.file_offset % BLOCK_SIZE

	// Keep writing to new blocks as long as still data to write
	for ((size/(BLOCK_SIZE - start)) > 0) {
		t.CopyInBytes(addr, (*(*f_entry).inodes)[f_entry.file_offset / BLOCK_SIZE].inode[start : BLOCK_SIZE])
		AddInodeToFD(f_entry)

		f_entry.file_offset += (BLOCK_SIZE - start)
		size -= (BLOCK_SIZE - start)
		start = 0
		// Iffy logic, does this work
		addr += (usermem.Addr)(BLOCK_SIZE - start)
	}

	// Write a partial block
	t.CopyInBytes(addr, (*(*f_entry).inodes)[f_entry.file_offset / BLOCK_SIZE].inode[start:start + size])
	f_entry.file_offset += size

	// Update size of file
	if (f_entry.file_size < f_entry.file_offset) {
		f_entry.file_size = f_entry.file_offset
	}

	return true
}

// Assume user will only read within bounds of file
func ReadFromUserMem(t *kernel.Task, fd int, addr usermem.Addr, size int) (bool){
	if (!CheckFdRange(fd)) {
		return false
	}

  if(!CheckValidRead(fd)){
    t.CopyOutBytes(addr, []byte{})
    return true
  }

	var f_entry = fd_table[fd-FD_OFFSET]
	var start = f_entry.file_offset % BLOCK_SIZE
	var data []byte

	// Keep reading while size is non-zero
	for ((size/(BLOCK_SIZE-start)) > 0) {
		index := f_entry.file_offset / BLOCK_SIZE
		data = append(data, (*f_entry.inodes)[index].inode[start:BLOCK_SIZE]...)

		f_entry.file_offset += (BLOCK_SIZE - start)
		size -= (BLOCK_SIZE - start)
		start = 0
	}

	// Fill partial block
	data = append(data, (*f_entry.inodes)[f_entry.file_offset / BLOCK_SIZE].inode[start:start+size]...)
	f_entry.file_offset += size
	t.CopyOutBytes(addr, data)
	return true
}
