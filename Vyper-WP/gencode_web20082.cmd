@echo on

set PYTHONPATH=c:\python25;Z:\python projects\@lib;Z:\python projects\_pyax-0.9.7.2-py2.5;Z:\python projects\@SQLAlchemy-0_5_3\lib;

REM sqlautocode mysql://root:peekab00@127.0.0.1:3306/wordpress -t * -o wordpress_tables.py
sqlautocode mysql://root:peekab00@127.0.0.1:3306/wordpress -o wordpress_tables.py

"C:\Program Files\@utils\sqlautocode\sqlautocode_cleanup.exe" --input=wordpress_tables.py
