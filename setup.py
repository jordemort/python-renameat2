from setuptools import setup

setup(
    cffi_modules=["renameat2_build.py:ffibuilder"],
    use_scm_version={"local_scheme": "no-local-version"},
)
