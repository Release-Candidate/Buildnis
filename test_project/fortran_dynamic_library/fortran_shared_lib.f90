! SPDX-License-Identifier: MIT
! Copyright (C) 2021 Roland Csaszar
!
! Project:  fortran_dynamic_library
! File:     fortran_shared_lib.f90
! Date:     2/27/2021
!===============================================================================

! Use this to export `fortran_dynamic_library` from a DLL!

! Module to test the linking to a shared library.
module fortran_shared_lib

    implicit none

    ! @brief Class to test the linking of a shared library.
    type, public :: SharedLib

        private
        ! @brief Message to display when `printMessage` is called.
        character(len=70) :: message = 'Linking a shared library works!'

    contains

        ! @brief Print the text set with the constructor to `stdout`.
        !
        ! @param this (StaticLib): the class' instance
        procedure :: printMessage => printMessageImp

        ! @brief Destructor. Prints a message to `stdout`.
        final :: destructor

    end type SharedLib

    contains
!DEC$ IF DEFINED (_WIN32)
!DEC$ ATTRIBUTES DLLEXPORT :: printMessageImp
!DEC$ END IF
    ! @brief Print the text set with the constructor to `stdout`.
    !
    ! @param this (StaticLib): the class' instance
    subroutine printMessageImp(this)

        class(SharedLib), intent(in) :: this

        print *, this%message

    end subroutine printMessageImp

!DEC$ IF DEFINED (_WIN32)
!DEC$ ATTRIBUTES DLLEXPORT :: destructor
!DEC$ END IF
    ! @brief Destructor. Prints a message to `stdout`.
    !
    ! @param this (SharedLib): the class' instance to delete.
    subroutine destructor(this)

        type(SharedLib), intent(inout) :: this

        print *, 'In the destructor of SharedLib!'

    end subroutine destructor

end module fortran_shared_lib

