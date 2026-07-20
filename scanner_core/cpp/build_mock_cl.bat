@echo off
echo Building Mock YARA Scanner with MSVC...

REM Compile the C++ code with cl
cl /EHsc /Femock_scanner.exe mock_scanner.cpp

if %ERRORLEVEL% NEQ 0 (
    echo Compilation failed.
    exit /b 1
)

echo Build successful. The executable is mock_scanner.exe
