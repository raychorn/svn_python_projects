@echo on

sqlautocode mysql://root:peekab00@SQL2005:3306/iso_data -t country,states -o iso_tables.py
