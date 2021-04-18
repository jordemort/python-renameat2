from setuptools import setup

# setup.cfg seems to be working but I'm old and still don't trust it
# setup(
#    name="renameat2",
#    version="1.0.0",
#    author="Jordan Webb",
#    author_email="jordan@getseam.com",
#    description="A wrapper around Linux's renameat2 system call",
#    url="https://github.com/jordemort/python-renameat2",
#    packages=["renameat2"],
#    setup_requires=["cffi>=1.0.0"],
#    cffi_modules=["renameat2_build.py:ffibuilder"],
#    python_requires=">=3.6",
# )

setup(cffi_modules=["renameat2_build.py:ffibuilder"])
