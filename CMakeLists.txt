if (${CMAKE_SOURCE_DIR} STREQUAL ${CMAKE_BINARY_DIR})
    message(FATAL_ERROR "Prevented in-tree built. Please create a build directory outside of the source code and call cmake from there")
endif ()

cmake_minimum_required(VERSION 3.9)
project(pbrain-PARIS-Florian-Bacho)

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ../)
set(CMAKE_CXX_STANDARD 17)


set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS}")


file(GLOB_RECURSE src
		"src/*.cpp")

file(GLOB inc
		"inc")

include_directories(${inc})

set(CMAKE_SUPPRESS_REGENERATION true)
add_executable(${PROJECT_NAME} WIN32 ${src} ${inc})