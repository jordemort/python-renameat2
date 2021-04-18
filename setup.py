from setuptools import setup

setup(
    name="renameat2",
    version="1.0.0",
    author="Jordan Webb",
    author_email="jordan@getseam.com",
    description="A wrapper around Linux's renameat2 system call",
    url="https://github.com/jordemort/python-renameat2",
    packages=["renameat2"],
    setup_requires=["cffi>=1.0.0"],
    cffi_modules=["renameat2_build.py:ffibuilder"],
    install_requires=["cffi>=1.0.0"],
)
