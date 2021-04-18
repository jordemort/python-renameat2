# python-renameat2

This is a Python wrapper around Linux's [renameat2](https://manpages.debian.org/buster/manpages-dev/renameat.2.en.html) system call. With `renameat2`, you can atomically swap two files, choose if existing files are replaced, and create "whiteout" files for overlay filesystems.

## Status

I consider this feature-complete - it's just a single system call and I can't imagine doing too much more with the interface. Pull requests are welcome, though.

## License

This project is provided under the [MIT License](LICENSE)
