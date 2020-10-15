@echo off

set PYTHONPATH=.;%PYTHONPATH%;Z:\python projects\@lib;c:\python25;

pyro-ns -v -s NSSecEx

REM python -O -tt -c "import Pyro.naming,sys; import vyperlogix.misc._psyco; vyperlogix.misc._psyco.importPsycoIfPossible(func=Pyro.naming.main); Pyro.naming.main(sys.argv[1:])" -v -s NSSecEx

