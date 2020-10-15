@echo on

set PYTHONPATH=c:\python25;Z:\python projects\@lib;Z:\python projects\_pyax-0.9.7.2-py2.5;Z:\python projects\@SQLAlchemy-0_5_3\lib;

sqlautocode mysql://root:peekab00@SQL2005:3307/vyperlogix2 -t content_* -o sql2005_tables.py

"C:\Program Files\@utils\sqlautocode\sqlautocode_cleanup.exe" --input=sql2005_tables.py
