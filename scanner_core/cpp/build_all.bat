@echo off
REM Build script for C++ components of SBARDSProject on Windows
REM This script compiles and links all C++ components of the project

REM Set color codes for better output
set RED=[91m
set GREEN=[92m
set YELLOW=[93m
set BLUE=[94m
set NC=[0m

REM Print banner
echo %BLUE%=======================================%NC%
echo %BLUE%  SBARDSProject C++ Component Builder  %NC%
echo %BLUE%=======================================%NC%

REM Create build directory
if not exist build (
    echo %BLUE%Creating build directory...%NC%
    mkdir build
    echo %GREEN%Build directory created.%NC%
) else (
    echo %BLUE%Build directory already exists.%NC%
)

REM Check for MSVC compiler
echo %BLUE%Checking for MSVC compiler...%NC%
where cl >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo %RED%Error: MSVC compiler (cl.exe) not found in PATH.%NC%
    echo %RED%Please run this script from a Visual Studio Developer Command Prompt.%NC%
    echo.
    echo %YELLOW%To open a Developer Command Prompt:%NC%
    echo %YELLOW%1. Start Menu -^> Visual Studio -^> Developer Command Prompt%NC%
    echo %YELLOW%2. Navigate to this directory%NC%
    echo %YELLOW%3. Run this script again%NC%
    exit /b 1
)
echo %GREEN%MSVC compiler found.%NC%

REM Set compiler flags
set CXXFLAGS=/c /EHsc /std:c++17 /W4 /O2 /MD /Fo"build\\"
set LDFLAGS=

REM Check for OpenSSL
echo %BLUE%Checking for OpenSSL...%NC%
if exist "%OPENSSL_ROOT%\include\openssl\ssl.h" (
    echo %GREEN%OpenSSL found at %OPENSSL_ROOT%.%NC%
    set CXXFLAGS=%CXXFLAGS% /I"%OPENSSL_ROOT%\include"
    set LDFLAGS=%LDFLAGS% /LIBPATH:"%OPENSSL_ROOT%\lib" libssl.lib libcrypto.lib
) else (
    echo %YELLOW%Warning: OpenSSL not found. Signature verification will be limited.%NC%
    echo %YELLOW%Set OPENSSL_ROOT environment variable to your OpenSSL installation path.%NC%
)

REM Try to find YARA automatically
echo %BLUE%Looking for YARA installation...%NC%
set YARA_FOUND=0

REM Check if YARA_ROOT environment variable is set
if defined YARA_ROOT (
    if exist "%YARA_ROOT%\include\yara.h" (
        set YARA_INCLUDE=%YARA_ROOT%\include
        set YARA_LIB=%YARA_ROOT%\lib
        set YARA_FOUND=1
        echo %GREEN%YARA found at %YARA_ROOT%.%NC%
    )
)

REM Check common installation paths if not found yet
if %YARA_FOUND% equ 0 (
    if exist "C:\yara\include\yara.h" (
        set YARA_INCLUDE=C:\yara\include
        set YARA_LIB=C:\yara\lib
        set YARA_FOUND=1
        echo %GREEN%YARA found at C:\yara.%NC%
    ) else if exist "C:\Program Files\yara\include\yara.h" (
        set YARA_INCLUDE=C:\Program Files\yara\include
        set YARA_LIB=C:\Program Files\yara\lib
        set YARA_FOUND=1
        echo %GREEN%YARA found at C:\Program Files\yara.%NC%
    ) else if exist "C:\Program Files (x86)\yara\include\yara.h" (
        set YARA_INCLUDE=C:\Program Files (x86)\yara\include
        set YARA_LIB=C:\Program Files (x86)\yara\lib
        set YARA_FOUND=1
        echo %GREEN%YARA found at C:\Program Files (x86)\yara.%NC%
    )
)

REM If YARA not found, allow user to specify paths
if %YARA_FOUND% equ 0 (
    echo %YELLOW%YARA not found automatically.%NC%
    echo %YELLOW%You can set YARA paths manually:%NC%

    set /p YARA_INCLUDE=Enter YARA include path (or press Enter to skip YARA support):
    if not "%YARA_INCLUDE%"=="" (
        set /p YARA_LIB=Enter YARA library path:

        if exist "%YARA_INCLUDE%\yara.h" (
            if exist "%YARA_LIB%\libyara.lib" (
                set YARA_FOUND=1
                echo %GREEN%YARA paths set manually.%NC%
            ) else (
                echo %RED%YARA library not found at %YARA_LIB%\libyara.lib%NC%
            )
        ) else (
            echo %RED%YARA header not found at %YARA_INCLUDE%\yara.h%NC%
        )
    ) else (
        echo %YELLOW%Building without YARA support.%NC%
    )
)

REM Compile shared utilities
echo %BLUE%Compiling shared_utils.cpp...%NC%
cl %CXXFLAGS% shared_utils.cpp
if %ERRORLEVEL% neq 0 (
    echo %RED%Error: Failed to compile shared_utils.cpp%NC%
    exit /b 1
)
echo %GREEN%Successfully compiled shared_utils.cpp%NC%

REM Compile file analyzer
echo %BLUE%Compiling file_analyzer.cpp...%NC%
cl %CXXFLAGS% file_analyzer.cpp
if %ERRORLEVEL% neq 0 (
    echo %RED%Error: Failed to compile file_analyzer.cpp%NC%
    exit /b 1
)
echo %GREEN%Successfully compiled file_analyzer.cpp%NC%

REM Compile permission checker
echo %BLUE%Compiling permission_checker.cpp...%NC%
cl %CXXFLAGS% permission_checker.cpp
if %ERRORLEVEL% neq 0 (
    echo %RED%Error: Failed to compile permission_checker.cpp%NC%
    exit /b 1
)
echo %GREEN%Successfully compiled permission_checker.cpp%NC%

REM Compile signature verifier
echo %BLUE%Compiling signature_verifier.cpp...%NC%
cl %CXXFLAGS% signature_verifier.cpp
if %ERRORLEVEL% neq 0 (
    echo %RED%Error: Failed to compile signature_verifier.cpp%NC%
    exit /b 1
)
echo %GREEN%Successfully compiled signature_verifier.cpp%NC%

REM Compile YARA scanner if YARA is available
if %YARA_FOUND% equ 1 (
    echo %BLUE%Compiling yara_scanner.cpp...%NC%
    cl %CXXFLAGS% /I"%YARA_INCLUDE%" yara_scanner.cpp
    if %ERRORLEVEL% neq 0 (
        echo %RED%Error: Failed to compile yara_scanner.cpp%NC%
        exit /b 1
    )
    echo %GREEN%Successfully compiled yara_scanner.cpp%NC%

    REM Link YARA scanner executable
    echo %BLUE%Linking yara_scanner executable...%NC%
    cl /EHsc /Fe"build\yara_scanner.exe" build\yara_scanner.obj build\shared_utils.obj %LDFLAGS% /link /LIBPATH:"%YARA_LIB%" libyara.lib
    if %ERRORLEVEL% neq 0 (
        echo %RED%Error: Failed to link yara_scanner executable%NC%
        exit /b 1
    )
    echo %GREEN%Successfully linked yara_scanner executable%NC%
) else (
    echo %YELLOW%Skipping YARA scanner compilation (YARA library not found).%NC%
)

REM Link file analyzer executable
echo %BLUE%Linking file_analyzer executable...%NC%
cl /EHsc /Fe"build\file_analyzer.exe" build\file_analyzer.obj build\shared_utils.obj %LDFLAGS%
if %ERRORLEVEL% neq 0 (
    echo %RED%Error: Failed to link file_analyzer executable%NC%
    exit /b 1
)
echo %GREEN%Successfully linked file_analyzer executable%NC%

REM Link permission checker executable
echo %BLUE%Linking permission_checker executable...%NC%
cl /EHsc /Fe"build\permission_checker.exe" build\permission_checker.obj build\shared_utils.obj %LDFLAGS%
if %ERRORLEVEL% neq 0 (
    echo %RED%Error: Failed to link permission_checker executable%NC%
    exit /b 1
)
echo %GREEN%Successfully linked permission_checker executable%NC%

REM Link signature verifier executable
echo %BLUE%Linking signature_verifier executable...%NC%
cl /EHsc /Fe"build\signature_verifier.exe" build\signature_verifier.obj build\shared_utils.obj %LDFLAGS%
if %ERRORLEVEL% neq 0 (
    echo %RED%Error: Failed to link signature_verifier executable%NC%
    exit /b 1
)
echo %GREEN%Successfully linked signature_verifier executable%NC%

REM Create a combined library
echo %BLUE%Creating combined library...%NC%
lib /OUT:build\sbards.lib build\shared_utils.obj build\file_analyzer.obj build\permission_checker.obj build\signature_verifier.obj
if %ERRORLEVEL% neq 0 (
    echo %RED%Error: Failed to create combined library%NC%
    exit /b 1
)
echo %GREEN%Successfully created combined library%NC%

echo %BLUE%=======================================%NC%
echo %GREEN%Build completed successfully!%NC%
echo %BLUE%=======================================%NC%
echo %YELLOW%Executables can be found in the build directory:%NC%
dir /b build\*.exe
echo.
echo %YELLOW%Libraries can be found in the build directory:%NC%
dir /b build\*.lib
