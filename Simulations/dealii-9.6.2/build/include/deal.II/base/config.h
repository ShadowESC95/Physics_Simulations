// ------------------------------------------------------------------------
//
// SPDX-License-Identifier: LGPL-2.1-or-later
// Copyright (C) 2012 - 2024 by the deal.II authors
//
// This file is part of the deal.II library.
//
// Part of the source code is dual licensed under Apache-2.0 WITH
// LLVM-exception OR LGPL-2.1-or-later. Detailed license information
// governing the source code and code contributions can be found in
// LICENSE.md and CONTRIBUTING.md at the top level directory of deal.II.
//
// ------------------------------------------------------------------------

#ifndef dealii_config_h
#define dealii_config_h


/***********************************************************************
 * Information about deal.II:
 */

#define DEAL_II_PACKAGE_NAME "deal.II"

#define DEAL_II_PACKAGE_VERSION "9.6.2"

#define DEAL_II_VERSION_MAJOR 9
#define DEAL_II_VERSION_MINOR 6
#define DEAL_II_VERSION_SUBMINOR 2


/***********************************************************************
 * Configured deal.II features:
 */

/* #undef DEAL_II_WITH_64BIT_INDICES */
#define DEAL_II_WITH_ADOLC
#define DEAL_II_WITH_ARPACK
/* #undef DEAL_II_WITH_ARBORX */
#define DEAL_II_WITH_ASSIMP
/* #undef DEAL_II_FEATURE_BOOST_BUNDLED_CONFIGURED */
/* #undef DEAL_II_WITH_CGAL */
#define DEAL_II_WITH_COMPLEX_VALUES
/* #undef DEAL_II_WITH_CUDA */
/* #undef DEAL_II_WITH_GINKGO */
#define DEAL_II_WITH_GMSH
#define DEAL_II_WITH_GSL
#define DEAL_II_WITH_HDF5
#define DEAL_II_WITH_KOKKOS
/* #undef DEAL_II_FEATURE_KOKKOS_BUNDLED_CONFIGURED */
#define DEAL_II_WITH_LAPACK
/* #undef LAPACK_WITH_64BIT_BLAS_INDICES */
/* #undef DEAL_II_LAPACK_WITH_MKL */
#define DEAL_II_WITH_METIS
#define DEAL_II_WITH_MPI
#define DEAL_II_WITH_MUPARSER
/* #undef DEAL_II_FEATURE_MUPARSER_BUNDLED_CONFIGURED */
#define DEAL_II_WITH_OPENCASCADE
#define DEAL_II_WITH_P4EST
#define DEAL_II_WITH_PETSC
#define DEAL_II_WITH_SCALAPACK
#define DEAL_II_WITH_SLEPC
#define DEAL_II_WITH_SUNDIALS
/* #undef DEAL_II_WITH_SYMENGINE */
/* #undef DEAL_II_WITH_TASKFLOW */
/* #undef DEAL_II_FEATURE_TASKFLOW_BUNDLED_CONFIGURED */
#define DEAL_II_WITH_TBB
/* #undef DEAL_II_FEATURE_TBB_BUNDLED_CONFIGURED */
#define DEAL_II_WITH_TRILINOS
#define DEAL_II_WITH_UMFPACK
/* #undef DEAL_II_FEATURE_UMFPACK_BUNDLED_CONFIGURED */
#define DEAL_II_USE_VECTORIZATION_GATHER
/* #undef DEAL_II_WITH_VTK */
#define DEAL_II_WITH_ZLIB

#ifdef DEAL_II_WITH_TBB
/**
 * For backwards compatibility, continue defining DEAL_II_WITH_THREADS when the
 * library is configured with TBB.
 */
#define DEAL_II_WITH_THREADS

#define TBB_SUPPRESS_DEPRECATED_MESSAGES 1

/* #undef DEAL_II_TBB_WITH_ONEAPI */

#endif

/***********************************************************************
 * Compiler bugs:
 *
 * For documentation see cmake/checks/check_03_compiler_bugs.cmake
 */

