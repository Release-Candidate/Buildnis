#!/bin/bash

#/opt/AMD/aocc-compiler-2.3.0/setenv_AOCC.sh 
ENV_SCRIPT=$(find /opt/AMD/aocc-* -name "setenv*")

clang  --version
#AMD clang version 11.0.0 (CLANG: AOCC_2.3.0-Build#85 2020_11_10) (based on LLVM Mirror.Version.11.0.0)
clang  --version| grep "^.* (CL"

clang++ --version
AMD clang version 11.0.0 (CLANG: AOCC_2.3.0-Build#85 2020_11_10) (based on LLVM Mirror.Version.11.0.0

flang --version
AMD clang version 11.0.0 (CLANG: AOCC_2.3.0-Build#85 2020_11_10)



