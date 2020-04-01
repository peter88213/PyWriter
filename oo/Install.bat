@echo off
REM Installation script for the PyWriter Tools software package.
REM 
REM See: https://github.com/peter88213/PyWriter
REM License: The MIT License (https://opensource.org/licenses/mit-license.php)
REM Copyright: (c) 2020, Peter Triesberger
REM 
REM Note: This script is to be executed manually after un-packing the setup file.
REM 
REM Preconditions:
REM * Setup folder structure must exist in the working directory.
REM * OpenOffice 3.x or 4.x is installed.
REM
REM Postconditions: 
REM * The PyWriter Tools Python scripts are installed in the OpenOffice user profile.
REM * The OpenOffice extension "WriteYw-<version>" is installed.
REM * For yWriter7 files, there is an Explorer context menu entry "PyWriter Tools".

set _release=0.9.5

pushd setup

set _OpenOffice4_w64=c:\Program Files (x86)\OpenOffice 4
set _OpenOffice4_w32=c:\Program Files\OpenOffice 4
set _OpenOffice3_w64=c:\Program Files (x86)\OpenOffice.org 3
set _OpenOffice3_w32=c:\Program Files\OpenOffice.org 3

set _OpenOffice4_Userprofile=AppData\Roaming\OpenOffice\4\user
set _OpenOffice3_Userprofile=AppData\Roaming\OpenOffice.org\3\user



echo -----------------------------------------------------------------
echo PyWriter (yWriter to LibreOffice) v%_release%
echo Installing software package ...
echo -----------------------------------------------------------------

rem Detect combination of Windows and Office 

if exist "%_OpenOffice4_w64%\program\swriter.exe" goto OpenOffice4-Win64
if exist "%_OpenOffice4_w32%\program\swriter.exe" goto OpenOffice4-Win32
if exist "%_OpenOffice3_w64%\program\swriter.exe" goto OpenOffice3-Win64
if exist "%_OpenOffice3_w32%\program\swriter.exe" goto OpenOffice3-Win32
echo ERROR: No supported version of OpenOffice/LibreOffice found!
echo Installation aborted.
goto end

:OpenOffice4-Win64
set _writer=%_OpenOffice4_w64%
set _user=%USERPROFILE%\%_OpenOffice4_Userprofile%
echo OpenOffice 4.x - Windows (64 bit)
goto settings_done

:OpenOffice4-Win32
set _writer=%_OpenOffice4_w32%
set _user=%USERPROFILE%\%_OpenOffice4_Userprofile%
echo OpenOffice 4.x - Windows (32 bit)
goto settings_done

:OpenOffice3-Win64
set _writer=%_OpenOffice3_w64%
set _user=%USERPROFILE%\%_OpenOffice3_Userprofile%
echo OpenOffice 3.x - Windows (64 bit)
goto settings_done

:OpenOffice3-Win32
set _writer=%_OpenOffice3_w32%
set _user=%USERPROFILE%\%_OpenOffice3_Userprofile%
echo OpenOffice 3.x - Windows (32 bit)
goto settings_done

:settings_done

echo Copying program components to %_user%\Scripts\python ...

if not exist "%_user%\Scripts" mkdir "%_user%\Scripts"
if not exist "%_user%\Scripts\python" mkdir "%_user%\Scripts\python"
copy /y program\*.py "%_user%\Scripts\python"

echo Installing LibreOffice extension ...

"%_writer%\program\unopkg" add -f program\WriteYw7-%_release%.oxt

echo Installing Explorer context menu entry (You may be asked for approval) ...

if not exist c:\pywriter mkdir c:\pywriter 

echo start %_user%\Scripts\python\openyw7.pyw %%1 %%2 > c:\pywriter\openyw7.bat
echo %_user%\Scripts\python\saveyw7.pyw %%1 > %_user%\Scripts\python\saveyw7.bat

add_cm.reg

popd

echo -----------------------------------------------------------------
echo #
echo # Installation of PyWriter software package v%_release% finished.
echo #
echo # Operation: 
echo # Right click your yWriter7 Project file
echo # and select "Proof read with LibreOffice".
echo #
echo -----------------------------------------------------------------

:end
pause