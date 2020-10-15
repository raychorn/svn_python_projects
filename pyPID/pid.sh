export PYTHONPATH=$HOME/lib/python2.5:$HOME/lib/python2.5/site-packages:/root/lib/python2.5/site-packages/vyperlogix_2_5_5.zip:/usr/share/pyshared

rm -f /var/run/sleepy_mongoose.pid

python2.5 ~/bin/pid.py --pname=sleepy_mongoose -verbose
