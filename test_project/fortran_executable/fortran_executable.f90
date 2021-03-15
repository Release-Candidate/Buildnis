! SPDX-License-Identifier: MIT
! Copyright (C) 2021 Roland Csaszar
!
! Project:  fortran_executable
! File:     fortran_executable.f90
! Date:     2/27/2021
!===============================================================================

!DEC$ IF DEFINED (_WIN32)
!DEC$ ATTRIBUTES DLLIMPORT :: printMessage
!DEC$ ATTRIBUTES DLLIMPORT :: destructor
!DEC$ END IF


program fortran_executable

    use fortran_shared_lib
    use fortran_static_library

    implicit none

    character(len=70), parameter :: tmp_text = 'Calling a member from a static library works a second time!'
    type(SharedLib) :: test_shared
    type(StaticLib) :: test_static

    !===========================================================================

    call test_shared%printMessage

    call test_static%printMessage

    test_static = StaticLib(tmp_text)

    call test_static%printMessage

end program fortran_executable
