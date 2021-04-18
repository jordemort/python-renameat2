#!/usr/bin/env bash
# Adapted from https://github.com/pypa/python-manylinux-demo/blob/master/travis/build-wheels.sh

set -euo pipefail

WHICH_PYTHON=${WHICH_PYTHON:-cp36-cp36m}

function repair_wheel {
    wheel="$1"
    if ! auditwheel show "$wheel"; then
        echo "Skipping non-platform wheel $wheel"
    else
        auditwheel repair "$wheel" --plat "$PLAT" -w /wheelhouse/
    fi
}

mkdir -p /wheelhouse /tmp/wheelhouse

"/opt/python/${WHICH_PYTHON}/bin/pip" install -r /mnt/requirements-dev.txt

# Compile wheel
"/opt/python/${WHICH_PYTHON}/bin/pip" wheel /mnt/ --no-deps -w /tmp/wheelhouse

# Bundle external shared libraries into the wheels
for whl in /tmp/wheelhouse/*.whl; do
    repair_wheel "$whl"
done

# Install packages and test
cp /mnt/renameat2_test.py /bin/renameat2_test.py
"/opt/python/${WHICH_PYTHON}/bin/pip" install renameat2 --no-index -f /wheelhouse
"/opt/python/${WHICH_PYTHON}/bin/python3" -m pytest /bin/renameat2_test.py
