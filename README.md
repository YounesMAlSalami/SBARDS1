# SBARDSProject - Security Scanning System

SBARDSProject is a comprehensive security scanning system that integrates C++ performance with Python orchestration to detect threats across all file types. It provides a secure, efficient, and extensible framework for analyzing files using:

- File type detection
- Permission analysis
- Content scanning
- YARA rule-based threat detection
- Digital signature verification
- Threat intelligence integration
- Rule updating capabilities

The system is designed to work seamlessly across Windows, Linux, and macOS platforms with comprehensive test coverage and follows security best practices throughout.

## 🏗️ System Architecture

### Modular Design
The system is organized into distinct components with clear interfaces:
- **C++ Core**: High-performance modules for critical operations
- **Python Orchestrator**: Coordination and integration layer
- **Rule Management**: YARA rules for threat detection
- **Shared Utilities**: Common functions for text/file processing

### Design Principles
- **Security First**: Input validation, secure memory management, and proper error handling
- **Performance Optimized**: Efficient algorithms and minimal resource usage
- **DRY Principle**: No code duplication across components
- **Cross-Platform**: Works on Windows, Linux, and macOS
- **Extensible**: Easy to add new features and threat definitions

## 📦 Project Structure

```
SBARDSProject/
├── rules/                  # Comprehensive YARA rule files
│   ├── windows_executables.yar   # Windows executable threats
│   ├── multimedia.yar            # Multimedia file threats
│   ├── documents.yar             # Document-based threats
│   ├── archives.yar              # Archive file threats
│   ├── programming.yar           # Code-based threats
│   ├── gaming.yar                # Game file threats
│   ├── network.yar               # Network-related threats
│   ├── certificates.yar          # Certificate threats
│   └── custom_rules.yar          # User-defined rules
│
├── samples/                # Sample files for testing
│   └── test_sample.txt     # Test file for demonstrations
│
├── logs/                   # Scan history logs
│   └── scan_history.log    # Detailed scan event logs
│
├── output/                 # Scan results storage
│   └── latest_results.json # Current scan results
│
├── scanner_core/           # Core scanning components
│   ├── cpp/                # High-performance C++ components
│   │   ├── shared_utils.h         # Shared utilities header
│   │   ├── shared_utils.cpp       # Shared utilities implementation
│   │   ├── yara_scanner.h         # YARA scanner header
│   │   ├── yara_scanner.cpp       # YARA scanning engine
│   │   ├── file_analyzer.h        # File analyzer header
│   │   ├── file_analyzer.cpp      # File content analysis
│   │   ├── permission_checker.h   # Permission checker header
│   │   ├── permission_checker.cpp # Permission analysis
│   │   ├── signature_verifier.h   # Signature verifier header
│   │   ├── signature_verifier.cpp # Digital signature verification
│   │   ├── mock_scanner.cpp       # Mock scanner component
│   │   ├── mock_scanner.py        # Python mock scanner
│   │   ├── build.bat              # Windows build script
│   │   ├── build_all.bat          # Windows build all script
│   │   ├── build_mock.bat         # Windows mock build script
│   │   ├── build.sh               # Linux build script
│   │   └── build_mock.sh          # Linux mock build script
│   │
│   └── python/             # Python orchestration components
│       ├── orchestrator.py        # Main system controller
│       ├── yara_wrapper.py        # YARA integration
│       ├── file_type_detector.py  # File type identification
│       ├── rule_updater.py        # Rule management system
│       ├── threat_intel.py        # Threat intelligence integration
│       └── __init__.py            # Python package marker
│
├── run_scanner.py          # Unified execution script
├── run_scanner.sh          # Linux shell execution script
├── run_prescanning.py      # Pre-scanning execution script
└── run_prescanning.sh      # Pre-scanning shell script
```

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- Pipenv (for dependency management)
- C++ compiler (for building C++ components)
- YARA library (optional for full functionality)

### Installation

#### Method 1: Using pip

```bash
# Install from PyPI (when published)
pip install sbards-scanner

# Install from local directory
pip install .
```

#### Method 2: Manual Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/SBARDSProject.git
cd SBARDSProject
```

2. Install dependencies:

**Using Pipenv (recommended)**:
```bash
pip install pipenv
pipenv install
```

**Using pip with requirements.txt**:
```bash
pip install -r requirements.txt
```

**Installing dependencies manually**:
```bash
pip install yara-python python-magic requests colorama
```

Note: On Windows, you might need additional steps for python-magic:
```bash
pip install python-magic-bin
```

3. Build C++ components (optional):
```bash
# On Windows
cd scanner_core/cpp
build_all.bat

# On Linux
cd scanner_core/cpp
chmod +x build.sh
./build.sh

# For mock scanner only
# On Windows
cd scanner_core/cpp
build_mock.bat

# On Linux
cd scanner_core/cpp
chmod +x build_mock.sh
./build_mock.sh
```

### Configuration

The scanner can be configured using the `config.json` file. This file contains settings for:

- Scanner information
- Directory paths
- Scan options
- YARA settings
- File type filtering
- Threat intelligence integration
- Reporting options
- Logging settings
- Action settings

Example configuration:

```json
{
  "scanner": {
    "version": "1.0.0",
    "name": "SBARDS Security Scanner",
    "description": "Comprehensive Security Analysis Tool"
  },
  "paths": {
    "rules_dir": "rules",
    "samples_dir": "samples",
    "output_dir": "output",
    "logs_dir": "logs"
  },
  "scan_options": {
    "max_file_size": 104857600,
    "default_recursive": false,
    "parallel_scan": true,
    "max_workers": 0,
    "timeout_seconds": 300
  }
}
```

You can customize these settings to match your requirements.

### Running the Scanner

```bash
# Basic file scanning
python run_scanner.py samples/test_sample.txt

# Scan with verbose output
python run_scanner.py samples/test_sample.txt --verbose

# Scan all files in samples directory
python run_scanner.py --all

# Update YARA rules before scanning
python run_scanner.py --update-rules

# Scan directory recursively
python run_scanner.py /path/to/directory --recursive

# Save results to a specific file
python run_scanner.py samples/test_sample.txt --output results.json

# On Linux/macOS
./run_scanner.sh samples/test_sample.txt
```

### Running the Tests

```bash
# Run all tests
python run_tests.py

# Run tests with verbose output
python run_tests.py --verbose

# Run specific tests matching a pattern
python run_tests.py --pattern TestOrchestrator

# List available tests without running them
python run_tests.py --list
```

### Running the Pre-scanning Tool

```bash
# On Windows
python run_prescanning.py

# On Linux
./run_prescanning.sh
```

## 🔍 Features

- **File Type Detection**: Accurately identifies file types using multiple methods
- **Permission Analysis**: Checks file permissions for suspicious settings
- **Content Scanning**: Analyzes file content for malicious patterns
- **YARA Integration**: Uses YARA rules for advanced threat detection
- **Threat Intelligence**: Checks files against threat intelligence sources
- **Cross-Platform**: Works on Windows, Linux, and macOS
- **Extensible**: Easy to add new rules and scanning capabilities

## 📚 Documentation

For detailed documentation, please refer to the following files:

- [README.md](README.md): Project overview and getting started guide
- [DOCUMENTATION.md](DOCUMENTATION.md): Detailed system documentation
- [PRESCANNING_PHASE_DOCUMENTATION.md](PRESCANNING_PHASE_DOCUMENTATION.md): Pre-scanning phase documentation
- [ProjectWorkflowGPTdocm.md](ProjectWorkflowGPTdocm.md): Comprehensive workflow documentation

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.
