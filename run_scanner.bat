@echo off
REM SBARDSProject - Comprehensive Security Scanning System
REM Windows batch script for running the scanner

REM Ensure script is run from the correct directory
cd /d "%~dp0"

REM Check for Python 3
python --version 2>nul | findstr /r "^Python 3" >nul
if %ERRORLEVEL% NEQ 0 (
    echo Python 3 is required but not found. Please install Python 3 and try again.
    exit /b 1
)

REM Check for required Python packages
python -c "import yara" 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo The 'yara-python' package is required but not installed.
    echo Please install it using: pip install yara-python
    echo If you continue, the scanner will run with limited functionality.
)

python -c "import magic" 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo The 'python-magic' package is required but not installed.
    echo Please install it using: pip install python-magic python-magic-bin
    echo If you continue, the scanner will run with limited functionality.
)

python -c "import requests" 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo The 'requests' package is required but not installed.
    echo Please install it using: pip install requests
    echo If you continue, the scanner will run with limited functionality.
)

REM Ensure required directories exist
if not exist logs mkdir logs
if not exist output mkdir output
if not exist rules mkdir rules
if not exist samples mkdir samples

REM Build C++ scanner if needed
if not exist scanner_core\cpp\mock_scanner.exe (
    echo Building C++ scanner...
    cd scanner_core\cpp
    call build_mock.bat
    cd ..\..
)

REM Run the scanner
python run_scanner.py %*

REM Display appropriate message based on exit code
if %ERRORLEVEL% EQU 0 (
    echo.
    echo Scan completed successfully. No threats detected.
) else if %ERRORLEVEL% EQU 1 (
    echo.
    echo Scan completed. Threats were detected!
    echo Please review the scan results for details.
) else (
    echo.
    echo Scan failed with exit code %ERRORLEVEL%.
    echo Please check the logs for details.
)

exit /b %ERRORLEVEL%
