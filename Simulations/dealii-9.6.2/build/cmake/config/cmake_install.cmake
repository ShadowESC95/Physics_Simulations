# Install script for directory: /home/user/Downloads/dealii-9.6.2/cmake/config

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
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/deal.II/macros" TYPE FILE MESSAGE_LAZY FILES
    "/home/user/Downloads/dealii-9.6.2/cmake/macros/macro_deal_ii_add_test.cmake"
    "/home/user/Downloads/dealii-9.6.2/cmake/macros/macro_deal_ii_initialize_cached_variables.cmake"
    "/home/user/Downloads/dealii-9.6.2/cmake/macros/macro_deal_ii_invoke_autopilot.cmake"
    "/home/user/Downloads/dealii-9.6.2/cmake/macros/macro_deal_ii_pickup_tests.cmake"
    "/home/user/Downloads/dealii-9.6.2/cmake/macros/macro_deal_ii_query_git_information.cmake"
    "/home/user/Downloads/dealii-9.6.2/cmake/macros/macro_deal_ii_setup_target.cmake"
    "/home/user/Downloads/dealii-9.6.2/cmake/macros/macro_shell_escape_option_groups.cmake"
    "/home/user/Downloads/dealii-9.6.2/cmake/macros/macro_target_compile_flags.cmake"
    "/home/user/Downloads/dealii-9.6.2/cmake/macros/macro_target_link_flags.cmake"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xlibraryx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/cmake/deal.II" TYPE FILE MESSAGE_LAZY FILES
    "/home/user/Downloads/dealii-9.6.2/build/cmake/config/deal.IIConfig.cmake"
    "/home/user/Downloads/dealii-9.6.2/build/cmake/config/deal.IIConfigGit.cmake"
    "/home/user/Downloads/dealii-9.6.2/build/cmake/config/deal.IIConfigVersion.cmake"
    )
endif()

