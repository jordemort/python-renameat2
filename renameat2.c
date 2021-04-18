#include <unistd.h>
#include <sys/syscall.h>
#include <linux/fs.h>

/* Newer versions of glibc include this, but none new enough for manylinux */
int renameat2(int olddirfd, const char *oldpath,
              int newdirfd, const char *newpath,
              unsigned int flags)
{
  return syscall(SYS_renameat2, olddirfd, oldpath, newdirfd, newpath, flags);
}
