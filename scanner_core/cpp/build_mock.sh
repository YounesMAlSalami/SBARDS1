#!/bin/bash
echo "Building Mock YARA Scanner..."

# Create build directory if it doesn't exist
mkdir -p build

# Check if g++ is available
if command -v g++ &> /dev/null; then
    echo "Using g++ compiler..."
    g++ -std=c++17 -o build/mock_scanner mock_scanner.cpp
elif command -v clang++ &> /dev/null; then
    echo "Using clang++ compiler..."
    clang++ -std=c++17 -o build/mock_scanner mock_scanner.cpp
else
    echo "No C++ compiler found. Please install g++ or clang++."
    exit 1
fi

if [ $? -ne 0 ]; then
    echo "Compilation failed."
    exit 1
fi

# Copy the executable to the current directory for backward compatibility
cp build/mock_scanner ./mock_scanner

# Make the executables executable
chmod +x build/mock_scanner
chmod +x mock_scanner

echo "Build successful. The executable is in build/mock_scanner and ./mock_scanner"
