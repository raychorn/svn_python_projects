@echo on

set PATH=%PATH%;C:\Python25\Scripts;

sqlautocode mysql://root:peekab00@localhost:3306/monitor -t ps* -o monitor_tables.py

Z:\_utils\sqlautocode_cleanup\sqlautocode_cleanup --input="Z:\python projects\monitor-ram-usage\monitor_tables.py"
