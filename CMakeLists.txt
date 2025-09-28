cmake_minimum_required(VERSION 3.10)
project(RiseBlockchainRSDT)

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Find required packages
find_package(Boost 1.71 REQUIRED COMPONENTS system filesystem thread)
find_package(OpenSSL REQUIRED)

# Include directories
include_directories(
    ${Boost_INCLUDE_DIRS}
    ${OPENSSL_INCLUDE_DIR}
    include/
)

# Source files
file(GLOB_RECURSE SOURCES "src/*.cpp")

# Executable
add_executable(rsdt-blockchain ${SOURCES})

# Link libraries
target_link_libraries(rsdt-blockchain
    ${Boost_LIBRARIES}
    ${OPENSSL_LIBRARIES}
    pthread
)

# Installinstall(TARGETS rsdt-blockchain DESTINATION bin)
