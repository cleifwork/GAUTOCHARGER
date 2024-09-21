@echo off

REM Attempt to find the default Desktop path
set DefaultDesktopPath=%USERPROFILE%\Desktop

REM Check if the GAUTOCHARGER folder exists on the default Desktop
echo Checking Default Desktop: %DefaultDesktopPath%\GAUTOCHARGER
if exist "%DefaultDesktopPath%\GAUTOCHARGER" (
    echo GAUTOCHARGER folder found on default Desktop.
    start "" "python.exe" "%DefaultDesktopPath%\GAUTOCHARGER\GAutoCharger.py" %*
    exit /b
) else (
    echo GAUTOCHARGER folder not found on default Desktop.
)

REM Initialize OneDrivePath variable
set OneDrivePath=

REM Check if the OneDrive environment variable is set (for personal OneDrive accounts)
if defined OneDrive (
    set OneDrivePath=%OneDrive%
    echo Found OneDrive personal path: %OneDrivePath%
) else if defined OneDriveCommercial (
    REM Check for OneDriveCommercial (for business/organization accounts)
    set OneDrivePath=%OneDriveCommercial%
    echo Found OneDrive commercial path: %OneDrivePath%
) else (
    REM Attempt to retrieve the OneDrive path from the Windows registry
    echo Checking OneDrive path from registry...
    for /f "tokens=3*" %%A in ('reg query "HKEY_CURRENT_USER\Software\Microsoft\OneDrive" /v "UserFolder" 2^>nul') do set OneDrivePath=%%A %%B
)

REM Debug output to confirm if OneDrivePath was found
if defined OneDrivePath (
    echo OneDrive path resolved to: %OneDrivePath%
) else (
    echo ERROR: OneDrive path could not be found.
    pause
    exit /b
)

REM Append \Desktop to the OneDrivePath and check for GAUTOCHARGER folder
set DesktopPath=%OneDrivePath%\Desktop
echo Checking OneDrive Desktop: %DesktopPath%\GAUTOCHARGER

if exist "%DesktopPath%\GAUTOCHARGER" (
    echo GAUTOCHARGER folder found on OneDrive Desktop.
    start "" "python.exe" "%DesktopPath%\GAUTOCHARGER\GAutoCharger.py" %*
    exit /b
) else (
    echo GAUTOCHARGER folder not found on OneDrive Desktop.
    pause
    exit /b
)