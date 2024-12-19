cmake_minimum_required(VERSION 3.19.0)
project(test VERSION 0.1.0)

set(TARGET_NAME test)

cmake_policy(SET CMP0076 NEW)
set (CMAKE_CXX_STANDARD 20)

include_directories(${TRIPLET_INCLUDE_DIRS}) 

add_executable(${TARGET_NAME})
# add_library(${TARGET_NAME} SHARED test.cpp)
# add_library(${TARGET_NAME} test.cpp)

add_subdirectory("./src/cpp")

set_target_properties(${TARGET_NAME}
    PROPERTIES
    ARCHIVE_OUTPUT_DIRECTORY "./arc/"
    LIBRARY_OUTPUT_DIRECTORY "./lib/"
    RUNTIME_OUTPUT_DIRECTORY "./bin/"
)

set(CPACK_PROJECT_NAME ${PROJECT_NAME})
set(CPACK_PROJECT_VERSION ${PROJECT_VERSION})
