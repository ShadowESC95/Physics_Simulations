## ------------------------------------------------------------------------
##
## SPDX-License-Identifier: LGPL-2.1-or-later
## Copyright (C) 2012 - 2024 by the deal.II authors
##
## This file is part of the deal.II library.
##
## Part of the source code is dual licensed under Apache-2.0 WITH
## LLVM-exception OR LGPL-2.1-or-later. Detailed license information
## governing the source code and code contributions can be found in
## LICENSE.md and CONTRIBUTING.md at the top level directory of deal.II.
##
## ------------------------------------------------------------------------


########################################################################
##                                                                    ##
##               The deal.II project configuration file               ##
##                                                                    ##
########################################################################

#
# General information
#

set(DEAL_II_PACKAGE_NAME "deal.II")
set(DEAL_II_PACKAGE_VERSION "9.6.2")
set(DEAL_II_PACKAGE_VENDOR "The deal.II Authors <https://www.dealii.org/>")
set(DEAL_II_PACKAGE_DESCRIPTION "Library for solving partial differential equations with the finite element method")

set(DEAL_II_VERSION_MAJOR "9")
set(DEAL_II_VERSION_MINOR "6")
set(DEAL_II_VERSION_SUBMINOR "2")
set(DEAL_II_VERSION "9.6.2")

set(DEAL_II_PROJECT_CONFIG_NAME "deal.II")

set(DEAL_II_BUILD_TYPE "Release")
set(DEAL_II_BUILD_TYPES "RELEASE")

#
# Information about the project location
#

set(DEAL_II_DOCHTML_RELDIR "doc")
set(DEAL_II_DOCREADME_RELDIR "./")
set(DEAL_II_EXAMPLES_RELDIR "examples")
set(DEAL_II_EXECUTABLE_RELDIR "bin")
set(DEAL_II_INCLUDE_RELDIR "include")
set(DEAL_II_LIBRARY_RELDIR "lib")
set(DEAL_II_PROJECT_CONFIG_RELDIR "lib/cmake/deal.II")
set(DEAL_II_SHARE_RELDIR "share/deal.II")

#
# Determine DEAL_II_PATH from CMAKE_CURRENT_LIST_DIR:
#

set(DEAL_II_PATH "${CMAKE_CURRENT_LIST_DIR}")
set(_path "${DEAL_II_PROJECT_CONFIG_RELDIR}")
while(NOT "${_path}" STREQUAL "")
  get_filename_component(DEAL_II_PATH "${DEAL_II_PATH}" PATH)
  get_filename_component(_path "${_path}" PATH)
endwhile()

#
# Print a message after inclusion of this file:
#

set(DEAL_II_PROJECT_CONFIG_INCLUDED TRUE)

set(DEAL_II_BUILD_DIR TRUE)

if(NOT ${DEAL_II_PACKAGE_NAME}_FIND_QUIETLY)
  if(DEAL_II_BUILD_DIR)
    message(STATUS
      "Using the ${DEAL_II_PACKAGE_NAME}-${DEAL_II_PACKAGE_VERSION} build directory found at ${DEAL_II_PATH}"
      )
  else()
    message(STATUS
      "Using the ${DEAL_II_PACKAGE_NAME}-${DEAL_II_PACKAGE_VERSION} installation found at ${DEAL_II_PATH}"
      )
  endif()
endif()

#
# Include all convenience macros:
#

file(GLOB _macro_files
  "${DEAL_II_PATH}/${DEAL_II_SHARE_RELDIR}/macros/*.cmake"
  )
foreach(file ${_macro_files})
  if(NOT ${DEAL_II_PACKAGE_NAME}_FIND_QUIETLY)
    message(STATUS "Include macro ${file}")
  endif()
  include(${file})
endforeach()

#
# Compiler and linker configuration
#

set(DEAL_II_CXX_COMPILER "/usr/bin/c++")
set(DEAL_II_C_COMPILER "/usr/bin/cc")

# used for all targets:
set(DEAL_II_CXX_FLAGS "-fopenmp-simd")

# _additionally_ used for debug targets:
set(DEAL_II_CXX_FLAGS_DEBUG "-Wa,--compress-debug-sections")

