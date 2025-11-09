# lovamap-proto

Protocol Buffer definitions for lovamap project.

## Using as a Git Submodule

### 1. Add as submodule in your main project

```bash
git submodule add <your-repo-url> extern/lovamap-proto
git submodule update --init --recursive
```

### 2. In your main project's CMakeLists.txt

```cmake
# Add the submodule
add_subdirectory(extern/lovamap-proto)

# Link against your target
target_link_libraries(your_target
    PRIVATE
        lovamap::proto
)
```

### 3. Use in your C++ code

```cpp
#include "Descriptors.pb.h"

lovamap::Descriptors descriptors;
descriptors.set_job_id("job123");
descriptors.set_version("1.0");

auto* global_desc = descriptors.add_global_descriptors();
global_desc->set_name("example");
global_desc->set_int_value(42);
```

## Alternative Dependency Methods

### Option 1: Git Submodule (Current approach)
**Pros:**
- Simple integration
- Version control tracks exact commit
- No external dependency manager needed

**Cons:**
- Requires manual updates
- All users need to remember `git submodule update`

### Option 2: CMake FetchContent
Add to your main project's CMakeLists.txt:

```cmake
include(FetchContent)

FetchContent_Declare(
    lovamap-proto
    GIT_REPOSITORY <your-repo-url>
    GIT_TAG main  # or specific version tag
)

FetchContent_MakeAvailable(lovamap-proto)

target_link_libraries(your_target PRIVATE lovamap::proto)
```

**Pros:**
- Automatic fetching
- Easier version management
- Cleaner repository (no submodule clutter)

**Cons:**
- Downloads every configure (can use CPM.cmake to cache)
- Less control over exact version

### Option 3: Install and find_package
Install this library system-wide:

```bash
mkdir build && cd build
cmake ..
cmake --build .
sudo cmake --install .
```

Then in your main project:

```cmake
find_package(lovamap-proto REQUIRED)
target_link_libraries(your_target PRIVATE lovamap::proto)
```

**Pros:**
- Clean separation
- Shared between projects
- Professional approach

**Cons:**
- Requires installation step
- Version management per machine

## Requirements

- CMake 3.20 or higher
- Protocol Buffers compiler and libraries
- C++17 compatible compiler

## Building Standalone

```bash
mkdir build && cd build
cmake ..
cmake --build .
```

## Python Tools

### Converting Protobuf to JSON

A command-line tool is provided to convert binary protobuf files to JSON format.

#### Quick Setup (Recommended)

Run the automated setup script to install all dependencies:

```bash
cd /path/to/lovamap-proto
./setup.sh
```

The script will:
- Install `pipx` (if not already installed)
- Install `protoc` (Protocol Buffer compiler)
- Generate Python bindings from the proto file
- Install the `lvmp-pb2json` tool

**Options:**
```bash
./setup.sh --dry-run    # Preview what would be installed
./setup.sh --verbose    # Show detailed output
./setup.sh --help       # Show all options
```

#### Manual Installation

If you prefer to install manually:

1. Install `pipx` if you don't have it:
   ```bash
   # macOS
   brew install pipx
   pipx ensurepath

   # Linux
   python3 -m pip install --user pipx
   python3 -m pipx ensurepath
   ```

2. Install the Protocol Buffer compiler (`protoc`):

   **macOS:**
   ```bash
   brew install protobuf
   ```

   **Linux (Ubuntu/Debian):**
   ```bash
   sudo apt-get install protobuf-compiler
   ```

3. Install the proto-to-json tool with pipx:
   ```bash
   pipx install /path/to/lovamap-proto
   ```

4. Generate Python bindings from the proto file (one-time setup):
   ```bash
   cd /path/to/lovamap-proto
   protoc --python_out=. -I src src/Descriptors.proto
   ```

   This creates `Descriptors_pb2.py` in the root directory.

#### Usage

Once installed, the `lvmp-pb2json` command is available globally:

```bash
# Convert to JSON and print to stdout
lvmp-pb2json input.pb

# Convert to JSON file
lvmp-pb2json input.pb output.json

# Compact JSON output (no pretty-printing)
lvmp-pb2json input.pb output.json --compact
```

**Note:** Run `lvmp-pb2json` from the lovamap-proto directory (where `Descriptors_pb2.py` is located).

#### Alternative: Manual Installation

If you prefer not to use pipx:

1. Install dependencies:
   ```bash
   pip install protobuf
   ```

2. Generate Python bindings:
   ```bash
   protoc --python_out=. -I src src/Descriptors.proto
   ```

3. Run the script directly:
   ```bash
   python proto_to_json.py input.pb output.json
   ```
