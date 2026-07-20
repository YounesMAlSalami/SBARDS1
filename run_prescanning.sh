#!/bin/bash

# SBARDS Project - Pre-scanning Phase Runner for Linux
# This script runs the pre-scanning phase of the SBARDS Project on Linux

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Please install Python 3 and try again."
    exit 1
fi

# Check if pipenv is installed
if ! command -v pipenv &> /dev/null; then
    echo "Pipenv is not installed. Installing pipenv..."
    pip3 install pipenv
fi

# Create necessary directories
mkdir -p rules samples logs output scanner_core/cpp scanner_core/python

# Check if the YARA rules file exists
if [ ! -f "rules/custom_rules.yar" ]; then
    echo "YARA rules file not found. Creating a sample rules file..."
    cat > rules/custom_rules.yar << 'EOL'
rule ExampleRule
{
    meta:
        description = "This is an example rule"
        author = "SBARDS Project"
        date = "2025-05-11"

    strings:
        $text_string = "malicious" nocase
        $hex_string = { 4D 5A 90 00 }  // MZ header for PE files

    condition:
        any of them
}

rule PotentialRansomware
{
    meta:
        description = "Detects potential ransomware characteristics"
        author = "SBARDS Project"
        date = "2025-05-11"

    strings:
        $ransom_note = "your files have been encrypted" nocase
        $bitcoin = "bitcoin" nocase
        $payment = "payment" nocase
        $decrypt = "decrypt" nocase
        $encrypt = "encrypt" nocase

    condition:
        $ransom_note or ($bitcoin and $payment) or ($encrypt and $decrypt)
}
EOL
fi

# Check if the sample file exists
if [ ! -f "samples/test_sample.txt" ]; then
    echo "Sample file not found. Creating a test sample file..."
    cat > samples/test_sample.txt << 'EOL'
This is a test file that contains the word malicious to trigger our YARA rule.
It does not contain any actual malware but is used for testing the scanner functionality.

The file also mentions the words encrypt and decrypt to potentially trigger the PotentialRansomware rule.
EOL
fi

# Install dependencies
echo "Installing dependencies..."
pipenv install

# Make sure the build script is executable
chmod +x scanner_core/cpp/build_mock.sh

# Try to build the C++ scanner if possible
echo "Attempting to build C++ scanner..."
cd scanner_core/cpp
./build_mock.sh
cd ../..

# Run the pre-scanning phase
echo "Running the pre-scanning phase..."

# Pass all command-line arguments to the Python script
pipenv run python3 run_prescanning.py "$@"

echo "Pre-scanning phase complete!"
echo "Results are available in the output directory."

# Display usage information
echo ""
echo "Usage:"
echo "  ./run_prescanning.sh [file]                  # Scan a specific file"
echo "  ./run_prescanning.sh --all                   # Scan all files in samples directory"
echo "  ./run_prescanning.sh --update-rules          # Update YARA rules from remote sources"
echo "  ./run_prescanning.sh --verbose               # Enable verbose output"
echo "  ./run_prescanning.sh --no-save               # Don't save results to disk"
