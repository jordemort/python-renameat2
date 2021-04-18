"""A wrapper around Linux's `renameat2` system call
"""
import errno
import os

from contextlib import contextmanager
from enum import IntFlag
from pathlib import Path
from typing import Union

from _renameat2 import lib as _lib, ffi as _ffi


class Flags(IntFlag):
    RENAME_EXCHANGE: int = _lib.RENAME_EXCHANGE  # type: ignore
    """
    Atomically exchange oldpath and newpath. Both pathnames must exist but may be of
    different types (e.g., one could be a non-empty directory and the other a symbolic
    link).

    RENAME_NOEXCHANGE can't be used in combination with RENAME_NOREPLACE or
    RENAME_WHITEOUT.
    """

    RENAME_NOREPLACE: int = _lib.RENAME_NOREPLACE  # type: ignore
    """
    Don't overwrite newpath of the rename. Return an error if newpath already exists.

    RENAME_NOREPLACE requires support from the underlying filesystem. See the
    renameat(2) manpage for more information.
    """

    RENAME_WHITEOUT: int = _lib.RENAME_WHITEOUT  # type: ignore
    """
    Specifying RENAME_WHITEOUT creates a "whiteout" object at the source of the rename
    at the same time as performing the rename. The whole operation is atomic, so that
    if the rename succeeds then the whiteout will also have been created.

    This operation makes sense only for overlay/union filesystem implementations.

    See the renameat(2) man page for more information.
    """


def renameat2(
    olddirfd: int, oldpath: str, newdirfd: int, newpath: str, flags: int = 0
) -> None:
    """A thin wrapper around the renameat2 C library function.

    Most people will likely prefer the more Pythonic interfaces provided
    by the :func:`rename` or :func:`exchange` wrapper functions; this one is
    for people who prefer their C library bindings without any sugar.

    :param olddirfd: A directory file descriptor
    :type olddirfd: int
    :param oldpath: The name of a file in the directory represented by olddirfd
    :type oldpath: bytes
    :param newdirfd: A directory file descriptor
    :type newdirfd: int
    :param newpath: The name of a file in the in the directory represented by newdirfd
    :type newpath: bytes
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
    """Rename a file.

    If you don't need the functionality provided by :data:`RENAME_NOREPLACE`
    or :data:`RENAME_WHITEOUT` then you might be better off just using
    :obj:`os.rename`.

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

    :param a: Path to a file
    :type a: Union[path_lib.Path, str]
    :param b: Path to a file
    :type b: Union[path_lib.Path, str]

    :raises OSError: if `a` and `b` cannot be swapped
    """
    with _split_dirfd(a) as (dirfd_a, name_a):
        with _split_dirfd(b) as (dirfd_b, name_b):
            renameat2(dirfd_a, name_a, dirfd_b, name_b, Flags.RENAME_EXCHANGE)
