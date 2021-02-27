// SPDX-License-Identifier: MIT
// Copyright (C) 2021 Roland Csaszar
//
// Project:  cppstaticlibrary
// File:     StaticLib.hpp
// Date:     2/27/2021 12:56:50 PM
//==============================================================================

#ifndef HPP_CPPSTATICLIBRARY_STATICLIB_HPP
#define HPP_CPPSTATICLIBRARY_STATICLIB_HPP

#include <string>

/**
 * @brief The namespace everything of this static library is contained in.
 */
namespace CppStaticLibrary
{

/**
 * @brief To test the linking of a static library. Prints some messages to
 * `stdout`.
 */
class StaticLib
{
public:
    /**
     * @brief Constructor. Sets the message to print to the defulat one.
     */
    StaticLib() = default;

    /**
     * @brief Constructor. Sets the message to be printed by `printMessage`.
     * @param message The text to output when `printMessage`is called.
    */
    StaticLib(std::wstring const &message);

    /**
     * @brief Destructor, just prints some message to `stdout`.
     */
    ~StaticLib();

    /**
     * @brief Prints the message set in the constructor to `stdout`.
    */
    void printMessage() const;

protected:
private:
    std::wstring m_message = {L"Linking a static library works!"};
};    // class StaticLib

};    // namespace CppStaticLibrary

#endif    // HPP_CPPSTATICLIBRARY_STATICLIB_HPP
