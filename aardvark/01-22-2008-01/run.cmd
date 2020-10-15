if %1. == 1. goto method1			REM does Method1 using Psyco...
if %1. == 1nop. goto method1nop		REM does Method1 not using Psyco and not using Profiler...
if %1. == 1v. goto method1v			REM does Method1 using Psyco on old file...
if %1. == 1np. goto method1np			REM does Method1 using external Profiler...
if %1. == 1p. goto method1p			REM does Method1 using no Psyco...
if %1. == 2. goto method2			REM does Method2 using old file...
if %1. == o. goto output			REM does Shelve Method on SQL Server ResultSet...
if %1. == r. goto reader			REM reads shelved data...
if %1. == timeRe. goto timeRe			REM time the re versus split for timeDurations...
if %1. == 1pFull. goto method1psycoFull	REM does Method1 using Psyco=full...
if %1. == 1plog. goto method1psycoLog		REM does Method1 using Psyco=log...
if %1. == 1pbind. goto method1psycoBind	REM does Method1 using Psyco=bind...
if %1. == 1npfull. goto method1npFull		REM does Method1 using external Profiler and Psyco=full...
if %1. == 1nplog. goto method1npLog		REM does Method1 using external Profiler and Psyco=log...
if %1. == 1npbind. goto method1npBind		REM does Method1 using external Profiler and Psyco=bind...
if %1. == 1pbindPipe2. goto method1pBindPipe2		REM does Pipeline Process 2 using internal Profiler and Psyco=bind...
goto end

:method1
 main.py --profile --psyco %2 %3 %4 %5 %6 %7 %8 %9 --input=Bigtest.txt
goto end

:method1nop
 main.py %2 %3 %4 %5 %6 %7 %8 %9 --input=Bigtest.txt
goto end

:method1v
 main.py --profile --psyco --verbose %2 %3 %4 %5 %6 %7 %8 %9 --input=Z:\project-aardvark\bigtest.txt
goto end

:method1np
python -m cProfile -s cumulative main.py --psyco=bind %2 %3 %4 %5 %6 %7 %8 %9 --input=Bigtest.txt
goto end

:method1npFull
python -m cProfile -s cumulative main.py --psyco=full %2 %3 %4 %5 %6 %7 %8 %9 --input=Bigtest.txt
goto end

:method1npLog
python -m cProfile -s cumulative main.py --psyco=log %2 %3 %4 %5 %6 %7 %8 %9 --input=Bigtest.txt
goto end

:method1npBind
python -m cProfile -s cumulative main.py --psyco=bind %2 %3 %4 %5 %6 %7 %8 %9 --input=Bigtest.txt
goto end

:method1p
python -m cProfile -s cumulative main.py %2 %3 %4 %5 %6 %7 %8 %9 --input=Bigtest.txt
goto end

:method2
 main.py --profile --psyco %2 %3 %4 %5 %6 %7 %8 %9 --input2=Z:\project-aardvark\bigtest.txt
goto end

:output
 main.py --profile --psyco %2 %3 %4 %5 %6 %7 %8 %9 --output=Bigtest
goto end

:reader
 main.py --psyco %2 %3 %4 %5 %6 %7 %8 %9 --read=Bigtest
goto end

:timeRe
 main.py --psyco %2 %3 %4 %5 %6 %7 %8 %9 --timeRe
goto end

:method1psycoFull
 main.py --profile --psyco=full %2 %3 %4 %5 %6 %7 %8 %9 --input=Bigtest.txt
goto end

:method1psycoLog
 main.py --profile --psyco=log %2 %3 %4 %5 %6 %7 %8 %9 --input=Bigtest.txt
goto end

:method1psycoBind
 main.py --profile --psyco=bind %2 %3 %4 %5 %6 %7 %8 %9 --input=Bigtest.txt
goto end

:method1pBindPipe2
 main.py --profile --psyco=bind %2 %3 %4 %5 %6 %7 %8 %9 --process=2
goto end

:end

