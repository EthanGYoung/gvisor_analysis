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

#include <errno.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/statfs.h>
#include <unistd.h>
#include <string>
#include <vector>

#include "gmock/gmock.h"
#include "gtest/gtest.h"
#include "gtest/gtest.h"
#include "absl/strings/match.h"
#include "absl/strings/str_cat.h"
#include "absl/strings/string_view.h"
#include "test/syscalls/linux/file_base.h"
#include "test/util/cleanup.h"
#include "test/util/file_descriptor.h"
#include "test/util/fs_util.h"
#include "test/util/temp_path.h"
#include "test/util/test_util.h"

namespace gvisor {
namespace testing {

namespace {

class StatTest : public FileTest {};

TEST_F(StatTest, FstatatAbs) {
  struct stat st;

  // Check that the stat works.
  EXPECT_THAT(fstatat(AT_FDCWD, test_file_name_.c_str(), &st, 0),
              SyscallSucceeds());
  EXPECT_TRUE(S_ISREG(st.st_mode));
}

TEST_F(StatTest, FstatatEmptyPath) {
  struct stat st;
  const auto fd = ASSERT_NO_ERRNO_AND_VALUE(Open(test_file_name_, O_RDONLY));

  // Check that the stat works.
  EXPECT_THAT(fstatat(fd.get(), "", &st, AT_EMPTY_PATH), SyscallSucceeds());
  EXPECT_TRUE(S_ISREG(st.st_mode));
}

TEST_F(StatTest, FstatatRel) {
  struct stat st;
  int dirfd;
  auto filename = std::string(Basename(test_file_name_));

  // Open the temporary directory read-only.
  ASSERT_THAT(dirfd = open(GetAbsoluteTestTmpdir().c_str(), O_RDONLY),
              SyscallSucceeds());

  // Check that the stat works.
  EXPECT_THAT(fstatat(dirfd, filename.c_str(), &st, 0), SyscallSucceeds());
  EXPECT_TRUE(S_ISREG(st.st_mode));
  close(dirfd);
}

TEST_F(StatTest, FstatatSymlink) {
  struct stat st;

  // Check that the link is followed.
  EXPECT_THAT(fstatat(AT_FDCWD, "/proc/self", &st, 0), SyscallSucceeds());
  EXPECT_TRUE(S_ISDIR(st.st_mode));
  EXPECT_FALSE(S_ISLNK(st.st_mode));

  // Check that the flag works.
  EXPECT_THAT(fstatat(AT_FDCWD, "/proc/self", &st, AT_SYMLINK_NOFOLLOW),
              SyscallSucceeds());
  EXPECT_TRUE(S_ISLNK(st.st_mode));
  EXPECT_FALSE(S_ISDIR(st.st_mode));
}

TEST_F(StatTest, Nlinks) {
  TempPath basedir = ASSERT_NO_ERRNO_AND_VALUE(TempPath::CreateDir());

  // Directory is initially empty, it should contain 2 links (one from itself,
  // one from ".").
  EXPECT_THAT(Links(basedir.path()), IsPosixErrorOkAndHolds(2));

  // Create a file in the test directory. Files shouldn't increase the link
  // count on the base directory.
  TempPath file1 =
      ASSERT_NO_ERRNO_AND_VALUE(TempPath::CreateFileIn(basedir.path()));
  EXPECT_THAT(Links(basedir.path()), IsPosixErrorOkAndHolds(2));

  // Create subdirectories. This should increase the link count by 1 per
  // subdirectory.
  TempPath dir1 =
      ASSERT_NO_ERRNO_AND_VALUE(TempPath::CreateDirIn(basedir.path()));
  EXPECT_THAT(Links(basedir.path()), IsPosixErrorOkAndHolds(3));
  TempPath dir2 =
      ASSERT_NO_ERRNO_AND_VALUE(TempPath::CreateDirIn(basedir.path()));
  EXPECT_THAT(Links(basedir.path()), IsPosixErrorOkAndHolds(4));

  // Removing directories should reduce the link count.
  dir1.reset();
  EXPECT_THAT(Links(basedir.path()), IsPosixErrorOkAndHolds(3));
  dir2.reset();
  EXPECT_THAT(Links(basedir.path()), IsPosixErrorOkAndHolds(2));

  // Removing files should have no effect on link count.
  file1.reset();
  EXPECT_THAT(Links(basedir.path()), IsPosixErrorOkAndHolds(2));
}

TEST_F(StatTest, BlocksIncreaseOnWrite) {
  struct stat st;

  // Stat the empty file.
  ASSERT_THAT(fstat(test_file_fd_.get(), &st), SyscallSucceeds());

  const int initial_blocks = st.st_blocks;

  // Write to the file, making sure to exceed the block size.
  std::vector<char> buf(2 * st.st_blksize, 'a');
  ASSERT_THAT(write(test_file_fd_.get(), buf.data(), buf.size()),
              SyscallSucceedsWithValue(buf.size()));

  // Stat the file again, and verify that number of allocated blocks has
  // increased.
  ASSERT_THAT(fstat(test_file_fd_.get(), &st), SyscallSucceeds());
  EXPECT_GT(st.st_blocks, initial_blocks);
}

TEST_F(StatTest, PathNotCleaned) {
  TempPath basedir = ASSERT_NO_ERRNO_AND_VALUE(TempPath::CreateDir());

  // Create a file in the basedir.
  TempPath file =
      ASSERT_NO_ERRNO_AND_VALUE(TempPath::CreateFileIn(basedir.path()));

  // Stating the file directly should succeed.
  struct stat buf;
  EXPECT_THAT(lstat(file.path().c_str(), &buf), SyscallSucceeds());

  // Try to stat the file using a directory that does not exist followed by
  // "..".  If the path is cleaned prior to stating (which it should not be)
  // then this will succeed.
  const std::string bad_path = JoinPath("/does_not_exist/..", file.path());
  EXPECT_THAT(lstat(bad_path.c_str(), &buf), SyscallFailsWithErrno(ENOENT));
}

TEST_F(StatTest, PathCanContainDotDot) {
  TempPath basedir = ASSERT_NO_ERRNO_AND_VALUE(TempPath::CreateDir());
  TempPath subdir =
      ASSERT_NO_ERRNO_AND_VALUE(TempPath::CreateDirIn(basedir.path()));
  const std::string subdir_name = std::string(Basename(subdir.path()));

  // Create a file in the subdir.
  TempPath file =
      ASSERT_NO_ERRNO_AND_VALUE(TempPath::CreateFileIn(subdir.path()));
  const std::string file_name = std::string(Basename(file.path()));

  // Stat the file through a path that includes '..' and '.' but still resolves
  // to the file.
  const std::string good_path =
      JoinPath(basedir.path(), subdir_name, "..", subdir_name, ".", file_name);
  struct stat buf;
  EXPECT_THAT(lstat(good_path.c_str(), &buf), SyscallSucceeds());
}

TEST_F(StatTest, PathCanContainEmptyComponent) {
  TempPath basedir = ASSERT_NO_ERRNO_AND_VALUE(TempPath::CreateDir());

  // Create a file in the basedir.
  TempPath file =
      ASSERT_NO_ERRNO_AND_VALUE(TempPath::CreateFileIn(basedir.path()));
  const std::string file_name = std::string(Basename(file.path()));

  // Stat the file through a path that includes an empty component.  We have to
  // build this ourselves because JoinPath automatically removes empty
  // components.
  const std::string good_path = absl::StrCat(basedir.path(), "//", file_name);
  struct stat buf;
  EXPECT_THAT(lstat(good_path.c_str(), &buf), SyscallSucceeds());
}

TEST_F(StatTest, TrailingSlashNotCleanedReturnsENOTDIR) {
  TempPath basedir = ASSERT_NO_ERRNO_AND_VALUE(TempPath::CreateDir());

  // Create a file in the basedir.
  TempPath file =
      ASSERT_NO_ERRNO_AND_VALUE(TempPath::CreateFileIn(basedir.path()));

  // Stat the file with an extra "/" on the end of it.  Since file is not a
  // directory, this should return ENOTDIR.
  const std::string bad_path = absl::StrCat(file.path(), "/");
  struct stat buf;
  EXPECT_THAT(lstat(bad_path.c_str(), &buf), SyscallFailsWithErrno(ENOTDIR));
}

TEST_F(StatTest, LeadingDoubleSlash) {
  // Create a file, and make sure we can stat it.
  TempPath file = ASSERT_NO_ERRNO_AND_VALUE(TempPath::CreateFile());
  struct stat st;
  ASSERT_THAT(lstat(file.path().c_str(), &st), SyscallSucceeds());

  // Now add an extra leading slash.
  const std::string double_slash_path = absl::StrCat("/", file.path());
  ASSERT_TRUE(absl::StartsWith(double_slash_path, "//"));

  // We should be able to stat the new path, and it should resolve to the same
  // file (same device and inode).
  struct stat double_slash_st;
  ASSERT_THAT(lstat(double_slash_path.c_str(), &double_slash_st),
              SyscallSucceeds());
  EXPECT_EQ(st.st_dev, double_slash_st.st_dev);
  EXPECT_EQ(st.st_ino, double_slash_st.st_ino);
}

// Test that a rename doesn't change the underlying file.
TEST_F(StatTest, StatDoesntChangeAfterRename) {
  const TempPath old_dir = ASSERT_NO_ERRNO_AND_VALUE(TempPath::CreateDir());
  const TempPath new_path(NewTempAbsPath());

  struct stat st_old = {};
  struct stat st_new = {};

  ASSERT_THAT(stat(old_dir.path().c_str(), &st_old), SyscallSucceeds());
  ASSERT_THAT(rename(old_dir.path().c_str(), new_path.path().c_str()),
              SyscallSucceeds());
  ASSERT_THAT(stat(new_path.path().c_str(), &st_new), SyscallSucceeds());

  EXPECT_EQ(st_old.st_nlink, st_new.st_nlink);
  EXPECT_EQ(st_old.st_dev, st_new.st_dev);
  EXPECT_EQ(st_old.st_ino, st_new.st_ino);
  EXPECT_EQ(st_old.st_mode, st_new.st_mode);
  EXPECT_EQ(st_old.st_uid, st_new.st_uid);
  EXPECT_EQ(st_old.st_gid, st_new.st_gid);
  EXPECT_EQ(st_old.st_size, st_new.st_size);
}

// Test link counts with a regular file as the child.
TEST_F(StatTest, LinkCountsWithRegularFileChild) {
  const TempPath dir = ASSERT_NO_ERRNO_AND_VALUE(TempPath::CreateDir());

  struct stat st_parent_before = {};
  ASSERT_THAT(stat(dir.path().c_str(), &st_parent_before), SyscallSucceeds());
  EXPECT_EQ(st_parent_before.st_nlink, 2);

  // Adding a regular file doesn't adjust the parent's link count.
  const TempPath child =
      ASSERT_NO_ERRNO_AND_VALUE(TempPath::CreateFileIn(dir.path()));

  struct stat st_parent_after = {};
  ASSERT_THAT(stat(dir.path().c_str(), &st_parent_after), SyscallSucceeds());
  EXPECT_EQ(st_parent_after.st_nlink, 2);

  // The child should have a single link from the parent.
  struct stat st_child = {};
  ASSERT_THAT(stat(child.path().c_str(), &st_child), SyscallSucceeds());
  EXPECT_TRUE(S_ISREG(st_child.st_mode));
  EXPECT_EQ(st_child.st_nlink, 1);

  // Finally unlinking the child should not affect the parent's link count.
  ASSERT_THAT(unlink(child.path().c_str()), SyscallSucceeds());
  ASSERT_THAT(stat(dir.path().c_str(), &st_parent_after), SyscallSucceeds());
  EXPECT_EQ(st_parent_after.st_nlink, 2);
}

// This test verifies that inodes remain around when there is an open fd
// after link count hits 0.
TEST_F(StatTest, ZeroLinksOpenFdRegularFileChild) {
  // Setting the enviornment variable GVISOR_GOFER_UNCACHED to any value
  // will prevent this test from running, see the tmpfs lifecycle.
  //
  // We need to support this because when a file is unlinked and we forward
  // the stat to the gofer it would return ENOENT.
  const char* uncached_gofer = getenv("GVISOR_GOFER_UNCACHED");
  SKIP_IF(uncached_gofer != nullptr);

  // We don't support saving unlinked files.
  const DisableSave ds;

  const TempPath dir = ASSERT_NO_ERRNO_AND_VALUE(TempPath::CreateDir());
  const TempPath child = ASSERT_NO_ERRNO_AND_VALUE(TempPath::CreateFileWith(
      dir.path(), "hello", TempPath::kDefaultFileMode));

  // The child should have a single link from the parent.
  struct stat st_child_before = {};
  ASSERT_THAT(stat(child.path().c_str(), &st_child_before), SyscallSucceeds());
  EXPECT_TRUE(S_ISREG(st_child_before.st_mode));
  EXPECT_EQ(st_child_before.st_nlink, 1);
  EXPECT_EQ(st_child_before.st_size, 5);  // Hello is 5 bytes.

  // Open the file so we can fstat after unlinking.
  const FileDescriptor fd =
      ASSERT_NO_ERRNO_AND_VALUE(Open(child.path(), O_RDONLY));

  // Now a stat should return ENOENT but we should still be able to stat
  // via the open fd and fstat.
  ASSERT_THAT(unlink(child.path().c_str()), SyscallSucceeds());

  // Since the file has no more links stat should fail.
  struct stat st_child_after = {};
  ASSERT_THAT(stat(child.path().c_str(), &st_child_after),
              SyscallFailsWithErrno(ENOENT));

  // Fstat should still allow us to access the same file via the fd.
  struct stat st_child_fd = {};
  ASSERT_THAT(fstat(fd.get(), &st_child_fd), SyscallSucceeds());
  EXPECT_EQ(st_child_before.st_dev, st_child_fd.st_dev);
  EXPECT_EQ(st_child_before.st_ino, st_child_fd.st_ino);
  EXPECT_EQ(st_child_before.st_mode, st_child_fd.st_mode);
  EXPECT_EQ(st_child_before.st_uid, st_child_fd.st_uid);
  EXPECT_EQ(st_child_before.st_gid, st_child_fd.st_gid);
  EXPECT_EQ(st_child_before.st_size, st_child_fd.st_size);

  // TODO: This isn't ideal but since fstatfs(2) will always return
  // OVERLAYFS_SUPER_MAGIC we have no way to know if this fs is backed by a
  // gofer which doesn't support links.
  EXPECT_TRUE(st_child_fd.st_nlink == 0 || st_child_fd.st_nlink == 1);
}

// Test link counts with a directory as the child.
TEST_F(StatTest, LinkCountsWithDirChild) {
  const TempPath dir = ASSERT_NO_ERRNO_AND_VALUE(TempPath::CreateDir());

  // Before a child is added the two links are "." and the link from the parent.
  struct stat st_parent_before = {};
  ASSERT_THAT(stat(dir.path().c_str(), &st_parent_before), SyscallSucceeds());
  EXPECT_EQ(st_parent_before.st_nlink, 2);

  // Create a subdirectory and stat for the parent link counts.
  const TempPath sub_dir =
      ASSERT_NO_ERRNO_AND_VALUE(TempPath::CreateDirIn(dir.path()));

  // The three links are ".", the link from the parent, and the link from
  // the child as "..".
  struct stat st_parent_after = {};
  ASSERT_THAT(stat(dir.path().c_str(), &st_parent_after), SyscallSucceeds());
  EXPECT_EQ(st_parent_after.st_nlink, 3);

  // The child will have 1 link from the parent and 1 link which represents ".".
  struct stat st_child = {};
  ASSERT_THAT(stat(sub_dir.path().c_str(), &st_child), SyscallSucceeds());
  EXPECT_TRUE(S_ISDIR(st_child.st_mode));
  EXPECT_EQ(st_child.st_nlink, 2);

  // Finally delete the child dir and the parent link count should return to 2.
  ASSERT_THAT(rmdir(sub_dir.path().c_str()), SyscallSucceeds());
  ASSERT_THAT(stat(dir.path().c_str(), &st_parent_after), SyscallSucceeds());

  // Now we should only have links from the parent and "." since the subdir
  // has been removed.
  EXPECT_EQ(st_parent_after.st_nlink, 2);
}

// Test statting a child of a non-directory.
TEST_F(StatTest, ChildOfNonDir) {
  // Create a path that has a child of a regular file.
  const std::string filename = JoinPath(test_file_name_, "child");

  // Statting the path should return ENOTDIR.
  struct stat st;
  EXPECT_THAT(lstat(filename.c_str(), &st), SyscallFailsWithErrno(ENOTDIR));
}

// Verify that we get an ELOOP from too many symbolic links even when there
// are directories in the middle.
TEST_F(StatTest, LstatELOOPPath) {
  const TempPath dir = ASSERT_NO_ERRNO_AND_VALUE(TempPath::CreateDir());
  std::string subdir_base = "subdir";
  ASSERT_THAT(mkdir(JoinPath(dir.path(), subdir_base).c_str(), 0755),
              SyscallSucceeds());

  std::string target = JoinPath(dir.path(), subdir_base, subdir_base);
  std::string dst = JoinPath("..", subdir_base);
  ASSERT_THAT(symlink(dst.c_str(), target.c_str()), SyscallSucceeds());
  auto cleanup = Cleanup(
      [&target]() { EXPECT_THAT(unlink(target.c_str()), SyscallSucceeds()); });

  // Now build a path which is /subdir/subdir/... repeated many times so that
  // we can build a path that is shorter than PATH_MAX but can still cause
  // too many symbolic links. Note: Every other subdir is actually a directory
  // so we're not in a situation where it's a -> b -> a -> b, where a and b
  // are symbolic links.
  std::string path = dir.path();
  std::string subdir_append = absl::StrCat("/", subdir_base);
  do {
    absl::StrAppend(&path, subdir_append);
    // Keep appending /subdir until we would overflow PATH_MAX.
  } while ((path.size() + subdir_append.size()) < PATH_MAX);

  struct stat s = {};
  ASSERT_THAT(lstat(path.c_str(), &s), SyscallFailsWithErrno(ELOOP));
}

}  // namespace

}  // namespace testing
}  // namespace gvisor
