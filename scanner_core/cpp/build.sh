#!/bin/bash
# Build script for C++ components of SBARDSProject
# This script compiles and links all C++ components of the project

# Set color codes for better output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print banner
echo -e "${BLUE}=======================================${NC}"
echo -e "${BLUE}  SBARDSProject C++ Component Builder  ${NC}"
echo -e "${BLUE}=======================================${NC}"

# Ensure script is run from the correct directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$SCRIPT_DIR" || { echo -e "${RED}Failed to change to script directory${NC}"; exit 1; }
echo -e "${GREEN}Working directory: ${SCRIPT_DIR}${NC}"

# Check for required tools
echo -e "${BLUE}Checking for required tools...${NC}"
command -v g++ >/dev/null 2>&1 || { echo -e "${RED}Error: g++ is required but not installed. Aborting.${NC}"; exit 1; }
command -v pkg-config >/dev/null 2>&1 || { echo -e "${RED}Error: pkg-config is required but not installed. Aborting.${NC}"; exit 1; }
echo -e "${GREEN}Required tools found.${NC}"

# Check for YARA library
echo -e "${BLUE}Checking for YARA library...${NC}"
if pkg-config --exists yara; then
    YARA_VERSION=$(pkg-config --modversion yara)
    echo -e "${GREEN}YARA library found (version: ${YARA_VERSION}).${NC}"
else
    echo -e "${YELLOW}Warning: YARA library not found. Will build without YARA support.${NC}"
    echo -e "${YELLOW}To enable YARA support, install libyara-dev package.${NC}"
    echo -e "${YELLOW}On Ubuntu/Debian: sudo apt-get install libyara-dev${NC}"
    echo -e "${YELLOW}On Fedora/RHEL: sudo dnf install yara-devel${NC}"
    echo -e "${YELLOW}On macOS: brew install yara${NC}"
    YARA_SUPPORT=0
fi

# Create build directory
echo -e "${BLUE}Creating build directory...${NC}"
mkdir -p build
echo -e "${GREEN}Build directory created.${NC}"

# Set compiler flags
CXXFLAGS="-std=c++17 -Wall -Wextra -pedantic -O2 -fPIC"
LDFLAGS=""

# Check for OpenSSL
echo -e "${BLUE}Checking for OpenSSL...${NC}"
if pkg-config --exists openssl; then
    OPENSSL_VERSION=$(pkg-config --modversion openssl)
    echo -e "${GREEN}OpenSSL found (version: ${OPENSSL_VERSION}).${NC}"
    CXXFLAGS="$CXXFLAGS $(pkg-config --cflags openssl)"
    LDFLAGS="$LDFLAGS $(pkg-config --libs openssl)"
else
    echo -e "${YELLOW}Warning: OpenSSL not found. Signature verification will be limited.${NC}"
fi

# Compile shared utilities
echo -e "${BLUE}Compiling shared_utils.cpp...${NC}"
g++ $CXXFLAGS -c -o build/shared_utils.o shared_utils.cpp
if [ $? -ne 0 ]; then
    echo -e "${RED}Error: Failed to compile shared_utils.cpp${NC}"
    exit 1
fi
echo -e "${GREEN}Successfully compiled shared_utils.cpp${NC}"

# Compile file analyzer
echo -e "${BLUE}Compiling file_analyzer.cpp...${NC}"
g++ $CXXFLAGS -c -o build/file_analyzer.o file_analyzer.cpp
if [ $? -ne 0 ]; then
    echo -e "${RED}Error: Failed to compile file_analyzer.cpp${NC}"
    exit 1
fi
echo -e "${GREEN}Successfully compiled file_analyzer.cpp${NC}"

# Compile permission checker
echo -e "${BLUE}Compiling permission_checker.cpp...${NC}"
g++ $CXXFLAGS -c -o build/permission_checker.o permission_checker.cpp
if [ $? -ne 0 ]; then
    echo -e "${RED}Error: Failed to compile permission_checker.cpp${NC}"
    exit 1
