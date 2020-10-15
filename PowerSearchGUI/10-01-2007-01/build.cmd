set SevenZipEXE=C:\Program Files\7-Zip\7z.exe
if exist "C:\Program Files\7-Zip\7z.exe" set SevenZipEXE=C:\Program Files\7-Zip\7z.exe

python -OO setup.py py2exe --includes lib

if exist dist\powerSearch.exe del dist\powerSearch.exe
rename dist\main.exe powerSearch.exe

if "%SevenZipEXE%". == "". goto nocompress

"%SevenZipEXE%" -aoa x "dist\library.zip" -o"dist\library\"
del "dist\library.zip"

cd dist\library
"%SevenZipEXE%" a -tzip -mx9 "..\library.zip" -r
cd ..\..
rd "dist\library" /s /q

goto done

:nocompress
echo NoCompress !

:done
echo Done !
