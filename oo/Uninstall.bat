@echo off
REM Removes the PyWriter Tools software package.
REM 
REM See: https://github.com/peter88213/PyWriter
REM License: The MIT License (https://opensource.org/licenses/mit-license.php)
REM Copyright: (c) 2020, Peter Triesberger
REM 
REM Note: This script is to be executed manually.
REM 
REM Preconditions:
REM * PyWriter Tools are installed.
REM * OpenOffice 3.x or 4.x is installed.
REM
REM Postconditions:
REM * Previously auto-installed items of PyWriter Tools are removed.
REM * The Explorer context menu entry "PyWriter Tools" is removed.

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

echo Deleting program components in %_user%\Scripts\python ...

del /q "%_user%\Scripts\python\saveyw7.pyw"
del /q "%_user%\Scripts\python\saveyw7.bat"
del /q "%_user%\Scripts\python\openyw7.pyw"
del /q c:\pywriter\openyw7.bat

echo Removing LibreOffice extension ...

"%_writer%\program\unopkg" remove -f WriteYw7-%_release%.oxt

echo Removing Explorer context menu entry (You may be asked for approval) ...

del_cm.reg

popd

echo -----------------------------------------------------------------
echo #
echo # PyWriter v%_release% is removed from your PC.
echo #
echo -----------------------------------------------------------------
pause



:end