/* #undef DEAL_II_DELETED_MOVE_CONSTRUCTOR_BUG */

/***********************************************************************
 * Compiler features:
 *
 * For documentation see cmake/checks/check_01_compiler_features.cmake
 */

#define DEAL_II_COMPILER_USE_VECTOR_ARITHMETICS
/* #undef DEAL_II_VECTOR_ITERATOR_IS_POINTER */
#define DEAL_II_HAVE_BUILTIN_EXPECT
#define DEAL_II_HAVE_GLIBC_STACKTRACE
#define DEAL_II_HAVE_LIBSTDCXX_DEMANGLER
/* #undef __PRETTY_FUNCTION__ */
#define DEAL_II_ALWAYS_INLINE __attribute__((always_inline))
#define DEAL_II_RESTRICT __restrict
#define DEAL_II_COMPILER_HAS_DIAGNOSTIC_PRAGMA

/***********************************************************************
 * CPU features:
 *
 * For documentation see cmake/checks/check_01_cpu_features.cmake
 */

/* #undef DEAL_II_WORDS_BIGENDIAN */

/*
 * This sets the largest number of vectorization bits detected for the given
 * compiler flags and hardware (e.g. 256 for AVX on x86-64 architectures) for
 * use in deal.II's intrinsics-based VectorizedArray class.
 */
#define DEAL_II_VECTORIZATION_WIDTH_IN_BITS 128

/*
 * Backward compatibility setting
 */
#if DEAL_II_VECTORIZATION_WIDTH_IN_BITS == 512
#define DEAL_II_COMPILER_VECTORIZATION_LEVEL 3
#elif DEAL_II_VECTORIZATION_WIDTH_IN_BITS == 256
#define DEAL_II_COMPILER_VECTORIZATION_LEVEL 2
#elif DEAL_II_VECTORIZATION_WIDTH_IN_BITS == 128
#define DEAL_II_COMPILER_VECTORIZATION_LEVEL 1
#else
#define DEAL_II_COMPILER_VECTORIZATION_LEVEL 0
#endif

#define DEAL_II_OPENMP_SIMD_PRAGMA _Pragma("omp simd")


/***********************************************************************
 * Language features:
 *
 * For documentation see cmake/checks/check_01_cxx_features.cmake
 */

/* #undef DEAL_II_HAVE_CXX14 */
#define DEAL_II_HAVE_CXX17
/* #undef DEAL_II_HAVE_CXX20 */
/* #undef DEAL_II_HAVE_CXX23 */

#define DEAL_II_HAVE_FP_EXCEPTIONS
/* #undef DEAL_II_HAVE_COMPLEX_OPERATOR_OVERLOADS */
#define DEAL_II_HAVE_CXX17_BESSEL_FUNCTIONS
/* #undef DEAL_II_CXX14_CONSTEXPR_BUG */

// The following three are defined for backwards compatibility with older
// deal.II versions:
#define DEAL_II_WITH_CXX11
#define DEAL_II_WITH_CXX14
#define DEAL_II_WITH_CXX17

/**
 * If we have C++20 available, we can have concepts and requires
 * clauses. We want to avoid using too many `#ifdef` statements, so
 * define a convenience macro that allows us to write a 'requires'
 * clause that is simply removed when not using C++20.
 */
#if defined(DEAL_II_HAVE_CXX20) && !defined(DEAL_II_DOXYGEN_DO_NOT_PARSE_REQUIRES_CLAUSES)
#  define DEAL_II_CXX20_REQUIRES(condition) requires(condition)
#else
#  define DEAL_II_CXX20_REQUIRES(condition)
#endif

/**
 * Provide support for the C++23 [[assume]] attribute. To mimic the
 * attribute for older standards we rely on compiler intrinsics when
 * available.
 */
#ifdef DEAL_II_HAVE_CXX23
#  define define DEAL_II_ASSUME(expr) [[assume(expr)]]
#else
#  if defined(__clang__)
#    define DEAL_II_CXX23_ASSUME(expr) __builtin_assume(static_cast<bool>(expr))
#  elif defined(_MSC_VER) || defined(__ICC)
#    define DEAL_II_CXX23_ASSUME(expr) __assume(expr);
#  else
/* no way with GCC to express this without evaluating 'expr' */
#    define DEAL_II_CXX23_ASSUME(expr) \
    do                               \
      {                              \
      }                              \
    while (false)
