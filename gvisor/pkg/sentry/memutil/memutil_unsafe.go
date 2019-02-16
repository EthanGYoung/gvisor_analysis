// Copyright 2018 Google LLC
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

package memutil

import (
	"syscall"
	"unsafe"

	"golang.org/x/sys/unix"
)

// CreateMemFD creates a memfd file and returns the fd.
func CreateMemFD(name string, flags int) (fd int, err error) {
	p, err := syscall.BytePtrFromString(name)
	if err != nil {
		return -1, err
	}
	r0, _, e0 := syscall.Syscall(unix.SYS_MEMFD_CREATE, uintptr(unsafe.Pointer(p)), uintptr(flags), 0)
	if e0 != 0 {
		return -1, e0
	}
	return int(r0), nil
}
