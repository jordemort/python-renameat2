ARG ARCH=x86_64
ARG BASE_IMAGE=quay.io/pypa/manylinux2014_${ARCH}:latest

FROM ${BASE_IMAGE}

COPY build-wheel.sh /usr/bin/build-wheel.sh

VOLUME [ "/mnt", "/tmp" ]
WORKDIR /mnt
