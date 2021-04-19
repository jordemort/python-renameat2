"""renameat2 is a wrapper around Linux's `renameat2` system call.

The most likely reason you might want to use renameat2 is to atomically swap
two files; the :func:`exchange` function is for you.

If you just want to rename things with more control than :py:func:`os.rename`,
and/or possibly do some weird overlayfs stuff, check out :func:`rename`.

Finally, if you really just like the interface of renameat2 as it's implemented
in the system call, :func:`renameat2` recreates it in Python.
"""

import errno
import os

from contextlib import contextmanager
from enum import IntFlag
from pathlib import Path
from typing import Union

from ._renameat2 import lib as _lib, ffi as _ffi


def _check_kernel_version():
    uname = os.uname()

    if uname.sysname != "Linux":
        raise RuntimeError("renameat2 is Linux-specific")

    kernelver = uname.release.split(".")

    if int(kernelver[0]) < 3:
        raise RuntimeError("Kernel 3.15 is required to use renameat2")
    elif int(kernelver[0]) == 3 and int(kernelver[1]) < 15:
        raise RuntimeError("Kernel 3.15 is required to use renameat2")


_check_kernel_version()


class Flags(IntFlag):
    RENAME_EXCHANGE = 2
    """
    Atomically exchange oldpath and newpath. Both pathnames must exist but may be of
    different types (e.g., one could be a non-empty directory and the other a symbolic
    link).

    RENAME_EXCHANGE can't be used in combination with RENAME_NOREPLACE or
    RENAME_WHITEOUT.
    """

    RENAME_NOREPLACE = 1
    """
    Don't overwrite newpath of the rename. Return an error if newpath already exists.

    RENAME_NOREPLACE requires support from the underlying filesystem. See the
    renameat(2) manpage for more information.
    """

    RENAME_WHITEOUT = 4
    """
    Specifying RENAME_WHITEOUT creates a "whiteout" object at the source of the rename
    at the same time as performing the rename. The whole operation is atomic, so that
    if the rename succeeds then the whiteout will also have been created.

    This operation makes sense only for overlay/union filesystem implementations.

    See the renameat(2) man page for more information.
    """


def renameat2(
    olddirfd: int, oldpath: str, newdirfd: int, newpath: str, flags: Flags = Flags(0)
) -> None:
    """A thin wrapper around the renameat2 C library function.

    Most people will likely prefer the more Pythonic interfaces provided
    by the :func:`rename` or :func:`exchange` wrapper functions; this one is
    for people who prefer their C library bindings without any sugar.

    :param olddirfd: A directory file descriptor
    :type olddirfd: int
    :param oldpath: The name of a file in the directory represented by olddirfd
    :type oldpath: str
    :param newdirfd: A directory file descriptor
    :type newdirfd: int
    :param newpath: The name of a file in the in the directory represented by newdirfd
    :type newpath: str
    :param flags: A bit mask consisting of zero or more of :data:`RENAME_EXCHANGE`,
        :data:`RENAME_NOREPLACE`, or :data:`RENAME_WHITEOUT`.
    :type flags: int

    :raises OSError: if the system call fails
    """
    err: int = _lib.renameat2(  # type: ignore
        olddirfd, oldpath.encode(), newdirfd, newpath.encode(), flags
    )

    if err != 0:
        raise OSError(
            _ffi.errno, f"renameat2: {errno.errorcode[_ffi.errno]}"  # type: ignore
        )


@contextmanager
def _split_dirfd(path: Union[Path, str]):
    path = Path(path)
    fd = os.open(path.parent, os.O_PATH | os.O_DIRECTORY | os.O_CLOEXEC)
    try:
        yield (fd, path.name)
    finally:
        os.close(fd)


def rename(
    oldpath: Union[Path, str],
    newpath: Union[Path, str],
    replace: bool = True,
    whiteout: bool = False,
) -> None:
    """Rename a file using the renameat2 system call.

    :param oldpath: Path to the file to rename
    :type oldpath: Union[pathlib.Path, str]
    :param newpath: Path to rename the file to
    :type newpath: Union[pathlib.Path, str]
    :param replace: If true, any existing file at newpath will be replaced.
      If false, any existing file at newpath will cause an error to be raised.
      False corresponds to passing RENAME_NOREPLACE to the system call.
    :type replace: bool
    :param whiteout: If true, a "whiteout" file will be left behind at oldpath.
      True corresponds to passing RENAME_WHITEOUT to the system call.
    :type whiteout: bool

    :raises OSError: if the system call fails
    """
    flags = 0
    if not replace:
        flags |= Flags.RENAME_NOREPLACE

    if whiteout:
        flags |= Flags.RENAME_WHITEOUT

    with _split_dirfd(oldpath) as (dirfd_a, name_a):
        with _split_dirfd(newpath) as (dirfd_b, name_b):
            renameat2(dirfd_a, name_a, dirfd_b, name_b, flags)


def exchange(a: Union[Path, str], b: Union[Path, str]) -> None:
    """Atomically swap two files.

    This is probably the main attraction of this module.

    After this call, the file originally referred to by the first path
    will be referred to by the second, and the file originally referred
    to by the second path will be referred to by the first.

    This is an atomic operation; that is to say, there is no possible
    intermediate state where the files could be "partially" swapped;
    either the call succeeds and the files are exchanged, or the call
    fails and the files are not exchanged.

    This function is implemented by passing RENAME_EXCHANGE to the system call.

    :param a: Path to a file
    :type a: Union[pathlib.Path, str]
    :param b: Path to a file
    :type b: Union[pathlib.Path, str]

    :raises OSError: if `a` and `b` cannot be swapped
    """
    with _split_dirfd(a) as (dirfd_a, name_a):
        with _split_dirfd(b) as (dirfd_b, name_b):
            renameat2(dirfd_a, name_a, dirfd_b, name_b, Flags.RENAME_EXCHANGE)
