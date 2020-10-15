target='/root/@svn/repo1-14049.bzip'
repo='/root/@svn'

function var.defined {
    eval '[[ ${!'$1'[@]} ]]'
}

if var.defined target; then
{
    if var.defined repo; then
    {
        export PYTHONPATH=${PYTHONPATH}:~/python/libs/2.5/vyperlogix.zip:/usr/share/pyshared
        python2.5 ~/svnHotBackups/svnHotBackups.py --restore=$target --repo-path=$repo > run_log.txt
	cat run_log.txt
    }
    else
     {
        echo "CANNOT perform the desired function...";
      }
     fi
}
else
 {
    echo "CANNOT perform the desired function...";
  }
 fi
