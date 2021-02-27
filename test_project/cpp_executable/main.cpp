// SPDX-License-Identifier: MIT
// Copyright (C) 2021 Roland Csaszar
//
// Project:  cppexecutable
// File:     main.cpp
// Date:     2/27/2021 12:54:40 AM
//==============================================================================

#include <cstdlib>
#include <memory>
#include <SharedLib.hpp>
#include <StaticLib.hpp>

//==============================================================================
// Windows: set the link option /entry:mainCRTStartup if using GUI
// Visual Studio: 'Linker'->'Advanced' 'Entry Point'
/**
 * @brief The program's main entry point, `main`
 * @param[in] argc number of arguments passed to the program
 * @param[in] argv the arguments, in an array
 * @return EXIT_SUCCESS if no error occurred
 *         EXIT_FAILURE if an error occurred
 */
int wmain(int argc, wchar_t *argv[])
{
    auto test_shared = std::make_unique<CppDynamicLibrary::SharedLib>(
        L"Linking a shared library works!");

    test_shared->printMessage();

    auto test_static = std::make_unique<CppStaticLibrary::StaticLib>(
        L"Linking a static library works!");

    test_static->printMessage();

    return EXIT_SUCCESS;
}
