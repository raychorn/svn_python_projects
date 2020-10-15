@echo on

set PYTHONPATH=Z:\Python;Z:\python projects\@lib;Z:\python projects\_pyax-0.9.7.2-py2.5;Z:\python projects\@SQLAlchemy-0_5_4p2\lib;

sqlautocode mysql://root:peekab00@127.0.0.1:3307/wordpress -t wp_* -o wp_tables.py
"C:\Program Files\@utils\sqlautocode\sqlautocode_cleanup.exe" --input="Z:\python projects\wordpress-in-django\wp_tables.py"

sqlautocode mysql://root:peekab00@127.0.0.1:3307/wpmu10 -t wpmu_* -o wpmu_tables.py
"C:\Program Files\@utils\sqlautocode\sqlautocode_cleanup.exe" --input="Z:\python projects\wordpress-in-django\wpmu_tables.py"
