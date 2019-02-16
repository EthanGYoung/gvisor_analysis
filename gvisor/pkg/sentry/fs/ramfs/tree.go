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

package ramfs

import (
	"fmt"
	"path"
	"strings"

	"gvisor.googlesource.com/gvisor/pkg/sentry/context"
	"gvisor.googlesource.com/gvisor/pkg/sentry/fs"
	"gvisor.googlesource.com/gvisor/pkg/sentry/fs/anon"
	"gvisor.googlesource.com/gvisor/pkg/sentry/usermem"
)

// MakeDirectoryTree constructs a ramfs tree of all directories containing
// subdirs. Each element of subdir must be a clean path, and cannot be empty or
// "/".
func MakeDirectoryTree(ctx context.Context, msrc *fs.MountSource, subdirs []string) (*fs.Inode, error) {
	root := emptyDir(ctx, msrc)
	for _, subdir := range subdirs {
		if path.Clean(subdir) != subdir {
			return nil, fmt.Errorf("cannot add subdir at an unclean path: %q", subdir)
		}
		if subdir == "" || subdir == "/" {
			return nil, fmt.Errorf("cannot add subdir at %q", subdir)
		}
		makeSubdir(ctx, msrc, root.InodeOperations.(*Dir), subdir)
	}
	return root, nil
}

// makeSubdir installs into root each component of subdir. The final component is
// a *ramfs.Dir.
func makeSubdir(ctx context.Context, msrc *fs.MountSource, root *Dir, subdir string) {
	for _, c := range strings.Split(subdir, "/") {
		if len(c) == 0 {
			continue
		}
		child, ok := root.FindChild(c)
		if !ok {
			child = emptyDir(ctx, msrc)
			root.AddChild(ctx, c, child)
		}
		root = child.InodeOperations.(*Dir)
	}
}

// emptyDir returns an empty *ramfs.Dir that is traversable but not writable.
func emptyDir(ctx context.Context, msrc *fs.MountSource) *fs.Inode {
	dir := NewDir(ctx, make(map[string]*fs.Inode), fs.RootOwner, fs.FilePermsFromMode(0555))
	return fs.NewInode(dir, msrc, fs.StableAttr{
		DeviceID:  anon.PseudoDevice.DeviceID(),
		InodeID:   anon.PseudoDevice.NextIno(),
		BlockSize: usermem.PageSize,
		Type:      fs.Directory,
	})
}
