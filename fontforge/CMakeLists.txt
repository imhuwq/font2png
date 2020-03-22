# Distributed under the original FontForge BSD 3-clause license

cmake_minimum_required(VERSION 3.5)

# No in source builds
if ("${CMAKE_SOURCE_DIR}" STREQUAL "${CMAKE_BINARY_DIR}")
    message(FATAL_ERROR "In-source builds are disallowed. Create a build folder to run CMake from.")
endif ()

project(fontforge LANGUAGES C CXX)

# Add folder for custom cmake modules
list(INSERT CMAKE_MODULE_PATH 0 ${CMAKE_SOURCE_DIR}/cmake ${CMAKE_SOURCE_DIR}/cmake/packages)
if (${CMAKE_VERSION} VERSION_LESS "3.14")
    # This could be more targeted, but keep it simple
    list(APPEND CMAKE_MODULE_PATH ${CMAKE_SOURCE_DIR}/cmake/backports/3.14.5)
endif ()

# Include any required modules
include(BuildUtils)
include(CheckIncludeFile)
include(PackageUtils)
include(TargetUtils)

# Set any global defines
set(CMAKE_C_STANDARD 99)
set(CMAKE_C_STANDARD_REQUIRED TRUE)
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED TRUE)
set(CMAKE_THREAD_PREFER_PTHREAD 1)

set_default_build_type(RelWithDebInfo) # Sets CMAKE_BUILD_TYPE
set_default_rpath()

# Options
set_option(BUILD_SHARED_LIBS BOOL ON "Build libfontforge as a shared library")
set_option(ENABLE_PYTHON_SCRIPTING BOOL ON "Enables FontForge's Python scripting support")
set_option(ENABLE_PYTHON_EXTENSION AUTO ON "Builds the Python models for use with system python")
set_option(ENABLE_SANITIZER ENUM "none" "Enables a sanitizer. Requires support from the compiler."
        "none" "address" "leak" "thread" "undefined" "memory")
set_option(REAL_TYPE ENUM "double" "Sets the floating point type used." "double" "float")
set_option(THEME ENUM "tango" "Sets the GUI theme." "tango" "2012")

set(Python3_FIND_REGISTRY LAST)
set(Python3_USE_STATIC_LIBS FALSE)

if (CMAKE_C_COMPILER_ID MATCHES "GNU|Clang")
    list(APPEND _test_flags CFLAGS -Werror=implicit-function-declaration -Werror=int-conversion)
    set_supported_compiler_flags(FONTFORGE_DEFAULT_CFLAGS FONTFORGE_DEFAULT_CXXFLAGS ${_test_flags})
    list(APPEND FONTFORGE_EXTRA_CFLAGS -Wall -Wextra -pedantic)
    add_compile_options(
            "$<$<COMPILE_LANGUAGE:C>:${FONTFORGE_DEFAULT_CFLAGS}>"
            "$<$<COMPILE_LANGUAGE:CXX>:${FONTFORGE_DEFAULT_CXXFLAGS}>"
    )
endif ()

enable_sanitizer("${ENABLE_SANITIZER}")

# Required and default dependencies
find_package(Freetype 2.3.7 REQUIRED)
find_package(Gettext REQUIRED)
find_package_with_target(Intl REQUIRED)
find_package(GLIB 2.6 REQUIRED COMPONENTS gio)
find_package(Iconv REQUIRED)
find_package(LibXml2 REQUIRED)
find_package(MathLib REQUIRED)
find_package(ZLIB REQUIRED)
find_package(GIF REQUIRED)
find_package(JPEG REQUIRED)
find_package(PNG REQUIRED)
find_package(TIFF REQUIRED)
find_package(WOFF2 REQUIRED)

check_include_file(pthread.h HAVE_PTHREAD_H)
if (HAVE_PTHREAD_H)
    find_package(Threads)
endif ()

find_package_auto(ENABLE_PYTHON_SCRIPTING Python3 3.3 COMPONENTS Development Interpreter)

add_subdirectory(includes)
add_subdirectory(gutils)
add_subdirectory(fontforge)
add_subdirectory(libraries/Unicode)

# build the python module
add_library(fontforge_pymodule SHARED python.c)
target_link_libraries(fontforge_pymodule PUBLIC Python3::Python)
set_target_properties(fontforge_pymodule PROPERTIES OUTPUT_NAME "fontforge" PREFIX "")

if (WIN32)
    set_target_properties(fontforge_pymodule PROPERTIES SUFFIX ".pyd")
endif ()

target_link_libraries(fontforge_pymodule PRIVATE fontforge)