#  endif
#endif


/**
 * Macro indicating that the current feature will be removed in a future
 * release.
 */
#define DEAL_II_DEPRECATED [[deprecated]]
#define DEAL_II_DEPRECATED_WITH_COMMENT(comment) [[deprecated(comment)]]

/**
 * Same as above, but for things that have been deprecated during the current
 * development cycle. By default, no warnings are printed for a feature
 * deprecated prior to a release until <em>after</em> that release has been
 * finalized - see DEAL_II_EARLY_DEPRECATIONS for more information.
 */
/* #undef DEAL_II_EARLY_DEPRECATIONS */
#ifndef DEAL_II_DEPRECATED_EARLY
// guard to allow user to override DEAL_II_DEPRECATED_EARLY
#ifdef DEAL_II_EARLY_DEPRECATIONS
#define DEAL_II_DEPRECATED_EARLY [[deprecated]]
#else
#define DEAL_II_DEPRECATED_EARLY
#endif
#endif

#ifndef DEAL_II_DEPRECATED_EARLY_WITH_COMMENT
// guard to allow user to override DEAL_II_DEPRECATED_EARLY
#ifdef DEAL_II_EARLY_DEPRECATIONS
#define DEAL_II_DEPRECATED_EARLY_WITH_COMMENT(comment) [[deprecated(comment)]]
#else
#define DEAL_II_DEPRECATED_EARLY_WITH_COMMENT(comment)
#endif
#endif

#define DEAL_II_FALLTHROUGH [[fallthrough]]
#define DEAL_II_CONSTEXPR constexpr


/***********************************************************************
 * System features:
 *
 * For documentation see cmake/checks/check_02_system_features.cmake
 */

#define DEAL_II_HAVE_SYS_RESOURCE_H
#define DEAL_II_HAVE_UNISTD_H
#define DEAL_II_HAVE_GETHOSTNAME
#define DEAL_II_HAVE_GETPID
/* #undef DEAL_II_HAVE_JN */

/* #undef DEAL_II_MSVC */


/***********************************************************************
 * Feature configuration
 *
 * For documentation see cmake/configure/configure_*.cmake and
 * cmake/modules/Find*.cmake
 */

/* cmake/modules/FindADOLC.cmake */
#define DEAL_II_ADOLC_WITH_ATRIG_ERF
/* #undef DEAL_II_ADOLC_WITH_ADVANCED_BRANCHING */
/* #undef DEAL_II_ADOLC_WITH_TAPELESS_REFCOUNTING */

/* cmake/modules/FindARBORX.cmake */
/* #undef DEAL_II_ARBORX_WITH_MPI */

/* cmake/modules/FindARPACK.cmake */
#define DEAL_II_ARPACK_WITH_PARPACK

/* cmake/modules/FindGMSH.cmake */
#define DEAL_II_GMSH_WITH_API

/* cmake/modules/FindPETSC.cmake */
/* #undef DEAL_II_PETSC_WITH_COMPLEX */
/* #undef DEAL_II_PETSC_WITH_HYPRE */
/* #undef DEAL_II_PETSC_WITH_MUMPS */
/* #undef DEAL_II_PETSC_WITH_KOKKOS */

/* cmake/modules/FindSUNDIALS.cmake */
#define DEAL_II_SUNDIALS_WITH_IDAS

/* cmake/modules/FindSYMENGINE.cmake */
/* #undef DEAL_II_SYMENGINE_WITH_LLVM */

/* cmake/configure/configure_20_boost.cmake */
#define DEAL_II_BOOST_HAS_BROKEN_HEADER_DEPRECATIONS

/* cmake/configure/configure_50_cgal.cmake */
/* #undef DEAL_II_CGAL_HAS_DEPRECATED_BOOST_INCLUDES */

