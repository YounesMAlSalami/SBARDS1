@echo off
echo Building Mock YARA Scanner...

REM Create build directory if it doesn't exist
if not exist "build" mkdir build

REM Try to find Visual Studio compiler
set FOUND_COMPILER=0

REM Check for Visual Studio 2022
if exist "C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvars64.bat" (
    echo Using Visual Studio 2022 Community...
    call "C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvars64.bat"
    cl /EHsc /std:c++17 /Febuild\mock_scanner.exe mock_scanner.cpp
    set FOUND_COMPILER=1
) else if exist "C:\Program Files\Microsoft Visual Studio\2022\Professional\VC\Auxiliary\Build\vcvars64.bat" (
    echo Using Visual Studio 2022 Professional...
    call "C:\Program Files\Microsoft Visual Studio\2022\Professional\VC\Auxiliary\Build\vcvars64.bat"
    cl /EHsc /std:c++17 /Febuild\mock_scanner.exe mock_scanner.cpp
    set FOUND_COMPILER=1
) else if exist "C:\Program Files\Microsoft Visual Studio\2022\Enterprise\VC\Auxiliary\Build\vcvars64.bat" (
    echo Using Visual Studio 2022 Enterprise...
    call "C:\Program Files\Microsoft Visual Studio\2022\Enterprise\VC\Auxiliary\Build\vcvars64.bat"
    cl /EHsc /std:c++17 /Febuild\mock_scanner.exe mock_scanner.cpp
    set FOUND_COMPILER=1
)

REM Check for Visual Studio 2019
if %FOUND_COMPILER% EQU 0 (
    if exist "C:\Program Files (x86)\Microsoft Visual Studio\2019\BuildTools\VC\Auxiliary\Build\vcvars64.bat" (
        echo Using Visual Studio 2019 BuildTools...
        call "C:\Program Files (x86)\Microsoft Visual Studio\2019\BuildTools\VC\Auxiliary\Build\vcvars64.bat"
        cl /EHsc /std:c++17 /Febuild\mock_scanner.exe mock_scanner.cpp
        set FOUND_COMPILER=1
    ) else if exist "C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC\Auxiliary\Build\vcvars64.bat" (
        echo Using Visual Studio 2019 Community...
        call "C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC\Auxiliary\Build\vcvars64.bat"
        cl /EHsc /std:c++17 /Febuild\mock_scanner.exe mock_scanner.cpp
        set FOUND_COMPILER=1
    )
)

REM Try MinGW/GCC if Visual Studio not found
if %FOUND_COMPILER% EQU 0 (
    echo Visual Studio not found, trying MinGW/GCC...
    where g++ >nul 2>&1
    if %ERRORLEVEL% EQU 0 (
        echo Using GCC...
        g++ -std=c++17 -o build\mock_scanner.exe mock_scanner.cpp
        set FOUND_COMPILER=1
    )
)

REM Check if compilation was successful
if %FOUND_COMPILER% EQU 0 (
    echo No C++ compiler found. Please install Visual Studio or MinGW.
    exit /b 1
)

if %ERRORLEVEL% NEQ 0 (
    echo Compilation failed.
    exit /b 1
)

REM Copy the executable to the current directory for backward compatibility
copy /Y build\mock_scanner.exe mock_scanner.exe

echo Build successful. The executable is in build\mock_scanner.exe and mock_scanner.exe
