FROM ubuntu:22.04

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y git python3 msitools python3-simplejson python3-six ca-certificates
RUN git clone https://github.com/mstorsjo/msvc-wine.git /msvc-wine
RUN /msvc-wine/vsdownload.py --dest /msvc --accept-license
RUN /msvc-wine/install.sh /msvc

RUN apt-get install -y cmake ninja-build llvm-15 clang-tools-15 lld-15 wget
RUN wget -O llvm.tar.gz https://github.com/llvm/llvm-project/archive/main.tar.gz    # Download as archive because git takes ages
RUN mkdir /llvm
RUN tar -xzf llvm.tar.gz -C /llvm --strip-components=1

ARG PACKAGE_NAME
ARG FULL_PACKAGE_NAME
ARG CC_COMPILER_PACKAGE
ARG CXX_COMPILER_PACKAGE
ARG CC_COMPILER
ARG CXX_COMPILER
ARG TOOLCHAIN_FILE
ARG GIT_REPOSITORY
ARG GIT_TAG

ENV PACKAGE_NAME=$PACKAGE_NAME
ENV FULL_PACKAGE_NAME=$FULL_PACKAGE_NAME
ENV CC_COMPILER_PACKAGE=$CC_COMPILER_PACKAGE
ENV CXX_COMPILER_PACKAGE=$CXX_COMPILER_PACKAGE
ENV CC_COMPILER=$CC_COMPILER
ENV CXX_COMPILER=$CXX_COMPILER
ENV TOOLCHAIN_FILE=$TOOLCHAIN_FILE
ENV GIT_REPOSITORY=$GIT_REPOSITORY
ENV GIT_TAG=$GIT_TAG

ENTRYPOINT [ "/bin/bash", "-c", "cd /repo && python3 -m packages.$PACKAGE_NAME.build" ]