/* cmake/configure/configure_2_trilinos.cmake */
#define DEAL_II_TRILINOS_CXX_SUPPORTS_SACADO_COMPLEX_RAD
#define DEAL_II_TRILINOS_WITH_AMESOS2
#define DEAL_II_TRILINOS_WITH_BELOS
#define DEAL_II_TRILINOS_WITH_EPETRAEXT
#define DEAL_II_TRILINOS_WITH_IFPACK2
/* #undef DEAL_II_TRILINOS_WITH_MUELU */
#define DEAL_II_TRILINOS_WITH_NOX
#define DEAL_II_TRILINOS_WITH_ROL
#define DEAL_II_TRILINOS_WITH_SACADO
/* #undef DEAL_II_TRILINOS_WITH_SEACAS */
/* #undef DEAL_II_TRILINOS_WITH_TPETRA */
#define DEAL_II_TRILINOS_WITH_ZOLTAN

#if defined(DEAL_II_BOOST_HAS_BROKEN_HEADER_DEPRECATIONS) || \
  defined(DEAL_II_CGAL_HAS_DEPRECATED_BOOST_INCLUDES)
#  ifndef BOOST_ALLOW_DEPRECATED_HEADERS
#    define BOOST_ALLOW_DEPRECATED_HEADERS
#  endif
#endif

/***********************************************************************
 * Various macros for version number query and comparison:
 *
 * These macros are defined to make testing for specific versions within
 * the deal.II main code as simple as possible.
 */

/*
 * deal.II:
 */

/**
 * Returns true if the used deal.II version is greater or equal than the
 * version specified by the three arguments. The internal implementation
 * assumes that the number of minor and subminor versions is not larger
 * than 100.
 */
#define DEAL_II_VERSION_GTE(major,minor,subminor) \
 ((DEAL_II_VERSION_MAJOR * 10000 + \
    DEAL_II_VERSION_MINOR * 100 + \
     DEAL_II_VERSION_SUBMINOR) \
    >=  \
    (major)*10000 + (minor)*100 + (subminor))

/*
 * boost:
 */
#define DEAL_II_BOOST_VERSION_MAJOR 1
#define DEAL_II_BOOST_VERSION_MINOR 74
#define DEAL_II_BOOST_VERSION_SUBMINOR 0

#define DEAL_II_BOOST_VERSION_GTE(major,minor,subminor) \
 ((DEAL_II_BOOST_VERSION_MAJOR * 100000 + \
    DEAL_II_BOOST_VERSION_MINOR * 100 + \
     DEAL_II_BOOST_VERSION_SUBMINOR) \
    >= \
    (major)*100000 + (minor)*100 + (subminor))

/*
 * Gmsh:
 */
#ifdef DEAL_II_WITH_GMSH
#  define DEAL_II_GMSH_EXECUTABLE_PATH "/usr/bin/gmsh"
#endif

/**
 * OpenCASCADE:
 */

#ifdef DEAL_II_WITH_OPENCASCADE
#  define DEAL_II_OPENCASCADE_VERSION_MAJOR 7
#  define DEAL_II_OPENCASCADE_VERSION_MINOR 5
#  define DEAL_II_OPENCASCADE_VERSION_SUBMINOR 1

#  define DEAL_II_OPENCASCADE_VERSION_GTE(major,minor,subminor) \
 ((DEAL_II_OPENCASCADE_VERSION_MAJOR * 10000 + \
    DEAL_II_OPENCASCADE_VERSION_MINOR * 100 + \
      DEAL_II_OPENCASCADE_VERSION_SUBMINOR) \
    >=  \
    (major)*10000 + (minor)*100 + (subminor))
#endif

/*
 * p4est:
 */

#ifdef DEAL_II_WITH_P4EST
#  define DEAL_II_P4EST_VERSION_MAJOR 2
#  define DEAL_II_P4EST_VERSION_MINOR 2
#  define DEAL_II_P4EST_VERSION_SUBMINOR 0
#  define DEAL_II_P4EST_VERSION_PATCH 0

