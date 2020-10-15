@echo off

set PYTHONPATH=c:\python25;Z:\python projects\@lib;

 python -m cProfile -s cumulative oodb-tests.py > report-oodb-tests.txt
 rename db_PFH2.dbx db_PFH2.001
 python -m cProfile -s cumulative oodb-tests2.py > report-oodb-tests2.txt
 rename db_PFH2.dbx db_PFH2.002
 python -m cProfile -s cumulative oodb-tests3.py > report-oodb-tests3.txt
 rename db_PFH2.dbx db_PFH2.003

goto exit

python -m cProfile -s cumulative shove-tests1.py > report-shove-tests1.txt
python -m cProfile -s cumulative shove-tests2.py > report-shove-tests2.txt
python -m cProfile -s cumulative shove-tests3.py > report-shove-tests3.txt
python -m cProfile -s cumulative shove-tests4.py > report-shove-tests4.txt
python -m cProfile -s cumulative shove-tests5.py > report-shove-tests5.txt
python -m cProfile -s cumulative shove-tests6.py > report-shove-tests6.txt
python -m cProfile -s cumulative shove-tests7.py > report-shove-tests7.txt

:exit
