// SPDX-License-Identifier: MIT
// Copyright (C) 2021 Roland Csaszar
//
// Project:  cppstaticlibrary
// File:     StaticLib.cpp
// Date:     2/27/2021 1:09:54 PM
//==============================================================================

#include "StaticLib.hpp"

#include <iostream>

namespace CppStaticLibrary
{

//==============================================================================
StaticLib::StaticLib(std::wstring const &message) : m_message(message)
{
    std::wcout << "In the constructor of StaticLib. This is just to have some "
                  "code in here!"
               << std::endl;
}

//==============================================================================
StaticLib::~StaticLib()
{
    std::wcout << "In the destructor of StaticLib. This is just to have some "
                  "code in here!"
               << std::endl;
}

//==============================================================================
void StaticLib::printMessage() const
{
    std::wcout << m_message << std::endl;
}

};    // namespace CppStaticLibrary
