ARG ARCH=x86_64
ARG BASE_IMAGE=quay.io/pypa/manylinux2014_${ARCH}:latest

FROM ${BASE_IMAGE}

# We need newer kernel headers, manylinux comes with 3.10 and we need 3.15
RUN rpm --import https://repo.ius.io/RPM-GPG-KEY-IUS-7 && \
    yum install -y https://repo.ius.io/ius-release-el7.rpm && \
    yum install -y yum-plugin-replace && \
    rpm --import https://www.elrepo.org/RPM-GPG-KEY-elrepo.org && \
    yum install -y https://www.elrepo.org/elrepo-release-7.el7.elrepo.noarch.rpm && \
    yum --enablerepo=elrepo-kernel replace -y kernel-headers --replace-with=kernel-lt-headers && \
    yum clean all

COPY build-wheel.sh /usr/bin/build-wheel.sh

VOLUME [ "/mnt", "/tmp" ]
WORKDIR /mnt
