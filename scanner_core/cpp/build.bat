@echo off
echo Building YARA Scanner...

REM Check if YARA is installed
where yara >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo YARA not found. Please install YARA and make sure it's in your PATH.
    exit /b 1
)

REM Compile the C++ code
cl /EHsc /Feyara_scanner.exe yara_scanner.cpp /I"C:\Program Files\YARA\include" /link "C:\Program Files\YARA\lib\libyara.lib"

if %ERRORLEVEL% NEQ 0 (
    echo Compilation failed.
    exit /b 1
)

echo Build successful. The executable is yara_scanner.exe
