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

package fs

// afterLoad is invoked by stateify.
//
// Beyond the cache, this method's existence is required to ensure that this
// object is not marked "complete" until all dependent objects are also marked
// "complete". Implementations (e.g. see gofer_state.go) reach into the
// MountSourceOperations through this object, this is necessary on restore.
func (msrc *MountSource) afterLoad() {
	msrc.fscache = NewDirentCache(defaultDirentCacheSize)
}
