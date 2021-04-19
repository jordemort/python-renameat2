# python-renameat2

This is a Python wrapper (using [CFFI](https://cffi.readthedocs.io/en/latest/)) around Linux's [renameat2](https://manpages.debian.org/buster/manpages-dev/renameat.2.en.html) system call. With `renameat2`, you can atomically swap two files, choose if existing files are replaced, and create "whiteout" files for overlay filesystems.

## Requirements

This package requires Python 3.6. I tried building it for Python 3.5 and got some syntax errors with the type declarations. I don't care about Python 3.5 personally so I didn't bother fixing it. If you care about Python 3.5 and want to write a patch to make it work there too, I would consider merging it.

This package requires Linux, because `renameat2` is a Linux-specific system call. Your kernel must be version 3.15.0 or newer to use `renameat2`; it does not exist in older kernels. Importing this module will raise a *RuntimeError* if you are not running on Linux or if your kernel is older than 3.15.0.

This package does not have any libc requirements; glibc includes a wrapper for `renameat2` in version 2.28 and newer, but this is significantly newer than the glibc in any of the [manylinux](https://github.com/pypa/manylinux) containers. In order to avoid inflicting any libc requirements on the user, this package brings its own wrapper function that makes the system call directly.

## Status

Stableish? It's just a single system call and I can't imagine doing too much more with the interface. I did use this project to brush about 11 years of dust off of my Python packaging techniques, though, so let me know if you see anything amiss. Pull requests are welcome.

## Links

- [Documentation](https://python-renameat2.readthedocs.io/en/latest/)
- [PyPI](https://pypi.org/project/renameat2/)
- [GitHub repository](https://github.com/jordemort/python-renameat2)

## License

This package is provided under the [MIT License](https://github.com/jordemort/python-renameat2/blob/main/LICENSE).
