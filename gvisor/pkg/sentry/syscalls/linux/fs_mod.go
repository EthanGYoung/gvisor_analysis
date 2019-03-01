package linux

import (
	"gvisor.googlesource.com/gvisor/pkg/sentry/kernel"
	"gvisor.googlesource.com/gvisor/pkg/sentry/usermem"
)

// Initailize constant values
const (BLOCK_SIZE = 1100000)
const (NUM_FDS = 100)
const (FD_OFFSET = 100) // This is the start FD claimed for in-mem files
const (NUM_INODES = 1500)
const (NUM_DIR = 100)

// Define structs
type inode_entry struct {
	inode []byte
	used bool
	ref_count int		// Number of unique FD's referring to this inode
}

type file_meta struct {
	inodes *[]inode_entry
	file_size int
}

type fd_entry struct {
	fd int
	used bool
	closed bool
	file_offset int	// Current offset into file
	append_f bool // True if passed in O_APPEND flag on open
	meta file_meta
}

type dir_entry struct {
	key string
	used bool
  fds []int
}

var dir_table = []dir_entry{}
var fd_table = []fd_entry{}
var inode_table = []inode_entry{}

// Initialize all structs and tables
func init() {
	init_fd_table()
	init_inode_table()
	init_dir_table()
}

func init_fd_table() {
	for i:=0; i< NUM_FDS; i++ {
		fd := fd_entry{fd: FD_OFFSET + i, used: false,closed: true, file_offset: 0, append_f: false, meta: file_meta{inodes: nil, file_size:0}}
		fd_table =append(fd_table, fd)
	}
}

func init_inode_table() {
	for i:=0; i<NUM_INODES; i++ {
		inode := inode_entry{inode: make([]byte, BLOCK_SIZE), used: false}
		inode_table = append(inode_table,inode)
	}
}

func init_dir_table(){
	for i:=0; i<NUM_DIR; i++ {
		dir := dir_entry{key: "" ,used: false, fds: []int{}}
		dir_table = append(dir_table,dir)
	}
}

func addDirEntry(filename string, o_append bool) (*dir_entry,int){
	d_entry, err:= FindUnusedDir()
	if err == -1 {//no available dir
		return nil, -1
	}

	(*d_entry).key = filename
	(*d_entry).used = true

	//successful
	return d_entry, 0
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

func FindUnusedDir()(*dir_entry, int){
	var dir *dir_entry
	// Search for first unused dir and return it
	for i:=0; i<NUM_DIR; i++ {
		if (!dir_table[i].used) {
			dir = &(dir_table[i])
			return dir, 0
    }
  }
        return dir, -1
}

func AddInodeToFD(entry *fd_entry) {
	var in *inode_entry
	in = FindUnusedInode()
	(*in).used = true
	(*in).ref_count++

	*(*entry).meta.inodes = append(*(*entry).meta.inodes, *in)
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
			f_entry.file_offset = f_entry.meta.file_size
	}
	return f_entry.file_offset
}

