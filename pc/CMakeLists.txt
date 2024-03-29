cmake_minimum_required(VERSION 3.0)
project(line_tracker)

set(CMAKE_POSITION_INDEPENDENT_CODE ON)
set(CMAKE_CXX_STANDARD 14)
set(CMAKE_BUILD_TYPE "Release")
set(CMAKE_CXX_FLAGS "-std=c++14")
set(CMAKE_CXX_FLAGS_RELEASE "-O3 -Wall -g")

# Import OpenCV
find_package(OpenCV 3.4.16 REQUIRED)
include_directories(${OpenCV_INCLUDE_DIRS})

# Import Eigen3 and Boost
find_package(Eigen3 REQUIRED)
find_package(Boost REQUIRED COMPONENTS filesystem program_options system)
include_directories(${EIGEN3_INCLUDE_DIR})

# Line Feature Tracker Library and Executable
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/include)

add_subdirectory(submodules)
include_directories(${ELSED_INCLUDE_DIR})

add_executable(proj
  src/test_linefeaturetracker.cpp
  src/linefeature_tracker.cpp
)

target_link_libraries(proj PRIVATE ${ELSED_LIB} ${OpenCV_LIBS} ${Boost_LIBRARIES})

add_library(linefeature_tracker STATIC src/linefeature_tracker.cpp)
target_link_libraries(linefeature_tracker PRIVATE ${ELSED_LIB} ${OpenCV_LIBS} ${Boost_LIBRARIES})
set_target_properties(linefeature_tracker PROPERTIES POSITION_INDEPENDENT_CODE ON)

# Pybind11 Integration
pybind11_add_module(line_tracker src/binder.cpp)
target_link_libraries(line_tracker PRIVATE linefeature_tracker ${ELSED_LIB} ${OpenCV_LIBS} ${Boost_LIBRARIES})