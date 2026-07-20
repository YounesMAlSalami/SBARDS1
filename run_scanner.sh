#!/bin/bash
# SBARDSProject - Comprehensive Security Scanning System
# Shell script for running the scanner on Linux/macOS

# Ensure script is run from the correct directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$SCRIPT_DIR" || { echo "Failed to change to script directory"; exit 1; }

# Check for Python 3
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is required but not found. Please install Python 3 and try again."
    exit 1
fi

# Check for required Python packages
python3 -c "import yara" &> /dev/null
if [ $? -ne 0 ]; then
    echo "The 'yara-python' package is required but not installed."
    echo "Please install it using: pip install yara-python"
    exit 1
fi

python3 -c "import magic" &> /dev/null
if [ $? -ne 0 ]; then
    echo "The 'python-magic' package is required but not installed."
    echo "Please install it using: pip install python-magic"
    exit 1
fi

# Ensure required directories exist
mkdir -p logs output rules samples

# Check if running with admin privileges for certain operations
if [ "$EUID" -ne 0 ] && [ "$1" = "--admin" ]; then
    echo "Some scanning operations require administrative privileges."
    echo "Please enter your password to continue with elevated privileges."
    sudo "$0" "${@:2}"
    exit $?
fi

# Run the scanner
python3 run_scanner.py "$@"
EXIT_CODE=$?

# Display appropriate message based on exit code
if [ $EXIT_CODE -eq 0 ]; then
    echo -e "\nScan completed successfully. No threats detected."
elif [ $EXIT_CODE -eq 1 ]; then
    echo -e "\nScan completed. Threats were detected!"
    echo "Please review the scan results for details."
else
    echo -e "\nScan failed with exit code $EXIT_CODE."
    echo "Please check the logs for details."
fi

exit $EXIT_CODE