#  define DEAL_II_P4EST_VERSION_GTE(major,minor,subminor,patch) \
 ((DEAL_II_P4EST_VERSION_MAJOR * 1000000 + \
    DEAL_II_P4EST_VERSION_MINOR * 10000 + \
     DEAL_II_P4EST_VERSION_SUBMINOR * 100 + \
      DEAL_II_P4EST_VERSION_PATCH) \
    >=  \
    (major)*1000000 + (minor)*10000 + (subminor)*100 + (patch))
#endif

/*
 * SUNDIALS:
 */

#ifdef DEAL_II_WITH_SUNDIALS
 #  define DEAL_II_SUNDIALS_VERSION_MAJOR 5
 #  define DEAL_II_SUNDIALS_VERSION_MINOR 8
 #  define DEAL_II_SUNDIALS_VERSION_PATCH 0

 #define DEAL_II_SUNDIALS_VERSION_GTE(major,minor,patch) \
   ((DEAL_II_SUNDIALS_VERSION_MAJOR * 10000 + \
     DEAL_II_SUNDIALS_VERSION_MINOR * 100 + \
     DEAL_II_SUNDIALS_VERSION_PATCH) \
     >=  \
     (major)*10000 + (minor)*100 + (patch))

 #define DEAL_II_SUNDIALS_VERSION_LT(major,minor,patch) \
   ((DEAL_II_SUNDIALS_VERSION_MAJOR * 10000 + \
     DEAL_II_SUNDIALS_VERSION_MINOR * 100 + \
     DEAL_II_SUNDIALS_VERSION_PATCH) \
     <  \
     (major)*10000 + (minor)*100 + (patch))
#endif

/*
 * PETSc:
 *
 * Note: The following macros are defined in petscversion.h
 *       so we don't repeat them here.
 */

#ifdef DEAL_II_WITH_PETSC
#  define DEAL_II_PETSC_VERSION_LT(major,minor,subminor) \
    PETSC_VERSION_LT(major,minor,subminor)
#  define DEAL_II_PETSC_VERSION_GTE(major,minor,subminor) \
    PETSC_VERSION_GE(major,minor,subminor)
#endif

/*
 * SLEPC:
 */

#ifdef DEAL_II_WITH_SLEPC
#  define DEAL_II_SLEPC_VERSION_LT(major,minor,subminor) \
    SLEPC_VERSION_LT(major,minor,subminor)
#  define DEAL_II_SLEPC_VERSION_GTE(major,minor,subminor) \
    SLEPC_VERSION_GE(major,minor,subminor)
#endif

/*
 * Trilinos:
 */

#ifdef DEAL_II_WITH_TRILINOS
#  define DEAL_II_TRILINOS_VERSION_MAJOR 13
#  define DEAL_II_TRILINOS_VERSION_MINOR 2
#  define DEAL_II_TRILINOS_VERSION_SUBMINOR 0

#  define DEAL_II_TRILINOS_VERSION_GTE(major,minor,subminor) \
 ((DEAL_II_TRILINOS_VERSION_MAJOR * 10000 + \
    DEAL_II_TRILINOS_VERSION_MINOR * 100 + \
      DEAL_II_TRILINOS_VERSION_SUBMINOR) \
    >=  \
    (major)*10000 + (minor)*100 + (subminor))
#endif

/*
 * CGAL:
 */

#ifdef DEAL_II_WITH_CGAL
#  define DEAL_II_CGAL_VERSION_MAJOR 
#  define DEAL_II_CGAL_VERSION_MINOR 
#  define DEAL_II_CGAL_VERSION_SUBMINOR 

#  define DEAL_II_CGAL_VERSION_GTE(major, minor, subminor)                    \
    ((DEAL_II_CGAL_VERSION_MAJOR * 10000 + DEAL_II_CGAL_VERSION_MINOR * 100 + \
      DEAL_II_CGAL_VERSION_SUBMINOR) >=                                       \
     (major)*10000 + (minor)*100 + (subminor))
#endif

/*
 * MPI
 */

