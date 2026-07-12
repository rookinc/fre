cmake_minimum_required(VERSION 3.20)

project(fre VERSION 0.1.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

option(FRE_ENABLE_OPENFHE "Enable the OpenFHE backend" OFF)

set(
    FRE_OPENFHE_PREFIX
    ""
    CACHE PATH
    "Durable OpenFHE installation prefix"
)

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
    if(NOT FRE_OPENFHE_PREFIX)
        message(FATAL_ERROR
            "FRE_OPENFHE_PREFIX is required when OpenFHE is enabled")
    endif()

    set(_fre_openfhe_required
        "${FRE_OPENFHE_PREFIX}/include/openfhe/pke/openfhe.h"
        "${FRE_OPENFHE_PREFIX}/include/openfhe/core/openfhecore.h"
        "${FRE_OPENFHE_PREFIX}/lib/libOPENFHEpke.so"
        "${FRE_OPENFHE_PREFIX}/lib/libOPENFHEbinfhe.so"
        "${FRE_OPENFHE_PREFIX}/lib/libOPENFHEcore.so"
    )

    foreach(_required_path IN LISTS _fre_openfhe_required)
        if(NOT EXISTS "${_required_path}")
            message(FATAL_ERROR
                "Required OpenFHE path missing: ${_required_path}")
        endif()
    endforeach()

    add_library(fre_openfhe_backend STATIC
        src/backends/openfhe/openfhe_backend_status.cpp
    )

    target_include_directories(fre_openfhe_backend
        PUBLIC
            ${CMAKE_CURRENT_SOURCE_DIR}/include
    )

    target_include_directories(fre_openfhe_backend
        SYSTEM PUBLIC
            ${FRE_OPENFHE_PREFIX}/include/openfhe/pke
            ${FRE_OPENFHE_PREFIX}/include/openfhe/core
            ${FRE_OPENFHE_PREFIX}/include/openfhe/binfhe
            ${FRE_OPENFHE_PREFIX}/include/openfhe
            ${FRE_OPENFHE_PREFIX}/include/openfhe/cereal
    )

    target_compile_definitions(fre_openfhe_backend
        PUBLIC
            FRE_OPENFHE_PREFIX="${FRE_OPENFHE_PREFIX}"
            FRE_OPENFHE_VERSION="1.5.1"
    )

    target_link_directories(fre_openfhe_backend
        PUBLIC
            ${FRE_OPENFHE_PREFIX}/lib
    )

    target_link_libraries(fre_openfhe_backend
        PUBLIC
            OPENFHEpke
            OPENFHEbinfhe
            OPENFHEcore
            omp
    )

    add_executable(fre_openfhe_status
        src/cli/fre_openfhe_status.cpp
    )

    target_link_libraries(fre_openfhe_status
        PRIVATE
            fre_openfhe_backend
            OPENFHEpke
            OPENFHEbinfhe
            OPENFHEcore
            omp
    )

    if(CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
        target_compile_options(fre_openfhe_backend
            PRIVATE -Wall -Wextra -Werror
        )
        target_compile_options(fre_openfhe_status
            PRIVATE -Wall -Wextra -Werror
        )
        target_link_options(fre_openfhe_status
            PRIVATE -Wl,--no-as-needed
        )
    endif()

    set_target_properties(fre_openfhe_status PROPERTIES
        BUILD_RPATH "${FRE_OPENFHE_PREFIX}/lib"
    )

    if(BUILD_TESTING)
        add_test(
            NAME fre_openfhe_link_status
            COMMAND fre_openfhe_status
        )
        set_tests_properties(fre_openfhe_link_status PROPERTIES
            PASS_REGULAR_EXPRESSION
                "linked[^a-z]*true.*profile_admitted[^a-z]*false.*crypto_allowed[^a-z]*false"
        )
    endif()

    message(STATUS
        "FRE OpenFHE link-only target configured")
else()
    message(STATUS
        "FRE OpenFHE link-only target disabled")
endif()

message(STATUS "FRE plaintext reference target configured")
