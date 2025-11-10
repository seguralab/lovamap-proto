cmake_minimum_required(VERSION 3.20)
project(lovamap-proto VERSION 0.1.0 LANGUAGES CXX)

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Find Protobuf
find_package(Protobuf REQUIRED)

# Proto files
set(PROTO_FILES
    src/Descriptors.proto
)

# Generate C++ files from proto
protobuf_generate_cpp(PROTO_SRCS PROTO_HDRS ${PROTO_FILES})

# Create library target
add_library(lovamap-proto ${PROTO_SRCS} ${PROTO_HDRS})

# Add alias for consistent naming when used as submodule
add_library(lovamap::proto ALIAS lovamap-proto)

# Include directories
target_include_directories(lovamap-proto
    PUBLIC
        $<BUILD_INTERFACE:${CMAKE_CURRENT_BINARY_DIR}>
        $<INSTALL_INTERFACE:include>
)

# Link protobuf
target_link_libraries(lovamap-proto
    PUBLIC
        protobuf::libprotobuf
)

# Set properties
set_target_properties(lovamap-proto PROPERTIES
    VERSION ${PROJECT_VERSION}
    SOVERSION 1
    POSITION_INDEPENDENT_CODE ON
)

# Installation rules (optional, but useful if you want to install the library)
include(GNUInstallDirs)

install(TARGETS lovamap-proto
    EXPORT lovamap-proto-targets
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
)

install(FILES ${PROTO_HDRS}
    DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/lovamap
)

install(EXPORT lovamap-proto-targets
    FILE lovamap-proto-targets.cmake
    NAMESPACE lovamap::
    DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/lovamap-proto
)

# Only generate config files when building standalone (not as submodule)
if(CMAKE_SOURCE_DIR STREQUAL PROJECT_SOURCE_DIR)
    # Create config file for find_package support
    include(CMakePackageConfigHelpers)

    configure_package_config_file(
        ${CMAKE_CURRENT_SOURCE_DIR}/cmake/lovamap-proto-config.cmake.in
        ${CMAKE_CURRENT_BINARY_DIR}/lovamap-proto-config.cmake
        INSTALL_DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/lovamap-proto
    )

    write_basic_package_version_file(
        ${CMAKE_CURRENT_BINARY_DIR}/lovamap-proto-config-version.cmake
        VERSION ${PROJECT_VERSION}
        COMPATIBILITY SameMajorVersion
    )

    install(FILES
        ${CMAKE_CURRENT_BINARY_DIR}/lovamap-proto-config.cmake
        ${CMAKE_CURRENT_BINARY_DIR}/lovamap-proto-config-version.cmake
        DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/lovamap-proto
    )
endif()
