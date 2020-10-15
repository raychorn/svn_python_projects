@echo off
cls
echo BEGIN:

set PYTHONPATH=c:\python25\lib;Z:\python projects\@lib;

if 0%1. == 0. goto help

if %1. == 1. python  -m cProfile -s cumulative zipper.py zip > reports-zipper.txt
if %1. == 2. python  -m cProfile -s cumulative zipper.py unzip > reports-zipper.txt

if %1. == 3. python  -m cProfile -s cumulative zipper.py xzip > reports-zipper.txt
if %1. == 4. python  -m cProfile -s cumulative zipper.py unxzip > reports-zipper.txt

if %1. == 5. python  -m cProfile -s cumulative zipper.py bzip > reports-zipper.txt
if %1. == 6. python  -m cProfile -s cumulative zipper.py unbzip > reports-zipper.txt

goto end

:help
echo Begin: ---------------------------------------------------------------------------------------------------
echo "1" means ZIP using ezip
echo "2" means UNZIP using ezip
echo
echo "3" means ZIP using xzip
echo "4" means UNZIP using xzip
echo
echo "5" means ZIP using bzip
echo "6" means UNZIP using bzip
echo END! -----------------------------------------------------------------------------------------------------

:end

echo END!