// Checks if this file is an inmem file and does appropriate steps if it is and returns fd. Else returns nil
func InmemOpen(filename string, o_append bool) int {
	var d_entry *dir_entry
	var err int
	alreadyExistFlag := true

	// Check if listed statically and/or open already
	d_entry,err = FindDirEntry(filename)
	// Couldnt find entry, setting up new entry
	if (err == -1) {
		alreadyExistFlag = false
		d_entry, err = addDirEntry(filename,o_append)
		if err != 0 {//failed to add dir
			return -1
		}
	}

	var f_entry *fd_entry
	// Find unused FD and use as this files FD
	f_entry,err = FindUnusedFD()
	if err == -1 {//no available fd
		return -1
	}
	(*d_entry).fds = append((*d_entry).fds,(*f_entry).fd)
	(*f_entry).used = true
	(*f_entry).closed = false
	//file_offset is zero by default, meta is file_meta{inodes: nil, file_size:0}
	(*f_entry).append_f = o_append
	if alreadyExistFlag {
		f_entry_exist,f_err := FindFDEntry((*d_entry).fds[0])
		if f_err == -1 {//no available fd
			return -1
		}
		(*f_entry).meta.inodes = (*f_entry_exist).meta.inodes
	}else{
		(*f_entry).meta.inodes = &[]inode_entry{}
		AddInodeToFD(f_entry)
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
	// File is now closed
	return 0
}

func CleanFDEntry(f_entry *fd_entry){
	(*f_entry).closed = true
	(*f_entry).append_f = false
	for index, _ := range *(*f_entry).meta.inodes {
		// i_entry is the inode_entry from inodes
		i_entry := &(*(*f_entry).meta.inodes)[index]
		(*i_entry).ref_count--
		if((*i_entry).ref_count <= 0){
			//No need to clean the inode content because overwriting anyway
			(*i_entry).ref_count = 0
			(*i_entry).used = false
		}
	}

	(*f_entry).file_offset = 0
	(*f_entry).meta.file_size = 0
}

func CheckValidFd(fd int) bool{
	for _, f_entry := range fd_table {
		if(f_entry.used && f_entry.fd == fd && f_entry.closed == false){
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

	return (*f_entry).meta.file_size != 0
}

func UpdateAllFds(file_size int, fd int){
	//performance nightmare...
	for index, _ := range dir_table {
		for i, _ := range dir_table[index].fds {
			if(dir_table[index].fds[i] == fd){
				//delete this fd from the fds array of dir_entry
				for _, curr_fd := range dir_table[index].fds {
					f_entry,err := FindFDEntry(curr_fd)
					if err == -1{
						return
					}
					(*f_entry).meta.file_size = file_size
				}
				return
			}
		}
	}
}

func WriteToUserMem(t *kernel.Task, fd int, addr usermem.Addr, size int) (bool){
	if (!CheckValidFd(fd)) {
		return false
	}
	var f_entry = &fd_table[fd-FD_OFFSET]

	// Set offset to end of file for appendable files
	if (f_entry.append_f) {
		f_entry.file_offset = f_entry.meta.file_size
	}

	var start = f_entry.file_offset % BLOCK_SIZE

	// Keep writing to new blocks as long as still data to write
	for ((size/(BLOCK_SIZE - start)) > 0) {
		t.CopyInBytes(addr, (*(*f_entry).meta.inodes)[f_entry.file_offset / BLOCK_SIZE].inode[start : BLOCK_SIZE])
		AddInodeToFD(f_entry)

		f_entry.file_offset += (BLOCK_SIZE - start)
		size -= (BLOCK_SIZE - start)
		addr += (usermem.Addr)(BLOCK_SIZE - start)
		start = 0
	}

	// Write a partial block
	t.CopyInBytes(addr, (*(*f_entry).meta.inodes)[f_entry.file_offset / BLOCK_SIZE].inode[start:start + size])
	f_entry.file_offset += size

	// Update size of file
	if (f_entry.meta.file_size < f_entry.file_offset) {
		f_entry.meta.file_size = f_entry.file_offset
		UpdateAllFds(f_entry.meta.file_size,fd)
	}

	return true
}

// Assume user will only read within bounds of file
func ReadFromUserMem(t *kernel.Task, fd int, addr usermem.Addr, size int) (bool){

	if (!CheckValidFd(fd)) {
		return false
	}

	if(!CheckValidRead(fd)){
		//Returning []byte{} (0 bytes)
		t.CopyOutBytes(addr, []byte{})
		return true
	}

	var f_entry = fd_table[fd-FD_OFFSET]
	var start = f_entry.file_offset % BLOCK_SIZE

	// Keep reading while size is non-zero
	for ((size/(BLOCK_SIZE-start)) > 0) {
		index := f_entry.file_offset / BLOCK_SIZE
		t.CopyOutBytes(addr, (*f_entry.meta.inodes)[index].inode[start:BLOCK_SIZE])

		f_entry.file_offset += (BLOCK_SIZE - start)
		size -= (BLOCK_SIZE - start)
		addr += (usermem.Addr)(BLOCK_SIZE - start)
		start = 0
	}

	// Fill partial block
	t.CopyOutBytes(addr, (*f_entry.meta.inodes)[f_entry.file_offset / BLOCK_SIZE].inode[start:start+size])
	f_entry.file_offset += size
	return true
}