# _additionally_ used for release targets:
set(DEAL_II_CXX_FLAGS_RELEASE "-O2 -funroll-loops -funroll-all-loops -fstrict-aliasing -Wno-unused-local-typedefs")

# warning flags used for all targets:
set(DEAL_II_WARNING_FLAGS "-pedantic -Wall -Wextra -Wmissing-braces -Woverloaded-virtual -Wpointer-arith -Wsign-compare -Wsuggest-override -Wswitch -Wsynth -Wwrite-strings -Wno-placement-new -Wno-deprecated-declarations -Wno-literal-suffix -Wno-psabi -Wno-unused-local-typedefs")

# used for all targets:
set(DEAL_II_LINKER_FLAGS "-rdynamic -fuse-ld=gold")

# _additionally_ used for debug targets:
set(DEAL_II_LINKER_FLAGS_DEBUG "-Wl,--compress-debug-sections=zlib")

# _additionally_ used for release targets:
set(DEAL_II_LINKER_FLAGS_RELEASE "")

#
# MPI runtime:
#

set(DEAL_II_MPIEXEC "/usr/bin/mpiexec")
set(DEAL_II_MPIEXEC_NUMPROC_FLAG "-n")
set(DEAL_II_MPIEXEC_PREFLAGS "")
set(DEAL_II_MPIEXEC_POSTFLAGS "")

#
# Information about git revision, library targets and feature configuration
#

set(DEAL_II_GIT_CONFIG "${DEAL_II_PATH}/${DEAL_II_PROJECT_CONFIG_RELDIR}/${DEAL_II_PROJECT_CONFIG_NAME}ConfigGit.cmake")
set(DEAL_II_TARGET_CONFIG "${DEAL_II_PATH}/${DEAL_II_PROJECT_CONFIG_RELDIR}/${DEAL_II_PROJECT_CONFIG_NAME}Targets.cmake")

#
# We support a rather nonstandard situation where the find_package(deal.II)
# call happens before proper setup of a toolchain via project(). The
# reasoning behind this was to properly initialize the compiler in user
# projects via the deal_ii_initialize_cached_variables():
#
#   find_package(deal.II)
#   deal_ii_initialize_cached_variables()
#   project(...)
#   ...
#   deal_ii_setup_target(...)
#
# This requires that the deal_ii_setup_target() loads the target
# configuration because this has to happen after the call to project().
#
# Unfortunately _not_ automatically including all target definitions is
# non-standard behavior and rather surprising. Therefore, in order to
# support the modern way of searching for a dependency and using it:
#
#   project(...)
#   find_package(deal.II)
#   ...
#   target_link_libraries(... dealii::dealii_[debug|release])
#
# we check whether project(... [CXX]) has been called prior to
# find_package(deal.II) and if yes simply include our target configuration:
#
if(DEFINED CMAKE_CXX_COMPILER_ABI)
  include(${DEAL_II_TARGET_CONFIG})
  set(DEAL_II_TARGET_CONFIG_INCLUDED TRUE)
endif()

# The Debug target:
set(DEAL_II_TARGET_DEBUG "")

# The Release target:
set(DEAL_II_TARGET_RELEASE "dealii::dealii_release")

# Full list of targets with "debug" and "optimized" keywords for easy use with TARGET_LINK_LIBRARIES:
set(DEAL_II_TARGET "${DEAL_II_TARGET_RELEASE}")


#
# Feature configuration:
#

