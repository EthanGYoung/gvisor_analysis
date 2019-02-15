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

package cmd

import (
	"context"
	"path/filepath"
	"syscall"

	"flag"
	"github.com/google/subcommands"
	"gvisor.googlesource.com/gvisor/runsc/boot"
	"gvisor.googlesource.com/gvisor/runsc/container"
	"gvisor.googlesource.com/gvisor/runsc/specutils"
)

// Restore implements subcommands.Command for the "restore" command.
type Restore struct {
	// Restore flags are a super-set of those for Create.
	Create

	// imagePath is the path to the saved container image
	imagePath string
}

// Name implements subcommands.Command.Name.
func (*Restore) Name() string {
	return "restore"
}

// Synopsis implements subcommands.Command.Synopsis.
func (*Restore) Synopsis() string {
	return "restore a saved state of container (experimental)"
}

// Usage implements subcommands.Command.Usage.
func (*Restore) Usage() string {
	return `restore [flags] <container id> - restore saved state of container.
`
}

// SetFlags implements subcommands.Command.SetFlags.
func (r *Restore) SetFlags(f *flag.FlagSet) {
	r.Create.SetFlags(f)
	f.StringVar(&r.imagePath, "image-path", "", "directory path to saved container image")

	// Unimplemented flags necessary for compatibility with docker.
	var d bool
	f.BoolVar(&d, "detach", false, "ignored")

	var nsr bool
	f.BoolVar(&nsr, "no-subreaper", false, "ignored")

	var wp string
	f.StringVar(&wp, "work-path", "", "ignored")
}

// Execute implements subcommands.Command.Execute.
func (r *Restore) Execute(_ context.Context, f *flag.FlagSet, args ...interface{}) subcommands.ExitStatus {
	if f.NArg() != 1 {
		f.Usage()
		return subcommands.ExitUsageError
	}

	id := f.Arg(0)
	conf := args[0].(*boot.Config)
	waitStatus := args[1].(*syscall.WaitStatus)

	bundleDir := r.bundleDir
	if bundleDir == "" {
		bundleDir = getwdOrDie()
	}
	spec, err := specutils.ReadSpec(bundleDir)
	if err != nil {
		Fatalf("reading spec: %v", err)
	}
	specutils.LogSpec(spec)

	if r.imagePath == "" {
		Fatalf("image-path flag must be provided")
	}

	restoreFile := filepath.Join(r.imagePath, checkpointFileName)

	c, err := container.Load(conf.RootDir, id)
	if err != nil {
		Fatalf("loading container: %v", err)
	}
	if err := c.Restore(spec, conf, restoreFile); err != nil {
		Fatalf("restoring container: %v", err)
	}

	ws, err := c.Wait()
	if err != nil {
		Fatalf("running container: %v", err)
	}
	*waitStatus = ws

	return subcommands.ExitSuccess
}
