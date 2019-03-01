package linux

import (
	"gvisor.googlesource.com/gvisor/pkg/sentry/kernel"
	"gvisor.googlesource.com/gvisor/pkg/sentry/usermem"
)

// Initailize constant values
const (FD_OFFSET = 100)		// This is the start FD claimed for in-mem files
const (BLOCK_SIZE = 1000000)
const (NUM_FDS = 100)
const (NUM_INODES = 1500)
const (NUM_FILES = 100)
const (NUM_BLOCKS = 1500)	// Number of inode blocks allowed per file 


// Define structs
type fd_entry struct {
	fd int
	used bool
	file_offset int	// Current offset into file
	append_f bool // True if passed in O_APPEND flag on open
	file_ptr *file
}

type inode_entry struct {
	inode []byte
	used bool
}

type file struct {
	filename string
	used bool		// True if opened/closed, but not removed
	inodes [NUM_BLOCKS]*inode_entry	// Array of pointers to inode_entries
	file_size int
}


var fd_table = []fd_entry{}
var inode_table = []inode_entry{}
var file_table = []file{}

// Initialize all structs and tables
func init() {
	init_fd_table()
	init_inode_table()
	init_file_table()
}

func init_fd_table() {
	for i:=0; i< NUM_FDS; i++ {
		fd := fd_entry{fd: FD_OFFSET + i, used: false, file_offset: 0, append_f: false, file_ptr: nil}
		fd_table =append(fd_table, fd)
	}
}

func init_inode_table() {
	for i:=0; i<NUM_INODES; i++ {
		inode := inode_entry{inode: make([]byte, BLOCK_SIZE), used: false}
		inode_table = append(inode_table,inode)
	}
}

func init_file_table(){
	for i:=0; i<NUM_FILES; i++ {
		f := file{filename: "" ,used: false,inodes:[NUM_BLOCKS]*inode_entry{},file_size:0}
		file_table = append(file_table,f)
	}
}


// In-Mem specific helper functions
func CreateFile(filename string, o_append bool) (*file,int){
	f, err:= FindUnusedFile()
	if err == -1 {//no available files
		return nil, -1
	}

	(*f).filename = filename
	(*f).used = true
	(*f).file_size = 0

	// File starts with one block
	AddInodeToFile(f)

	// File successfully added
	return f, 0
}

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

func FindFile(filename string) (*file,int) {
	var f *file
	if(file_table != nil){
		// Search file_table to find entry cooresponding to filename. Returns nil if not found.
		for i:=0; i<len(file_table); i++ {
			if (file_table[i].filename == filename) {
				return &file_table[i], 0
			}
		}
	}
	return f, -1
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
			return &(fd_table[i]), 0
                }
        }
        return f, -1
}

func FindUnusedFile()(*file, int){
	var f *file

	// Search for first unused file and return it
	for i:=0; i<NUM_FILES; i++ {
		if (!file_table[i].used) {
			return &(file_table[i]), 0
		}
	}

	return f, -1
}

func AddInodeToFile(f *file) {
	var in *inode_entry

	in = FindUnusedInode()
	(*in).used = true

	// Assign next opening in file to inode
	(*f).inodes[(*f).file_size/BLOCK_SIZE] = in
}

func SeekFD(fd int, offset int, whence int) (int) {
	if (!CheckValidFd(fd)) {
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
			f_entry.file_offset = (*f_entry).file_ptr.file_size
	}
	return f_entry.file_offset
}

// Checks if this file is an inmem file and does appropriate steps if it is and returns fd. Else returns nil
func InmemOpen(filename string, o_append bool) int {
	var f *file
	var err int

	// Check if listed statically and/or open already
	f,err = FindFile(filename)

	// Couldnt find entry, creating new file
	if (err == -1) {
		f, err = CreateFile(filename,o_append)
		if err != 0 {//failed to create file
			return -1
		}
	}

	var f_entry *fd_entry

	// Find unused FD and use as this files FD
	f_entry,err = FindUnusedFD()
	if err == -1 {//no available fd
		return -1
	}

	// Update fields in new File (File_size = 0 already and used = True from CreateFile and 1 block)
	(*f_entry).append_f = o_append
	(*f_entry).file_ptr = f
	(*f_entry).used = true

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

	// Setup FD for reuse. Keep File open in case program opens file again or other FD using it
	(*f_entry).used = false
	(*f_entry).file_offset = 0

	// File is now closed
	return 0
}

func CheckValidFd(fd int) bool{
//	return (fd >= FD_OFFSET && fd < NUM_FDS + FD_OFFSET)
	// Loops infinitely
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

	return (*f_entry).file_ptr.file_size != 0
}

func WriteToUserMem(t *kernel.Task, fd int, addr usermem.Addr, size int) (bool){
	if (!CheckValidFd(fd)) {
		return false
	}
	var f_entry = &fd_table[fd-FD_OFFSET]
	var f = (*f_entry).file_ptr

	// Set offset to end of file for appendable files
	if (f_entry.append_f) {
		f_entry.file_offset = f_entry.file_ptr.file_size
	}

	var start = f_entry.file_offset % BLOCK_SIZE

	// Keep writing to new blocks as long as still data to write
	for ((size/(BLOCK_SIZE - start)) > 0) {
		t.CopyInBytes(addr, (*(*f).inodes[f_entry.file_offset / BLOCK_SIZE]).inode[start : BLOCK_SIZE])
		f_entry.file_offset += (BLOCK_SIZE - start)
		size -= (BLOCK_SIZE - start)
		addr += (usermem.Addr)(BLOCK_SIZE - start)
		start = 0

		// Update size of file
		if (f.file_size < f_entry.file_offset) {
			f.file_size = f_entry.file_offset
			AddInodeToFile(f)
		}

	}
	// Write a partial block
	t.CopyInBytes(addr, (*(*f).inodes[f_entry.file_offset / BLOCK_SIZE]).inode[start:start+size])
	f_entry.file_offset += size
	// Update size of file
	if (f.file_size < f_entry.file_offset) {
		f.file_size = f_entry.file_offset
	}


	return true
}

// Assume user will only read within bounds of file
func ReadFromUserMem(t *kernel.Task, fd int, addr usermem.Addr, size int) (bool){
	if (!CheckValidFd(fd)) {
		return false
	}

	// TODO: Is this the same way Linux does it?
	if(!CheckValidRead(fd)){
		//Returning []byte{} (0 bytes)
		t.CopyOutBytes(addr, []byte{})
		return true
	}

	var f_entry = &fd_table[fd-FD_OFFSET]
	var f = (*f_entry).file_ptr

	var start = f_entry.file_offset % BLOCK_SIZE

	// TODO: Check that read is within bounds
	// Keep reading while size is non-zero
	for ((size/(BLOCK_SIZE-start)) > 0) {
		index := f_entry.file_offset / BLOCK_SIZE
		t.CopyOutBytes(addr, (*f).inodes[index].inode[start:BLOCK_SIZE])

		f_entry.file_offset += (BLOCK_SIZE - start)
		size -= (BLOCK_SIZE - start)
		addr += (usermem.Addr)(BLOCK_SIZE - start)
		start = 0
	}

	// Read from partial block
	t.CopyOutBytes(addr, (*((*f).inodes[f_entry.file_offset / BLOCK_SIZE])).inode[start:start+size])
	f_entry.file_offset += size
	return true
}
