cmake_minimum_required(VERSION 3.19.0)

include("./scb_cmake/scb_include.cmake")
scb_init_project()
project(${SCB_PROJECT_NAME} VERSION ${SCB_PROJECT_VERSION})

cmake_policy(SET CMP0076 NEW)
set (CMAKE_CXX_STANDARD 20)

set(TARGET_NAME ${SCB_PROJECT_NAME})
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
