# SBARDS Project - Pre-scanning Phase Documentation

This document provides detailed information about running the pre-scanning phase of the SBARDS Project, which involves both C++ and Python components. The project is designed to be cross-platform, supporting both Windows and Linux environments.

## Project Structure

The pre-scanning phase consists of the following components:

- **C++ YARA Scanner**: A C++ component that uses the YARA library to scan files for malicious patterns.
- **Python Orchestrator**: A Python component that orchestrates the scanning process, manages file operations, and logs results.
- **Integration**: A script that integrates both components to perform the complete pre-scanning phase.

## Prerequisites

- Python 3.8 or later (Windows: `python`, Linux: `python3`)
- pipenv (for Python dependency management)
- YARA library (for the C++ component)
- C++ compiler (Windows: MSVC or MinGW, Linux: GCC)

## Directory Structure

```
SBARDSProject/
├── rules/                  # Contains YARA rule files
│   └── custom_rules.yar    # Custom YARA rules for malware detection
├── samples/                # Contains files to be scanned
│   └── test_sample.txt     # Test sample file
├── logs/                   # Contains scan logs
├── output/                 # Contains scan results in JSON format
├── scanner_core/           # Core scanning components
│   ├── cpp/                # C++ scanner component
│   │   ├── yara_scanner.cpp    # Original C++ YARA scanner
│   │   ├── mock_scanner.cpp    # Mock C++ scanner
│   │   ├── mock_scanner.py     # Python mock scanner for demonstration
│   │   ├── build_mock.bat      # Windows build script
│   │   └── build_mock.sh       # Linux build script
│   └── python/             # Python orchestrator component
│       ├── orchestrator.py     # Main orchestrator script
│       └── yara_wrapper.py     # Python wrapper for YARA
├── run_prescanning.py      # Cross-platform script to run the integrated pre-scanning phase
└── run_prescanning.sh      # Shell script for Linux users
```

## Cross-Platform Compatibility

The project has been designed to work seamlessly on both Windows and Linux platforms:

- **Path Handling**: All file paths use `os.path.join()` for cross-platform compatibility
- **File Operations**: File operations use proper encoding and error handling
- **Build Scripts**: Separate build scripts for Windows (.bat) and Linux (.sh)
- **Process Execution**: Platform-specific command detection and execution

## Running the Components Separately

### 1. C++ YARA Scanner

The C++ YARA scanner is designed to scan individual files using YARA rules. It requires the YARA library to be installed.

**Building the C++ Scanner on Windows:**

```bash
cd scanner_core\cpp
build_mock.bat
```

**Building the C++ Scanner on Linux:**

```bash
cd scanner_core/cpp
chmod +x build_mock.sh
./build_mock.sh
```

**Running the C++ Scanner on Windows:**

```bash
mock_scanner.exe <rules_file> <target_file>
```

**Running the C++ Scanner on Linux:**

```bash
./mock_scanner <rules_file> <target_file>
```

For demonstration purposes, we've created a mock scanner in Python that simulates the behavior of the C++ scanner:

**On Windows:**
```bash
python scanner_core\cpp\mock_scanner.py rules\custom_rules.yar samples\test_sample.txt
```

**On Linux:**
```bash
python3 scanner_core/cpp/mock_scanner.py rules/custom_rules.yar samples/test_sample.txt
```

### 2. Python Orchestrator

The Python orchestrator manages the scanning process, including file operations and result logging.

**Setting up the Python Environment:**

**On Windows:**
```bash
pip install pipenv
pipenv install
```

**On Linux:**
```bash
pip3 install pipenv
pipenv install
```

**Running the Python Orchestrator:**

**On Windows:**
```bash
pipenv run python scanner_core\python\orchestrator.py
```

**On Linux:**
```bash
pipenv run python3 scanner_core/python/orchestrator.py
```

## Running the Integrated Pre-scanning Phase

The integrated pre-scanning phase combines both the C++ scanner and Python orchestrator to perform a complete scan.

**On Windows:**
```bash
python run_prescanning.py
```

**On Linux:**
```bash
chmod +x run_prescanning.sh
./run_prescanning.sh
```

This script performs the following steps:

1. Runs the C++ scanner on a test file
2. Runs the Python orchestrator
3. Runs an integrated scan that uses the C++ scanner for file scanning and Python for orchestration

## Output and Logs

- Scan logs are stored in the `logs/` directory
- Scan results in JSON format are stored in the `output/` directory

## Best Practices for Cross-Platform Development

1. **Path Handling**: Always use `os.path.join()` for constructing file paths
2. **File Encoding**: Specify UTF-8 encoding when reading/writing files
3. **Error Handling**: Implement robust error handling for both platforms
4. **Platform Detection**: Use `platform.system()` to detect the operating system
5. **Command Execution**: Handle platform-specific command differences
6. **Build Scripts**: Provide separate build scripts for each platform
7. **Documentation**: Document platform-specific instructions clearly

## Troubleshooting

### Windows-Specific Issues

- **YARA Library Not Found**: Ensure the YARA library is installed and properly configured in your PATH
- **Python Command**: Use `python` instead of `python3`
- **Path Separators**: Windows uses backslashes (`\`) in paths

### Linux-Specific Issues

- **File Permissions**: Ensure scripts have execute permissions (`chmod +x script.sh`)
- **Python Command**: Use `python3` instead of `python`
- **Path Separators**: Linux uses forward slashes (`/`) in paths

### General Issues

- **Python Dependencies**: Use pipenv to manage Python dependencies
- **File Permissions**: Ensure the scanner has appropriate permissions to access files
- **Path Issues**: Use absolute paths when necessary to avoid path-related issues

## Next Steps

After the pre-scanning phase, the project will proceed to:

1. **Analysis Phase**: Analyze the scan results to identify potential threats
2. **Remediation Phase**: Take appropriate actions based on the analysis
3. **Reporting Phase**: Generate comprehensive reports on the scanning process and results

## 📚 Additional Documentation

For more detailed information about the project workflow and implementation details, please refer to:

- [README.md](README.md): Project overview and getting started guide
- [DOCUMENTATION.md](DOCUMENTATION.md): Detailed system documentation
- [ProjectWorkflowGPTdocm.md](ProjectWorkflowGPTdocm.md): Comprehensive workflow documentation
