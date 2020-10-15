@echo on

set PYTHONPATH=c:\python25;Z:\python projects\@lib;Z:\python projects\_pyax-0.9.7.2-py2.5;Z:\python projects\@SQLAlchemy-0_5_3\lib;

sqlautocode mysql://root:peekab00@127.0.0.1:3306/vyperlogix2 -t content_* -o web20082_tables.py

"C:\Program Files\@utils\sqlautocode\sqlautocode_cleanup.exe" --input=web20082_tables.py
