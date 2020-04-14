# - Try to find yaml-cpp
# Once done this will define
#  YAMLCPP_FOUND - System has yaml-cpp
#  YAMLCPP_INCLUDE_DIRS - The yaml-cpp include directories
#  YAMLCPP_LIBRARIES - The libraries needed to use yaml-cpp
#  YAMLCPP_DEFINITIONS - Compiler switches required for using yaml-cpp

find_package(PkgConfig)
pkg_check_modules(PC_YAMLCPP QUIET yaml-cpp)
set(YAMLCPP_DEFINITIONS ${PC_YAMLCPP_CFLAGS_OTHER})

find_path(YAMLCPP_INCLUDE_DIR yaml-cpp/yaml.h
          HINTS ${PC_YAMLCPP_INCLUDEDIR} ${PC_YAMLCPP_INCLUDE_DIRS} )

find_library(YAMLCPP_LIBRARY NAMES yaml-cpp libyaml-cpp
             HINTS ${PC_YAMLCPP_LIBDIR} ${PC_YAMLCPP_LIBRARY_DIRS} )

set(YAMLCPP_LIBRARIES ${YAMLCPP_LIBRARY} )
set(YAMLCPP_INCLUDE_DIRS ${YAMLCPP_INCLUDE_DIR} )

include(FindPackageHandleStandardArgs)
# handle the QUIETLY and REQUIRED arguments and set YAMLCPP_FOUND to TRUE
# if all listed variables are TRUE
find_package_handle_standard_args(YamlCpp  DEFAULT_MSG
                                  YAMLCPP_LIBRARY YAMLCPP_INCLUDE_DIR)

mark_as_advanced(YAMLCPP_INCLUDE_DIR YAMLCPP_LIBRARY )