set SevenZipEXE=C:\Program Files\7-Zip\7z.exe
if exist "C:\Program Files\7-Zip\7z.exe" set SevenZipEXE=C:\Program Files\7-Zip\7z.exe

python -OO setup.py py2exe --includes lib

if not exist dist\setupProduct.exe copy C:\Python25\lib\site-packages\py2exe\run.exe dist\setupProduct.exe

if %1. == nocompress. goto nocompress

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