fi
echo -e "${GREEN}Successfully compiled permission_checker.cpp${NC}"

# Compile signature verifier
echo -e "${BLUE}Compiling signature_verifier.cpp...${NC}"
g++ $CXXFLAGS -c -o build/signature_verifier.o signature_verifier.cpp
if [ $? -ne 0 ]; then
    echo -e "${RED}Error: Failed to compile signature_verifier.cpp${NC}"
    exit 1
fi
echo -e "${GREEN}Successfully compiled signature_verifier.cpp${NC}"

# Compile YARA scanner if YARA is available
if pkg-config --exists yara; then
    echo -e "${BLUE}Compiling yara_scanner.cpp...${NC}"
    g++ $CXXFLAGS $(pkg-config --cflags yara) -c -o build/yara_scanner.o yara_scanner.cpp
    if [ $? -ne 0 ]; then
        echo -e "${RED}Error: Failed to compile yara_scanner.cpp${NC}"
        exit 1
    fi
    echo -e "${GREEN}Successfully compiled yara_scanner.cpp${NC}"

    # Link YARA scanner executable
    echo -e "${BLUE}Linking yara_scanner executable...${NC}"
    g++ -o build/yara_scanner build/yara_scanner.o build/shared_utils.o $LDFLAGS $(pkg-config --libs yara)
    if [ $? -ne 0 ]; then
        echo -e "${RED}Error: Failed to link yara_scanner executable${NC}"
        exit 1
    fi
    echo -e "${GREEN}Successfully linked yara_scanner executable${NC}"
else
    echo -e "${YELLOW}Skipping YARA scanner compilation (YARA library not found).${NC}"
fi

# Link file analyzer executable
echo -e "${BLUE}Linking file_analyzer executable...${NC}"
g++ -o build/file_analyzer build/file_analyzer.o build/shared_utils.o $LDFLAGS
if [ $? -ne 0 ]; then
    echo -e "${RED}Error: Failed to link file_analyzer executable${NC}"
    exit 1
fi
echo -e "${GREEN}Successfully linked file_analyzer executable${NC}"

# Link permission checker executable
echo -e "${BLUE}Linking permission_checker executable...${NC}"
g++ -o build/permission_checker build/permission_checker.o build/shared_utils.o $LDFLAGS
if [ $? -ne 0 ]; then
    echo -e "${RED}Error: Failed to link permission_checker executable${NC}"
    exit 1
fi
echo -e "${GREEN}Successfully linked permission_checker executable${NC}"

# Link signature verifier executable
echo -e "${BLUE}Linking signature_verifier executable...${NC}"
g++ -o build/signature_verifier build/signature_verifier.o build/shared_utils.o $LDFLAGS
if [ $? -ne 0 ]; then
    echo -e "${RED}Error: Failed to link signature_verifier executable${NC}"
    exit 1
fi
echo -e "${GREEN}Successfully linked signature_verifier executable${NC}"

# Create a combined library
echo -e "${BLUE}Creating combined library...${NC}"
g++ -shared -o build/libsbards.so build/shared_utils.o build/file_analyzer.o build/permission_checker.o build/signature_verifier.o $LDFLAGS
if [ $? -ne 0 ]; then
    echo -e "${RED}Error: Failed to create combined library${NC}"
    exit 1
fi
echo -e "${GREEN}Successfully created combined library${NC}"

# Make executables executable
chmod +x build/file_analyzer build/permission_checker build/signature_verifier
if pkg-config --exists yara; then
    chmod +x build/yara_scanner
fi

echo -e "${BLUE}=======================================${NC}"
echo -e "${GREEN}Build completed successfully!${NC}"
echo -e "${BLUE}=======================================${NC}"
echo -e "${YELLOW}Executables can be found in the build directory:${NC}"
ls -la build/
