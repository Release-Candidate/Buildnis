! SPDX-License-Identifier: MIT
! Copyright (C) 2021 Roland Csaszar
!
! Project:  fortran_static_library
! File:     fortran_static_lib.f90
! Date:     2/27/2021
!===============================================================================

! Module to test the linking to a static library.
module fortran_static_library

     implicit none

    ! @brief Class to test the linking of a static library.
    type, public :: StaticLib

        private
        ! @brief Message to display when `printMessage` is called.
        character(len=70) :: message = 'Linking a static library works!'

    contains

        ! @brief Print the text set with the constructor to `stdout`.
        procedure :: printMessage => printMessageImp

        ! @brief Destructor. Prints a message to `stdout`.
        final :: destructor

    end type StaticLib

    interface StaticLib

        ! @brief Constructor. Prints a message to `stdout`.
        !
        ! @param text (character(len=70)): The text to display if `printMessage` is called.
        procedure newStaticLib

    end interface StaticLib


    contains

    ! @brief Print the text set with the constructor to `stdout`.
    !
    ! @param this (StaticLib): the class' instance
    subroutine printMessageImp(this)

        class(StaticLib), intent(in) :: this

        print *, this%message

    end subroutine printMessageImp

    ! @brief Destructor. Prints a message to `stdout`.
    !
    ! @param this (StaticLib): the class' instance to delete.
    subroutine destructor(this)

        type(StaticLib), intent(inout) :: this

        print *, 'In the destructor of StaticLib! This is just to have some code in here!'

    end subroutine destructor

    ! @brief Constructor. Prints a message to `stdout`.
    !
    ! @param text (character(len=70)): The text to display if `printMessage` is called.
    function newStaticLib(text) result(ret_val)

        character(len=70), intent(in) :: text
        type(StaticLib) :: ret_val

        print *, 'In the constructor of StaticLib. This is just to have some code in here!'

        ret_val%message = text

    end function newStaticLib

end module fortran_static_library
