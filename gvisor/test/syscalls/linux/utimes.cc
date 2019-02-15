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

#include <fcntl.h>
#include <sys/stat.h>
#include <sys/syscall.h>
#include <sys/time.h>
#include <sys/types.h>
#include <time.h>
#include <unistd.h>
#include <utime.h>
#include <string>

#include "absl/time/time.h"
#include "test/util/file_descriptor.h"
#include "test/util/fs_util.h"
#include "test/util/temp_path.h"
#include "test/util/test_util.h"

namespace gvisor {
namespace testing {

namespace {

// TODO: utimes(nullptr) does not pick the "now" time in the
// application's time domain, so when asserting that times are within a window,
// we expand the window to allow for differences between the time domains.
constexpr absl::Duration kClockSlack = absl::Milliseconds(100);

// TimeBoxed runs fn, setting before and after to (coarse realtime) times
// guaranteed* to come before and after fn started and completed, respectively.
//
// fn may be called more than once if the clock is adjusted.
//
// * See the comment on kClockSlack. gVisor breaks this guarantee.
void TimeBoxed(absl::Time* before, absl::Time* after,
               std::function<void()> const& fn) {
  do {
    // N.B. utimes and friends use CLOCK_REALTIME_COARSE for setting time (i.e.,
    // current_kernel_time()). See fs/attr.c:notify_change.
    //
    // notify_change truncates the time to a multiple of s_time_gran, but most
    // filesystems set it to 1, so we don't do any truncation.
    struct timespec ts;
    EXPECT_THAT(clock_gettime(CLOCK_REALTIME_COARSE, &ts), SyscallSucceeds());
    *before = absl::TimeFromTimespec(ts);

    fn();

    EXPECT_THAT(clock_gettime(CLOCK_REALTIME_COARSE, &ts), SyscallSucceeds());
    *after = absl::TimeFromTimespec(ts);

    if (*after < *before) {
      // Clock jumped backwards; retry.
      //
      // Technically this misses jumps small enough to keep after > before,
      // which could lead to test failures, but that is very unlikely to happen.
      continue;
    }

    if (IsRunningOnGvisor()) {
      // See comment on kClockSlack.
      *before -= kClockSlack;
      *after += kClockSlack;
    }
  } while (*after < *before);
}

void TestUtimesOnPath(std::string const& path) {
  struct stat statbuf;

  struct timeval times[2] = {{1, 0}, {2, 0}};
  EXPECT_THAT(utimes(path.c_str(), times), SyscallSucceeds());
  EXPECT_THAT(stat(path.c_str(), &statbuf), SyscallSucceeds());
  EXPECT_EQ(1, statbuf.st_atime);
  EXPECT_EQ(2, statbuf.st_mtime);

  absl::Time before;
  absl::Time after;
  TimeBoxed(&before, &after, [&] {
    EXPECT_THAT(utimes(path.c_str(), nullptr), SyscallSucceeds());
  });

  EXPECT_THAT(stat(path.c_str(), &statbuf), SyscallSucceeds());

  absl::Time atime = absl::TimeFromTimespec(statbuf.st_atim);
  EXPECT_GE(atime, before);
  EXPECT_LE(atime, after);

  absl::Time mtime = absl::TimeFromTimespec(statbuf.st_mtim);
  EXPECT_GE(mtime, before);
  EXPECT_LE(mtime, after);
}

TEST(UtimesTest, OnFile) {
  auto f = ASSERT_NO_ERRNO_AND_VALUE(TempPath::CreateFile());
  TestUtimesOnPath(f.path());
}

TEST(UtimesTest, OnDir) {
  auto dir = ASSERT_NO_ERRNO_AND_VALUE(TempPath::CreateDir());
  TestUtimesOnPath(dir.path());
}

TEST(UtimesTest, MissingPath) {
  auto path = NewTempAbsPath();
  struct timeval times[2] = {{1, 0}, {2, 0}};
  EXPECT_THAT(utimes(path.c_str(), times), SyscallFailsWithErrno(ENOENT));
}

void TestFutimesat(int dirFd, std::string const& path) {
  struct stat statbuf;

  struct timeval times[2] = {{1, 0}, {2, 0}};
  EXPECT_THAT(futimesat(dirFd, path.c_str(), times), SyscallSucceeds());
  EXPECT_THAT(fstatat(dirFd, path.c_str(), &statbuf, 0), SyscallSucceeds());
  EXPECT_EQ(1, statbuf.st_atime);
  EXPECT_EQ(2, statbuf.st_mtime);

  absl::Time before;
  absl::Time after;
  TimeBoxed(&before, &after, [&] {
    EXPECT_THAT(futimesat(dirFd, path.c_str(), nullptr), SyscallSucceeds());
  });

  EXPECT_THAT(fstatat(dirFd, path.c_str(), &statbuf, 0), SyscallSucceeds());

  absl::Time atime = absl::TimeFromTimespec(statbuf.st_atim);
  EXPECT_GE(atime, before);
  EXPECT_LE(atime, after);

  absl::Time mtime = absl::TimeFromTimespec(statbuf.st_mtim);
  EXPECT_GE(mtime, before);
  EXPECT_LE(mtime, after);
}

TEST(FutimesatTest, OnAbsPath) {
  auto f = ASSERT_NO_ERRNO_AND_VALUE(TempPath::CreateFile());
  TestFutimesat(0, f.path());
}

TEST(FutimesatTest, OnRelPath) {
  auto d = ASSERT_NO_ERRNO_AND_VALUE(TempPath::CreateDir());
  auto f = ASSERT_NO_ERRNO_AND_VALUE(TempPath::CreateFileIn(d.path()));
  auto basename = std::string(Basename(f.path()));
  const FileDescriptor dirFd =
      ASSERT_NO_ERRNO_AND_VALUE(Open(d.path(), O_RDONLY | O_DIRECTORY));
  TestFutimesat(dirFd.get(), basename);
}

TEST(FutimesatTest, InvalidNsec) {
  auto f = ASSERT_NO_ERRNO_AND_VALUE(TempPath::CreateFile());
  struct timeval times[4][2] = {{
                                    {0, 1},                       // Valid
                                    {1, static_cast<int64_t>(1e7)}  // Invalid
                                },
                                {
                                    {1, static_cast<int64_t>(1e7)},  // Invalid
                                    {0, 1}                         // Valid
                                },
                                {
                                    {0, 1},  // Valid
                                    {1, -1}  // Invalid
                                },
                                {
                                    {1, -1},  // Invalid
                                    {0, 1}    // Valid
                                }};

  for (unsigned int i = 0; i < sizeof(times) / sizeof(times[0]); i++) {
    std::cout << "test:" << i << "\n";
    EXPECT_THAT(futimesat(0, f.path().c_str(), times[i]),
                SyscallFailsWithErrno(EINVAL));
  }
}

void TestUtimensat(int dirFd, std::string const& path) {
  struct stat statbuf;
  const struct timespec times[2] = {{1, 0}, {2, 0}};
  EXPECT_THAT(utimensat(dirFd, path.c_str(), times, 0), SyscallSucceeds());
  EXPECT_THAT(fstatat(dirFd, path.c_str(), &statbuf, 0), SyscallSucceeds());
  EXPECT_EQ(1, statbuf.st_atime);
  EXPECT_EQ(2, statbuf.st_mtime);

  // Test setting with UTIME_NOW and UTIME_OMIT.
  struct stat statbuf2;
  const struct timespec times2[2] = {
      {0, UTIME_NOW},  // Should set atime to now.
      {0, UTIME_OMIT}  // Should not change mtime.
  };

  absl::Time before;
  absl::Time after;
  TimeBoxed(&before, &after, [&] {
    EXPECT_THAT(utimensat(dirFd, path.c_str(), times2, 0), SyscallSucceeds());
  });

  EXPECT_THAT(fstatat(dirFd, path.c_str(), &statbuf2, 0), SyscallSucceeds());

  absl::Time atime2 = absl::TimeFromTimespec(statbuf2.st_atim);
  EXPECT_GE(atime2, before);
  EXPECT_LE(atime2, after);

  absl::Time mtime = absl::TimeFromTimespec(statbuf.st_mtim);
  absl::Time mtime2 = absl::TimeFromTimespec(statbuf2.st_mtim);
  // mtime should not be changed.
  EXPECT_EQ(mtime, mtime2);

  // Test setting with times = NULL. Should set both atime and mtime to the
  // current system time.
  struct stat statbuf3;
  TimeBoxed(&before, &after, [&] {
    EXPECT_THAT(utimensat(dirFd, path.c_str(), nullptr, 0), SyscallSucceeds());
  });

  EXPECT_THAT(fstatat(dirFd, path.c_str(), &statbuf3, 0), SyscallSucceeds());

  absl::Time atime3 = absl::TimeFromTimespec(statbuf3.st_atim);
  EXPECT_GE(atime3, before);
  EXPECT_LE(atime3, after);

  absl::Time mtime3 = absl::TimeFromTimespec(statbuf3.st_mtim);
  EXPECT_GE(mtime3, before);
  EXPECT_LE(mtime3, after);

  if (!IsRunningOnGvisor()) {
    // FIXME: Gofers set atime and mtime to different "now" times.
    EXPECT_EQ(atime3, mtime3);
  }
}

TEST(UtimensatTest, OnAbsPath) {
  auto f = ASSERT_NO_ERRNO_AND_VALUE(TempPath::CreateFile());
  TestUtimensat(0, f.path());
}

TEST(UtimensatTest, OnRelPath) {
  auto d = ASSERT_NO_ERRNO_AND_VALUE(TempPath::CreateDir());
  auto f = ASSERT_NO_ERRNO_AND_VALUE(TempPath::CreateFileIn(d.path()));
  auto basename = std::string(Basename(f.path()));
  const FileDescriptor dirFd =
      ASSERT_NO_ERRNO_AND_VALUE(Open(d.path(), O_RDONLY | O_DIRECTORY));
  TestUtimensat(dirFd.get(), basename);
}

TEST(UtimensatTest, OmitNoop) {
  // Setting both timespecs to UTIME_OMIT on a nonexistant path should succeed.
  auto path = NewTempAbsPath();
  const struct timespec times[2] = {{0, UTIME_OMIT}, {0, UTIME_OMIT}};
  EXPECT_THAT(utimensat(0, path.c_str(), times, 0), SyscallSucceeds());
}

// Verify that we can actually set atime and mtime to 0.
TEST(UtimeTest, ZeroAtimeandMtime) {
  const auto tmp_dir = ASSERT_NO_ERRNO_AND_VALUE(TempPath::CreateDir());
  const auto tmp_file =
      ASSERT_NO_ERRNO_AND_VALUE(TempPath::CreateFileIn(tmp_dir.path()));

  // Stat the file before and after updating atime and mtime.
  struct stat stat_before = {};
  EXPECT_THAT(stat(tmp_file.path().c_str(), &stat_before), SyscallSucceeds());

  ASSERT_NE(stat_before.st_atime, 0);
  ASSERT_NE(stat_before.st_mtime, 0);

  const struct utimbuf times = {};  // Zero for both atime and mtime.
  EXPECT_THAT(utime(tmp_file.path().c_str(), &times), SyscallSucceeds());

  struct stat stat_after = {};
  EXPECT_THAT(stat(tmp_file.path().c_str(), &stat_after), SyscallSucceeds());

  // We should see the atime and mtime changed when we set them to 0.
  ASSERT_EQ(stat_after.st_atime, 0);
  ASSERT_EQ(stat_after.st_mtime, 0);
}

TEST(UtimensatTest, InvalidNsec) {
  auto f = ASSERT_NO_ERRNO_AND_VALUE(TempPath::CreateFile());
  struct timespec times[2][2] = {{
                                     {0, UTIME_OMIT},               // Valid
                                     {2, static_cast<int64_t>(1e10)}  // Invalid
                                 },
                                 {
                                     {2, static_cast<int64_t>(1e10)},  // Invalid
                                     {0, UTIME_OMIT}                 // Valid
                                 }};

  for (unsigned int i = 0; i < sizeof(times) / sizeof(times[0]); i++) {
    std::cout << "test:" << i << "\n";
    EXPECT_THAT(utimensat(0, f.path().c_str(), times[i], 0),
                SyscallFailsWithErrno(EINVAL));
  }
}

TEST(Utimensat, NullPath) {
  // From man utimensat(2):
  // "the Linux utimensat() system call implements a nonstandard feature: if
  // pathname is NULL, then the call modifies the timestamps of the file
  // referred to by the file descriptor dirfd (which may refer to any type of
  // file).
  // Note, however, that the glibc wrapper for utimensat() disallows
  // passing NULL as the value for file: the wrapper function returns the error
  // EINVAL in this case."
  auto f = ASSERT_NO_ERRNO_AND_VALUE(TempPath::CreateFile());
  const FileDescriptor fd = ASSERT_NO_ERRNO_AND_VALUE(Open(f.path(), O_RDWR));
  struct stat statbuf;
  const struct timespec times[2] = {{1, 0}, {2, 0}};
  // Call syscall directly.
  EXPECT_THAT(syscall(SYS_utimensat, fd.get(), NULL, times, 0),
              SyscallSucceeds());
  EXPECT_THAT(fstatat(0, f.path().c_str(), &statbuf, 0), SyscallSucceeds());
  EXPECT_EQ(1, statbuf.st_atime);
  EXPECT_EQ(2, statbuf.st_mtime);
}

}  // namespace

}  // namespace testing
}  // namespace gvisor
