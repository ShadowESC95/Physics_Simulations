#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "dealii::dealii_release" for configuration "Release"
set_property(TARGET dealii::dealii_release APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(dealii::dealii_release PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libdeal_II.so.9.6.2"
  IMPORTED_SONAME_RELEASE "libdeal_II.so.9.6.2"
  )

list(APPEND _IMPORT_CHECK_TARGETS dealii::dealii_release )
list(APPEND _IMPORT_CHECK_FILES_FOR_dealii::dealii_release "${_IMPORT_PREFIX}/lib/libdeal_II.so.9.6.2" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
