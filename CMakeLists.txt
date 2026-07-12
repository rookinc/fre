cmake_minimum_required(VERSION 3.20)

project(fre VERSION 0.1.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

option(FRE_ENABLE_OPENFHE "Enable the OpenFHE backend" OFF)

if(FRE_ENABLE_OPENFHE)
    message(FATAL_ERROR
        "OpenFHE backend gate is closed until its adapter is stubbed")
endif()

message(STATUS "FRE Phase 0 scaffold configured")