#ifdef DEAL_II_WITH_MPI
#  define DEAL_II_MPI_VERSION_MAJOR 3
#  define DEAL_II_MPI_VERSION_MINOR 1

#  define DEAL_II_MPI_VERSION_GTE(major,minor) \
 ((DEAL_II_MPI_VERSION_MAJOR * 100 + \
    DEAL_II_MPI_VERSION_MINOR) \
    >=  \
    (major)*100 + (minor))
#else
#  define DEAL_II_MPI_VERSION_GTE(major,minor) false
#endif

/* #undef DEAL_II_MPI_WITH_DEVICE_SUPPORT */
#ifdef DEAL_II_MPI_WITH_DEVICE_SUPPORT
/* #undef DEAL_II_MPI_WITH_CUDA_SUPPORT */
#endif

/***********************************************************************
 * Two macro names that we put at the top and bottom of all deal.II files
 * and that will be expanded to "namespace dealii {" and "}".
 */

#define DEAL_II_NAMESPACE_OPEN namespace dealii {
#define DEAL_II_NAMESPACE_CLOSE }

/***********************************************************************
 * Two macros to guard external header includes.
 *
 * Selectively disable diagnostics set by "-Wextra" (and similar flags) for
 * GCC and compiler accepting GCC dialects (such as clang).
 * "diagnostic push" is supported since gcc-4.6 and clang-3.3.
 */

#ifdef DEAL_II_COMPILER_HAS_DIAGNOSTIC_PRAGMA

/* keep pragmas with an exclamation mark in order.. */
#  define DEAL_II_DISABLE_EXTRA_DIAGNOSTICS                             \
_Pragma("GCC diagnostic push")                                    /*!*/ \
_Pragma("GCC diagnostic ignored \"-Wunknown-pragmas\"")           /*!*/ \
_Pragma("GCC diagnostic ignored \"-Wpragmas\"")                   /*!*/ \
_Pragma("GCC diagnostic ignored \"-Wunknown-warning-option\"")    /*!*/ \
_Pragma("GCC diagnostic ignored \"-Wunknown-warning\"")           /*!*/ \
_Pragma("GCC diagnostic ignored \"-Wextra\"")                     /*!*/ \
_Pragma("GCC diagnostic ignored \"-Waddress-of-packed-member\"")        \
_Pragma("GCC diagnostic ignored \"-Wcast-function-type\"")              \
_Pragma("GCC diagnostic ignored \"-Wdeprecated-copy\"")                 \
_Pragma("GCC diagnostic ignored \"-Wdeprecated-declarations\"")         \
_Pragma("GCC diagnostic ignored \"-Wdeprecated-volatile\"")             \
_Pragma("GCC diagnostic ignored \"-Wexpansion-to-defined\"")            \
_Pragma("GCC diagnostic ignored \"-Wfloat-conversion\"")                \
_Pragma("GCC diagnostic ignored \"-Wignored-attributes\"")              \
_Pragma("GCC diagnostic ignored \"-Wignored-qualifiers\"")              \
_Pragma("GCC diagnostic ignored \"-Wimplicit-fallthrough\"")            \
_Pragma("GCC diagnostic ignored \"-Winfinite-recursion\"")              \
_Pragma("GCC diagnostic ignored \"-Wint-in-bool-context\"")             \
_Pragma("GCC diagnostic ignored \"-Wmaybe-uninitialized\"")             \
_Pragma("GCC diagnostic ignored \"-Wmisleading-indentation\"")          \
_Pragma("GCC diagnostic ignored \"-Wmissing-field-initializers\"")      \
_Pragma("GCC diagnostic ignored \"-Wnested-anon-types\"")               \
_Pragma("GCC diagnostic ignored \"-Wnon-template-friend\"")             \
_Pragma("GCC diagnostic ignored \"-Wnon-virtual-dtor\"")                \
_Pragma("GCC diagnostic ignored \"-Wnonnull\"")                         \
_Pragma("GCC diagnostic ignored \"-Woverflow\"")                        \
_Pragma("GCC diagnostic ignored \"-Woverloaded-virtual\"")              \
_Pragma("GCC diagnostic ignored \"-Wpedantic\"")                        \
_Pragma("GCC diagnostic ignored \"-Wsuggest-override\"")                \
_Pragma("GCC diagnostic ignored \"-Wtautological-constant-out-of-range-compare\"") \
_Pragma("GCC diagnostic ignored \"-Wtautological-overlap-compare\"")    \
_Pragma("GCC diagnostic ignored \"-Wtype-limits\"")                     \
_Pragma("GCC diagnostic ignored \"-Wundef\"")                           \
_Pragma("GCC diagnostic ignored \"-Wunused-but-set-parameter\"")        \
_Pragma("GCC diagnostic ignored \"-Wunused-but-set-variable\"")         \
_Pragma("GCC diagnostic ignored \"-Wunused-function\"")                 \
_Pragma("GCC diagnostic ignored \"-Wunused-parameter\"")                \
_Pragma("GCC diagnostic ignored \"-Wunused-private-field\"")            \
_Pragma("GCC diagnostic ignored \"-Wunused-variable\"")                 \
_Pragma("GCC diagnostic ignored \"-Wuse-after-free\"")                  \
_Pragma("GCC diagnostic warning \"-Wpragmas\"")                   /*!*/

