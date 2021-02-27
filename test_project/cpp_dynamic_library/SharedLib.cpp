// SPDX-License-Identifier: MIT
// Copyright (C) 2021 Roland Csaszar
//
// Project:  cppdynamiclibrary
// File:     SharedLib.cpp
// Date:     2/27/2021 12:31:43 AM
//==============================================================================

#define IN_CPPDYNAMICLIBRARY_SHAREDLIB 1

#include <iostream>

#include "SharedLib.hpp"

namespace CppDynamicLibrary
{

//==============================================================================
SharedLib::SharedLib(std::wstring const &message) : m_message(message)
{
    std::wcout << "In the constructor of SharedLib! This is just to have some "
                  "code in the body of this constructor!"
               << std::endl;
}

//==============================================================================
SharedLib::~SharedLib()
{
    std::wcout << "In the destructor of SharedLib! This is just to have some "
                  "code in the body of this destructor!"
               << std::endl;
}

//==============================================================================
void SharedLib::printMessage() const
{
    std::wcout << m_message << std::endl;
}

};    // namespace CppDynamicLibrary
