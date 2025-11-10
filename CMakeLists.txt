cmake_minimum_required(VERSION 3.20)
project(lovamap-proto VERSION 0.1.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

find_package(Protobuf REQUIRED)

set(PROTO_FILES
    schemas/Descriptors.proto
)

# Generate into a subdirectory
set(PROTO_OUTPUT_DIR ${CMAKE_CURRENT_BINARY_DIR}/lovamap-proto)
file(MAKE_DIRECTORY ${PROTO_OUTPUT_DIR})

# Custom generation with explicit output path
protobuf_generate_cpp(PROTO_SRCS PROTO_HDRS ${PROTO_FILES})

# Move generated files to subdirectory (requires custom command)
# OR better: use protobuf_generate with explicit paths
add_library(lovamap-proto STATIC)

protobuf_generate(
    TARGET lovamap-proto
    PROTOS ${PROTO_FILES}
    PROTOC_OUT_DIR ${PROTO_OUTPUT_DIR}
)

add_library(lovamap::proto ALIAS lovamap-proto)

# Include the parent directory so users do lovamap-proto/Header.pb.h
target_include_directories(lovamap-proto
    PUBLIC
        $<BUILD_INTERFACE:${CMAKE_CURRENT_BINARY_DIR}>
        $<INSTALL_INTERFACE:include>
)

target_link_libraries(lovamap-proto
    PUBLIC
        protobuf::libprotobuf
)
