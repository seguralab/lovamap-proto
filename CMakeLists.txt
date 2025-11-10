cmake_minimum_required(VERSION 3.20)
project(lovamap-proto VERSION 0.1.0 LANGUAGES CXX)

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Find Protobuf
find_package(Protobuf REQUIRED)
find_package(absl REQUIRED)

# Proto files
set(PROTO_FILES
    schemas/Descriptors.proto
)

# Generate C++ files from proto
protobuf_generate_cpp(PROTO_SRCS PROTO_HDRS ${PROTO_FILES})

# Create library target
add_library(lovamap-proto STATIC ${PROTO_SRCS} ${PROTO_HDRS})

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
