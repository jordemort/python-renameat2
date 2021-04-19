#include <unistd.h>
#include <sys/syscall.h>
#include <linux/fs.h>

#ifndef SYS_renameat2
#  ifdef __x86_64__
#    define SYS_renameat2 316
#  endif
#  ifdef __i386__
#    define SYS_renameat2 353
#  endif
#  ifdef __aarch64__
#    define SYS_renameat2 276
#  endif
#  ifdef __arm__
#    define SYS_renameat2 382
#  endif
#endif

#ifndef SYS_renameat2
#  error SYS_renameat2 is not defined
#endif

/* Newer versions of glibc include this, but none new enough for manylinux */
int renameat2(int olddirfd, const char *oldpath,
              int newdirfd, const char *newpath,
              unsigned int flags)
{
  return syscall(SYS_renameat2, olddirfd, oldpath, newdirfd, newpath, flags);
}
