@echo off

REM "C:\Program Files (x86)\SWFTools\pdf2swf.exe" "E:\PROPHECYFOUNDATIONS\data\Study Guides\Is_there_anything_left_you_can_trust.pdf" -o "E:\PROPHECYFOUNDATIONS\data\Study Guides\Is_there_anything_left_you_can_trust.swf" -f -T 9 -t -G -s storeallcharacters

"C:\Program Files (x86)\SWFTools\pdf2swf.exe" "%1" -o "%2" -f -T 9 -t -G -s storeallcharacters
