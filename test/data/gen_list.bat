rem Generate a list of function calls for each yw7 file

set _genfile=update_all.bat
del %_genfile%
for /F "tokens=*" %%l in ('dir *.yw7 /s /b') do echo update.py "%%l" >> %_genfile%
popd
