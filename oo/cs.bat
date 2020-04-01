REM cs.bat
REM Collects everything for a PyWriter Tools release
REM and puts it the "dist" setup directory to be zipped.
REM 
REM See: https://github.com/peter88213/PyWriter
REM License: The MIT License (https://opensource.org/licenses/mit-license.php)
REM Copyright: (c) 2020, Peter Triesberger

set _release=0.9.5

set _project=PyWriter

set _root=..\

rem --------------------------------------------------------
rem Set up directory structure
rem --------------------------------------------------------

set _target=%_root%oo\dist\PyWriter_OO_v%_release%

if exist %_target% rd /s /q %_target%

mkdir %_target%
mkdir %_target%\setup
mkdir %_target%\setup\program

rem --------------------------------------------------------
rem Generate release info
rem --------------------------------------------------------

rem echo v%_release%>%_target%\VERSION

rem --------------------------------------------------------
rem Copy release items 
rem --------------------------------------------------------

set _file=%_root%oo\README.md
set _dest=%_target%\
call :copyFile

set _file=%_root%oo\oxt\WriteYw7-%_release%.oxt
set _dest=%_target%\setup\program\
call :copyFile

set _file=%_root%build\openyw7.pyw
set _dest=%_target%\setup\program\
call :copyFile

set _file=%_root%build\saveyw7.pyw
set _dest=%_target%\setup\program\
call :copyFile

set _file=%_root%oo\reg\del_cm.reg
set _dest=%_target%\setup\
call :copyFile

set _file=%_root%oo\reg\add_cm.reg
set _dest=%_target%\setup\
call :copyFile

set _file=%_root%LICENSE
set _dest=%_target%\
call :copyFile

set _file=%_root%oo\Install.bat
set _dest=%_target%\
call :copyFile

set _file=%_root%oo\Uninstall.bat
set _dest=%_target%\
call :copyFile

exit /b


:copyFile

rem --------------------------------------------------------
rem Copy a file
rem --------------------------------------------------------

if not exist %_file% goto error
copy /y  %_file% %_dest%
exit /b


:error

rmdir /s /q %_target%
echo ERROR: %_file% does not exist!
pause
exit 1

:end