set(DEAL_II_WITH_CXX11 ON)
set(DEAL_II_WITH_CXX14 ON)
set(DEAL_II_WITH_CXX17 ON)
set(DEAL_II_WITH_CXX20 FALSE)
set(DEAL_II_WITH_THREADS ON)
set(DEAL_II_WITH_64BIT_INDICES OFF)
set(DEAL_II_WITH_ADOLC ON)
set(DEAL_II_ADOLC_WITH_ADVANCED_BRANCHING FALSE)
set(DEAL_II_ADOLC_WITH_ATRIG_ERF TRUE)
set(DEAL_II_ADOLC_WITH_BOOST_ALLOCATOR TRUE)
set(DEAL_II_ADOLC_WITH_TAPELESS_REFCOUNTING FALSE)
set(DEAL_II_WITH_ARBORX OFF)
set(DEAL_II_WITH_ARPACK ON)
set(DEAL_II_ARPACK_WITH_PARPACK TRUE)
set(DEAL_II_WITH_ASSIMP ON)
set(DEAL_II_WITH_BOOST ON)
set(DEAL_II_BOOST_VERSION "1.74.0")
set(DEAL_II_WITH_CGAL OFF)
set(DEAL_II_WITH_COMPLEX_VALUES ON)
set(DEAL_II_WITH_CUDA OFF)
set(DEAL_II_WITH_GINKGO OFF)
set(DEAL_II_WITH_GMSH ON)
set(DEAL_II_GMSH_WITH_API TRUE)
set(DEAL_II_WITH_GSL ON)
set(DEAL_II_GSL_VERSION "7.1")
set(DEAL_II_WITH_HDF5 ON)
set(DEAL_II_HDF5_VERSION "1.10.7")
set(DEAL_II_WITH_KOKKOS ON)
set(DEAL_II_WITH_LAPACK ON)
set(DEAL_II_LAPACK_WITH_MKL OFF)
set(DEAL_II_WITH_METIS ON)
set(DEAL_II_METIS_VERSION "5.1.0")
set(DEAL_II_WITH_MPI ON)
set(DEAL_II_MPI_VERSION "3.1")
set(DEAL_II_MPI_WITH_DEVICE_SUPPORT OFF)
set(DEAL_II_WITH_MUPARSER ON)
set(DEAL_II_MUPARSER_VERSION "2.2.6")
set(DEAL_II_WITH_OPENCASCADE ON)
set(DEAL_II_OPENCASCADE_VERSION "7.5.1")
set(DEAL_II_WITH_P4EST ON)
set(DEAL_II_P4EST_VERSION "2.2")
set(DEAL_II_P4EST_WITH_SEARCH_LOCAL TRUE)
set(DEAL_II_P4EST_WITH_VTK_BINARY TRUE)
set(DEAL_II_WITH_PETSC ON)
set(DEAL_II_PETSC_VERSION "3.23.4.")
set(DEAL_II_PETSC_WITH_COMPLEX FALSE)
set(DEAL_II_PETSC_WITH_HYPRE FALSE)
set(DEAL_II_PETSC_WITH_KOKKOS FALSE)
set(DEAL_II_PETSC_WITH_MUMPS FALSE)
set(DEAL_II_WITH_SCALAPACK ON)
set(DEAL_II_WITH_SLEPC ON)
set(DEAL_II_SLEPC_VERSION "3.23.2.")
set(DEAL_II_WITH_SUNDIALS ON)
set(DEAL_II_SUNDIALS_VERSION "5.8.0")
set(DEAL_II_SUNDIALS_WITH_IDAS TRUE)
set(DEAL_II_WITH_SYMENGINE OFF)
set(DEAL_II_WITH_TASKFLOW OFF)
set(DEAL_II_WITH_TBB ON)
set(DEAL_II_TBB_VERSION "2020.3")
set(DEAL_II_TBB_WITH_ONEAPI FALSE)
set(DEAL_II_WITH_TRILINOS ON)
set(DEAL_II_TRILINOS_VERSION "13.2")
set(DEAL_II_TRILINOS_WITH_AMESOS2 ON)
set(DEAL_II_TRILINOS_WITH_BELOS ON)
set(DEAL_II_TRILINOS_WITH_EPETRAEXT ON)
set(DEAL_II_TRILINOS_WITH_IFPACK2 ON)
set(DEAL_II_TRILINOS_WITH_KOKKOS ON)
set(DEAL_II_TRILINOS_WITH_MUMPS ON)
set(DEAL_II_TRILINOS_WITH_NOX ON)
set(DEAL_II_TRILINOS_WITH_ROL ON)
set(DEAL_II_TRILINOS_WITH_SACADO ON)
set(DEAL_II_TRILINOS_WITH_ZOLTAN ON)
set(DEAL_II_WITH_UMFPACK ON)
set(DEAL_II_UMFPACK_VERSION "5.7.9")
set(DEAL_II_WITH_VTK OFF)
set(DEAL_II_WITH_ZLIB ON)
set(DEAL_II_ZLIB_VERSION "1.2.11")

