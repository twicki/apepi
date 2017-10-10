#!/usr/bin/env bash

module purge
module load craype-haswell
module load craype-network-infiniband
module load mvapich2gdr_gnu/2.1_cuda_7.0
module load GCC/4.9.3-binutils-2.25
module load cray-libsci_acc/3.3.0
module load CMake/3.8.1
#export BOOST_ROOT=/scratch/stefanm/boost_1_62_0/
#export BOOST_INCLUDE=/scratch/stefanm/boost_1_62_0/include/
export CC=`which gcc`
export CXX=`which g++`
