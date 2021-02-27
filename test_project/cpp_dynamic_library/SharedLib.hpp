// SPDX-License-Identifier: MIT
// Copyright (C) 2021 Roland Csaszar
//
// Project:  cppdynamiclibrary
// File:     SharedLib.hpp
// Date:     2/27/2021 12:16:07 AM
//==============================================================================

#ifndef HPP_CPPDYNAMICLIBRARY_SHAREDLIB_HPP
#define HPP_CPPDYNAMICLIBRARY_SHAREDLIB_HPP

#ifdef _WIN32
#    ifdef IN_CPPDYNAMICLIBRARY_SHAREDLIB
#        define DLL_INTERFACE __declspec(dllexport)
#    else
#        define DLL_INTERFACE __declspec(dllimport)
#    endif
#else
#    define DLL_INTERFACE
#endif

#include <string>

/**
 * @brief Everything in this shared library is contained in the namespace
 *        `CppDynamicLibrary`.
 */
namespace CppDynamicLibrary
{

/**
 * @brief Prints some messages to `stdout` when  constructed or destructed or
 * the method is called. This is only to test the usage of a class in a shared
 * library.
 */
class DLL_INTERFACE SharedLib
{
public:
    /**
     * @brief Constructor. Sets the text to print to stdout to `message`.
     * @param message  the text to print to stdout if `printMessage` is called.
     */
    explicit SharedLib(std::wstring const &message);

    /**
     * @brief Constructor. Sets the message to print to the default one.
     */
    SharedLib() = default;

    /**
     * @brief Destructor.
     */
    ~SharedLib();

    /**
     * @brief Prints the message set in the constructor to stdout.
    */
    void printMessage() const;

protected:
private:
    /**
     * @brief The message to print to stdout.
    */
    std::wstring m_message = {L"Linking and using a shared library works!"};
};    // class SharedLib

};    // namespace CppDynamicLibrary

#endif    // HPP_CPPDYNAMICLIBRARY_SHAREDLIB_HPP
