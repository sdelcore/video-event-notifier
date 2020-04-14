project(database-host)

#This is where you can set flags such as -Wall -pedantic etc...
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++14")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -pthread")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fconcepts")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -lmosquittopp")

#This is required
cmake_minimum_required(VERSION 2.8)
include(CheckCXXCompilerFlag)

#this method points to the include folder for your header files
include_directories(src)
include_directories(lib)

#add subdirectory for the src files
#add_subdirectory(src)

file(GLOB SOURCE_FILES "src/*.cpp" "src/*.h" "lib/*.hpp" "lib/*.h" "lib/*.cpp")

set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} "${CMAKE_CURRENT_SOURCE_DIR}/cmake")

add_executable( host ${SOURCE_FILES} )

find_package (SQLite3)
if (SQLITE3_FOUND)
  include_directories(${SQLITE3_INCLUDE_DIRS})
  target_link_libraries (host ${SQLITE3_LIBRARIES})
endif (SQLITE3_FOUND)

find_package(Mosquittopp)
if(MOSQUITTOPP_FOUND)
  include_directories(${MOSQUITTOPP_INCLUDE_DIRS})
  target_link_libraries (host ${MOSQUITTOPP_LIBRARIES})
endif (MOSQUITTOPP_FOUND)

find_package( YamlCpp )
if(YAMLCPP_FOUND)
  include_directories(${YAMLCPP_INCLUDE_DIRS})
  target_link_libraries(host ${YAMLCPP_LIBRARIES})
endif (YAMLCPP_FOUND)

