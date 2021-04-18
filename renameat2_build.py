from cffi import FFI

ffibuilder = FFI()

ffibuilder.cdef(  # type: ignore
    """
    #define RENAME_EXCHANGE ...
    #define RENAME_NOREPLACE ...
    #define RENAME_WHITEOUT ...

    int renameat2(int olddirfd, const char *oldpath,
                int newdirfd, const char *newpath,
                unsigned int flags);
    """
)

ffibuilder.set_source(  # type: ignore
    "renameat2._renameat2", "", sources=["renameat2.c"]
)

if __name__ == "__main__":
    ffibuilder.compile(verbose=True)  # type: ignore
