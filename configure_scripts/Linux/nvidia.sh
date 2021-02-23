#!/bin/bash

/opt/nvidia/hpc_sdk/Linux_x86_64/2021/compilers/


PATH=$NVCOMPILERS/$NVARCH/21.2/compilers/bin

OpenMP:

PATH=$NVCOMPILERS/$NVARCH/21.2/comm_libs/mpi/bin

nvc --version

nvc 21.2-0 LLVM 64-bit target on x86-64 Linux -tp haswell 

nvc++ --version

nvc++ 21.2-0 LLVM 64-bit target on x86-64 Linux -tp haswell

nvfortran --version

nvfortran 21.2-0 LLVM 64-bit target on x86-64 Linux -tp haswell

nvcc --version
nvcc: NVIDIA (R) Cuda compiler driver
Copyright (c) 2005-2020 NVIDIA Corporation
Built on Mon_Nov_30_19:08:53_PST_2020
Cuda compilation tools, release 11.2, V11.2.67
Build cuda_11.2.r11.2/compiler.29373293_0


ACHTUNG: Leerzeile!
