if exist air.pkg del air.pkg
if exist server.pkg del server.pkg
if exist tk.pkg del tk.pkg
if exist buildinstaller del buildinstaller\*.* < y.txt
if exist buildinstaller rmdir buildinstaller
if exist buildserver del buildserver\*.* < y.txt
if exist buildserver rmdir buildserver
if exist distserver del distserver\*.* < y.txt
if exist distserver rmdir distserver
if exist server.exe del server.exe
if exist installer.exe del installer.exe
