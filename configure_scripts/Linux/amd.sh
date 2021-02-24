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

echo "{"
echo '    "build_tools":'
echo "    ["
echo "         {"
echo "            \"name\": \"AMD AOCC\","
echo "            \"name_long\": \"${CLANG_VERSION}\","
echo "            \"version\": \"\","
echo "            \"version_arg\": \"--version\","
echo "            \"version_regex\": \"version (.*) \\\\(\","
echo "            \"build_tool_exe\": \"clang\","
echo "            \"install_path\": \"${CLANG_PATH}\","
echo "            \"env_script\": \"\""
echo "         },"
echo "         {"
echo "            \"name\": \"Clang++\","
echo "            \"name_long\": \"${CLANGPP_VERSION}\","
echo "            \"version\": \"\","
echo "            \"version_arg\": \"--version\","
echo "            \"version_regex\": \"version (.*) \\\\(\","
echo "            \"build_tool_exe\": \"clang++\","
echo "            \"install_path\": \"${CLANGPP_PATH}\","
echo "            \"env_script\": \"\""
echo "         }"
echo "    ]"
echo "}"