#  define DEAL_II_ENABLE_EXTRA_DIAGNOSTICS                              \
_Pragma("GCC diagnostic pop")

#else

#  define DEAL_II_DISABLE_EXTRA_DIAGNOSTICS
#  define DEAL_II_ENABLE_EXTRA_DIAGNOSTICS

#endif

/***********************************************************************
 * Define macros for picking the correct C linkage name for a Fortran function.
 * See cmake/configure/configure_fortran_mangling.cmake for more information.
 */

#define DEAL_II_FORTRAN_MANGLE(name, NAME) name ## _

#define DEAL_II_FORTRAN_MANGLE_UNDERSCORE(name, NAME) name ## _

/***********************************************************************
 * Define a portable preprocessor macro that generates custom warnings
 * reporting the line and the file where the warning appears. Taken from:
 * http://goodliffe.blogspot.com/2009/07/c-how-to-say-warning-to-visual-studio-c.html
 */

#ifdef _MSC_VER
  #define DEAL_II_STRINGIZE_HELPER(x) #x
  #define DEAL_II_STRINGIZE(x) DEAL_II_STRINGIZE_HELPER(x)
  #define DEAL_II_DO_PRAGMA(x) __pragma(x)
  #define DEAL_II_WARNING(desc) DEAL_II_DO_PRAGMA(message(__FILE__ "(" DEAL_II_STRINGIZE(__LINE__) ") : warning: " #desc))
#else
  #define DEAL_II_DO_PRAGMA(x) _Pragma(#x)
  #define DEAL_II_WARNING(desc) DEAL_II_DO_PRAGMA(message(#desc))
#endif


/***********************************************************************
 * Final inclusions:
 */

/*
 * Some systems require including mpi.h before stdio.h which happens in
 * types.h
 */
#if defined(DEAL_II_WITH_MPI)
DEAL_II_DISABLE_EXTRA_DIAGNOSTICS
#  include <mpi.h>
DEAL_II_ENABLE_EXTRA_DIAGNOSTICS
#endif

#include <deal.II/base/numbers.h>
#include <deal.II/base/types.h>

/*
 * Include the boost version header to do a quick version check in case, by
 * accident, we have configured with one version of boost but are compiling
 * either the library or an external application with a different version of
 * boost.
 */
#include <boost/version.hpp>
static_assert(
  BOOST_VERSION == 100000 * DEAL_II_BOOST_VERSION_MAJOR +
                     100 * DEAL_II_BOOST_VERSION_MINOR +
                     DEAL_II_BOOST_VERSION_SUBMINOR,
  "The version number of boost that you are compiling with does not match the "
  "version number of boost found during deal.II's configuration step. This "
  "leads to difficult to understand bugs and is not supported. Please check "
  "that you have set up your application with the same version of boost as "
  "deal.II.");

#endif
