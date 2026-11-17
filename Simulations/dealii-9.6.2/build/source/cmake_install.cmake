# Install script for directory: /home/user/Downloads/dealii-9.6.2/source

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/usr/local")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "Release")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

# Set default install directory permissions.
if(NOT DEFINED CMAKE_OBJDUMP)
  set(CMAKE_OBJDUMP "/usr/bin/objdump")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xlibraryx" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libdeal_II.so.9.6.2" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libdeal_II.so.9.6.2")
    file(RPATH_CHECK
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libdeal_II.so.9.6.2"
         RPATH "/usr/lib/x86_64-linux-gnu/openmpi/lib:/usr/lib/x86_64-linux-gnu/hdf5/openmpi:/home/user/miniconda3/lib/python3.13/site-packages/slepc/lib:/home/user/miniconda3/lib/python3.13/site-packages/petsc/lib")
  endif()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE SHARED_LIBRARY MESSAGE_LAZY FILES "/home/user/Downloads/dealii-9.6.2/build/lib/libdeal_II.so.9.6.2")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libdeal_II.so.9.6.2" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libdeal_II.so.9.6.2")
    file(RPATH_CHANGE
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libdeal_II.so.9.6.2"
         OLD_RPATH "/usr/lib/x86_64-linux-gnu/openmpi/lib:/usr/lib/x86_64-linux-gnu/hdf5/openmpi:/home/user/miniconda3/lib/python3.13/site-packages/slepc/lib:/home/user/miniconda3/lib/python3.13/site-packages/petsc/lib:"
         NEW_RPATH "/usr/lib/x86_64-linux-gnu/openmpi/lib:/usr/lib/x86_64-linux-gnu/hdf5/openmpi:/home/user/miniconda3/lib/python3.13/site-packages/slepc/lib:/home/user/miniconda3/lib/python3.13/site-packages/petsc/lib")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libdeal_II.so.9.6.2")
    endif()
  endif()
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xlibraryx" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libdeal_II.so" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libdeal_II.so")
    file(RPATH_CHECK
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libdeal_II.so"
         RPATH "/usr/lib/x86_64-linux-gnu/openmpi/lib:/usr/lib/x86_64-linux-gnu/hdf5/openmpi:/home/user/miniconda3/lib/python3.13/site-packages/slepc/lib:/home/user/miniconda3/lib/python3.13/site-packages/petsc/lib")
  endif()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE SHARED_LIBRARY MESSAGE_LAZY FILES "/home/user/Downloads/dealii-9.6.2/build/lib/libdeal_II.so")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libdeal_II.so" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libdeal_II.so")
    file(RPATH_CHANGE
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libdeal_II.so"
         OLD_RPATH "/usr/lib/x86_64-linux-gnu/openmpi/lib:/usr/lib/x86_64-linux-gnu/hdf5/openmpi:/home/user/miniconda3/lib/python3.13/site-packages/slepc/lib:/home/user/miniconda3/lib/python3.13/site-packages/petsc/lib:"
         NEW_RPATH "/usr/lib/x86_64-linux-gnu/openmpi/lib:/usr/lib/x86_64-linux-gnu/hdf5/openmpi:/home/user/miniconda3/lib/python3.13/site-packages/slepc/lib:/home/user/miniconda3/lib/python3.13/site-packages/petsc/lib")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libdeal_II.so")
    endif()
  endif()
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xlibraryx" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/cmake/deal.II/deal.IITargets.cmake")
    file(DIFFERENT EXPORT_FILE_CHANGED FILES
         "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/cmake/deal.II/deal.IITargets.cmake"
         "/home/user/Downloads/dealii-9.6.2/build/source/CMakeFiles/Export/lib/cmake/deal.II/deal.IITargets.cmake")
    if(EXPORT_FILE_CHANGED)
      file(GLOB OLD_CONFIG_FILES "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/cmake/deal.II/deal.IITargets-*.cmake")
      if(OLD_CONFIG_FILES)
        message(STATUS "Old export file \"$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/cmake/deal.II/deal.IITargets.cmake\" will be replaced.  Removing files [${OLD_CONFIG_FILES}].")
        file(REMOVE ${OLD_CONFIG_FILES})
      endif()
    endif()
  endif()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/cmake/deal.II" TYPE FILE MESSAGE_LAZY FILES "/home/user/Downloads/dealii-9.6.2/build/source/CMakeFiles/Export/lib/cmake/deal.II/deal.IITargets.cmake")
  if("${CMAKE_INSTALL_CONFIG_NAME}" MATCHES "^([Rr][Ee][Ll][Ee][Aa][Ss][Ee])$")
    file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/cmake/deal.II" TYPE FILE MESSAGE_LAZY FILES "/home/user/Downloads/dealii-9.6.2/build/source/CMakeFiles/Export/lib/cmake/deal.II/deal.IITargets-release.cmake")
  endif()
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for each subdirectory.
  include("/home/user/Downloads/dealii-9.6.2/build/source/numerics/cmake_install.cmake")
  include("/home/user/Downloads/dealii-9.6.2/build/source/fe/cmake_install.cmake")
  include("/home/user/Downloads/dealii-9.6.2/build/source/matrix_free/cmake_install.cmake")
  include("/home/user/Downloads/dealii-9.6.2/build/source/dofs/cmake_install.cmake")
  include("/home/user/Downloads/dealii-9.6.2/build/source/lac/cmake_install.cmake")
  include("/home/user/Downloads/dealii-9.6.2/build/source/base/cmake_install.cmake")
  include("/home/user/Downloads/dealii-9.6.2/build/source/cgal/cmake_install.cmake")
  include("/home/user/Downloads/dealii-9.6.2/build/source/gmsh/cmake_install.cmake")
  include("/home/user/Downloads/dealii-9.6.2/build/source/grid/cmake_install.cmake")
  include("/home/user/Downloads/dealii-9.6.2/build/source/hp/cmake_install.cmake")
  include("/home/user/Downloads/dealii-9.6.2/build/source/multigrid/cmake_install.cmake")
  include("/home/user/Downloads/dealii-9.6.2/build/source/distributed/cmake_install.cmake")
  include("/home/user/Downloads/dealii-9.6.2/build/source/algorithms/cmake_install.cmake")
  include("/home/user/Downloads/dealii-9.6.2/build/source/integrators/cmake_install.cmake")
  include("/home/user/Downloads/dealii-9.6.2/build/source/meshworker/cmake_install.cmake")
  include("/home/user/Downloads/dealii-9.6.2/build/source/opencascade/cmake_install.cmake")
  include("/home/user/Downloads/dealii-9.6.2/build/source/particles/cmake_install.cmake")
  include("/home/user/Downloads/dealii-9.6.2/build/source/differentiation/cmake_install.cmake")
  include("/home/user/Downloads/dealii-9.6.2/build/source/physics/cmake_install.cmake")
  include("/home/user/Downloads/dealii-9.6.2/build/source/optimization/rol/cmake_install.cmake")
  include("/home/user/Downloads/dealii-9.6.2/build/source/non_matching/cmake_install.cmake")
  include("/home/user/Downloads/dealii-9.6.2/build/source/sundials/cmake_install.cmake")
  include("/home/user/Downloads/dealii-9.6.2/build/source/trilinos/cmake_install.cmake")
  include("/home/user/Downloads/dealii-9.6.2/build/source/arborx/cmake_install.cmake")

endif()

