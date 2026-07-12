cmake_minimum_required(VERSION 3.20)

project(fre VERSION 0.1.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

option(FRE_ENABLE_OPENFHE "Enable the OpenFHE backend" OFF)

add_library(fre_reference STATIC
    src/support_mode_reference.cpp
)

target_include_directories(fre_reference
    PUBLIC
        ${CMAKE_CURRENT_SOURCE_DIR}/include
)

add_executable(fre_support_reference
    src/cli/fre_support_reference.cpp
)

target_link_libraries(fre_support_reference
    PRIVATE
        fre_reference
)

if(CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
    target_compile_options(fre_reference
        PRIVATE -Wall -Wextra -Werror
    )
    target_compile_options(fre_support_reference
        PRIVATE -Wall -Wextra -Werror
    )
endif()

include(CTest)

if(BUILD_TESTING)
    add_test(
        NAME fre_reference_regular
        COMMAND fre_support_reference 10 10 10 10 10 10
    )
    set_tests_properties(fre_reference_regular PROPERTIES
        PASS_REGULAR_EXPRESSION "K[^0-9-]*0.*regular[^a-z]*true"
    )

    add_test(
        NAME fre_reference_nonuniform
        COMMAND fre_support_reference 11 9 10 10 10 10
    )
    set_tests_properties(fre_reference_nonuniform PROPERTIES
        PASS_REGULAR_EXPRESSION "K[^0-9-]*72.*regular[^a-z]*false"
    )

    add_test(
        NAME fre_reference_scale_control
        COMMAND fre_support_reference 22 18 20 20 20 20
    )
    set_tests_properties(fre_reference_scale_control PROPERTIES
        PASS_REGULAR_EXPRESSION "K[^0-9-]*288.*regular[^a-z]*false"
    )

    add_test(
        NAME fre_reference_reject_bad_count
        COMMAND fre_support_reference 10 10 10 10 10
    )
    set_tests_properties(fre_reference_reject_bad_count PROPERTIES
        WILL_FAIL TRUE
    )
endif()

if(FRE_ENABLE_OPENFHE)
    message(FATAL_ERROR
        "OpenFHE backend gate is closed until its adapter is stubbed")
endif()

message(STATUS "FRE plaintext reference target configured")
