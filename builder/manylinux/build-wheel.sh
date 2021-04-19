#!/usr/bin/env bash
# Adapted from https://github.com/pypa/python-manylinux-demo/blob/master/travis/build-wheels.sh

set -euo pipefail

WHICH_PYTHON=${WHICH_PYTHON:-cp36-cp36m}

function repair_wheel {
  wheel="$1"
  if ! auditwheel show "$wheel"; then
    echo "Skipping non-platform wheel $wheel"
  else
    auditwheel repair "$wheel" --plat "$PLAT" -w /build/fixedwheel/
  fi
}

mkdir -p /build/sdist /build/source /build/wheel /build/fixedwheel

# Build and extract sdist
/opt/python/cp36-cp36m/bin/python3 setup.py sdist -d /build/sdist

find /build

sdist=$(find /build/sdist -name '*.tar.gz' | head -n1)

if [ -z "$sdist" ] ; then
  echo "couldn't find sdist!" >&2
  exit 1
fi

tar -C /build/source -xvf "$sdist"

# Install development requirements
"/opt/python/${WHICH_PYTHON}/bin/pip3" install -r /mnt/requirements-dev.txt

# Compile wheel
"/opt/python/${WHICH_PYTHON}/bin/pip3" wheel /build/source/"$(basename "$sdist" .tar.gz)" --no-deps -w /build/wheel

# Bundle external shared libraries into the wheels
for whl in /build/wheel/*.whl; do
    repair_wheel "$whl"
done

# Install packages and test
cp /mnt/renameat2_test.py /bin/renameat2_test.py
"/opt/python/${WHICH_PYTHON}/bin/pip3" install renameat2 --no-index -f /build/fixedwheel
cd / && "/opt/python/${WHICH_PYTHON}/bin/python3" -m pytest /bin/renameat2_test.py

mnt_uid=$(stat -c '%u' /mnt)
mnt_gid=$(stat -c '%g' /mnt)

# Copy tested wheel over to dist
mkdir -p /mnt/dist
cp /build/fixedwheel/*.whl /mnt/dist
chown -R "$mnt_uid:$mnt_gid" /mnt/dist
