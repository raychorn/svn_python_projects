if %1. == profile. goto profiler
if %1. == 2. goto phase2

main2.py --profile --psyco=bind --input=Bigtest.txt

goto end

:profiler
 python -m cProfile -s cumulative main2.py --psyco=bind --input=Bigtest.txt
goto end

:phase2
 main2.py --psyco=bind --input2=etl_unique_computers.csv
goto end

:end
