#!/usr/bin/env bash
# Adapted from https://github.com/pypa/python-manylinux-demo/blob/master/travis/build-wheels.sh
set -euo pipefail

WHICH_PYTHON=${WHICH_PYTHON:-cp36-cp36m}

# bash stacktrace from https://gist.github.com/ahendrix/7030300

function errexit() {
  local err=$?
  set +o xtrace
  local code="${1:-1}"
  echo "Error in ${BASH_SOURCE[1]}:${BASH_LINENO[0]}. '${BASH_COMMAND}' exited with status $err"
  # Print out the stack trace described by $function_stack
  if [ ${#FUNCNAME[@]} -gt 2 ]; then
    echo "Call tree:"
    for ((i = 1; i < ${#FUNCNAME[@]} - 1; i++)); do
      echo " $i: ${BASH_SOURCE[$i + 1]}:${BASH_LINENO[$i]} ${FUNCNAME[$i]}(...)"
    done
  fi
  echo "Exiting with status ${code}"
  exit "${code}"
}

# trap ERR to provide an error handler whenever a command exits nonzero
#  this is a more verbose version of set -o errexit
trap 'errexit' ERR
# setting errtrace allows our ERR trap handler to be propagated to functions,
#  expansions and subshells
set -o errtrace

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
echo "::group::Build and extract sdist"
/opt/python/cp36-cp36m/bin/python3 setup.py sdist -d /build/sdist

find /build

sdist=$(find /build/sdist -name '*.tar.gz' | head -n1)

if [ -z "$sdist" ] ; then
  echo "couldn't find sdist!" >&2
  exit 1
fi

tar -C /build/source -xvf "$sdist"
echo "::endgroup::"

# Install development requirements
echo "::group::Install requirements-dev.txt"
"/opt/python/${WHICH_PYTHON}/bin/pip3" install -r /mnt/requirements-dev.txt
echo "::endgroup::"

# Compile wheel
echo "::group::Build wheel"
"/opt/python/${WHICH_PYTHON}/bin/pip3" wheel /build/source/"$(basename "$sdist" .tar.gz)" --no-deps -w /build/wheel
echo "::endgroup::"

# Bundle external shared libraries into the wheels
echo "::group::Repair wheel"
for whl in /build/wheel/*.whl; do
  repair_wheel "$whl"
done
echo "::endgroup::"

# Install packages and test
echo "::group::Install package"
"/opt/python/${WHICH_PYTHON}/bin/pip3" install renameat2 --no-index -f /build/fixedwheel
echo "::endgroup::"

echo "::group::Run tests"
cp /mnt/renameat2_test.py /bin/renameat2_test.py
cd / && "/opt/python/${WHICH_PYTHON}/bin/python3" -m pytest /bin/renameat2_test.py
echo "::endgroup::"

# Copy tested wheel over to dist
mnt_uid=$(stat -c '%u' /mnt)
mnt_gid=$(stat -c '%g' /mnt)

mkdir -p /mnt/dist
cp -v /build/fixedwheel/*.whl /mnt/dist
chown -R "$mnt_uid:$mnt_gid" /mnt/dist
