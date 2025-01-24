# Use an official SBCL image as the base
FROM ubuntu:latest

# Set the working directory
WORKDIR /usr/src/app

ARG BOX2D_PATH=/Users/diedrich/Software/box2d

# Install dependencies
RUN apt-get update && \
    apt-get install -y \
    build-essential \
    wget 

RUN apt-get install -y \
    openssl \
    libssl-dev \
    libtool \
    autoconf \
    unzip 

RUN wget https://cmake.org/files/v3.31/cmake-3.31.4.tar.gz
RUN tar -xzvf cmake-3.31.4.tar.gz
RUN cd cmake-3.31.4 && \
    ./bootstrap && \
    make && \
    make install

#Install git
RUN apt-get install -y git
RUN apt-get install -y xorg-dev
RUN apt-get install -y g++

RUN apt-get update && \
    apt-get install -y \
    build-essential \
    wget 

# Ugly: 
RUN wget https://github.com/erincatto/box2d/archive/refs/tags/v3.0.0.tar.gz
RUN tar -xzvf v3.0.0.tar.gz
# HOTFIX 1: Fix the CMakeLists.txt file to not build the samples
RUN sed -i 's/option(BOX2D_SAMPLES "Build the Box2D samples" ON)/option(BOX2D_SAMPLES "Build the Box2D samples" OFF)/g' /usr/src/app/box2d-3.0.0/CMakeLists.txt
RUN cd  /usr/src/app/box2d-3.0.0 && \
    ./build.sh


RUN apt install -y sbcl clang
    
RUN git clone https://gitlab.isp.uni-luebeck.de/hai/geomates.git
RUN cd geomates && \
    clang -I ../box2d-3.0.0/include -pedantic -Wall -fPIC -shared -Wl,--no-undefined -lm -o wrapper.so wrapper.c ../box2d-3.0.0/build/src/libbox2d.a

# HOTFIX 2:
RUN sed -i  's/#(127 0 0 1)/#(0 0 0 0)/g' /usr/src/app/geomates/geomates.lisp

EXPOSE 8000

WORKDIR /usr/src/app/geomates