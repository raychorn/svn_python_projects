#!/bin/bash

prepdesignate="prepdesignate.sh"
cat << 'SCRIPTEOF' > "./$prepdesignate"
	#!/bin/bash

	if [ -d "/home/vagrant/designate" ]; then 
		echo "/home/vagrant/designate exists"
		cd /home/vagrant/designate
	else
    	echo "/home/vagrant/designate does not exist so Aborting."
    	exit 1
	fi
	
	p=$(whereis python)
	echo "DEBUG.1: $p"
	p=$(which python)
	echo "DEBUG.2: $p"
	p=$(which python | awk '{print $1}' | tail -n 1)
	echo "DEBUG.3: $p"
	if [ -f "$p" ]; then 

		ret=`python -c 'import sys; print("%i" % (sys.hexversion<0x03000000))'`
		if [ $ret -eq 0 ]; then
			echo "we require python version <3"
			exit 1
		else 
			echo "python version is <3"
		fi
	
	else
    	echo "Cannot find a suitable python. Aborting."
		exit 1
	fi
	
    sudo apt-get -y build-dep python-lxml
    sudo pip install -r requirements.txt -r test-requirements.txt
    sudo python setup.py develop	

	cd etc/designate #(/home/vagrant/designate/etc/designate)
	p=$(pwd)
	if [ "${p}" = "/home/vagrant/designate/etc/designate" ]; then
    	echo "has /home/vagrant/designate/etc/designate"
    	ls *.sample | while read f; do cp $f $(echo $f | sed "s/.sample$//g"); done
    else
    	echo "NOT has /home/vagrant/designate/etc/designate so Aborting."
    	exit 1
	fi

	#echo "(Replace contents of designate.conf with contents of file /home/vagrant/designate.conf.wkshp )"
	if [ -f "/home/vagrant/designate.conf.wkshp" ]; then 
		echo "/home/vagrant/designate.conf.wkshp exists"
    	cp /home/vagrant/designate.conf.wkshp ./designate.conf 
	else
    	echo "/home/vagrant/designate.conf.wkshp does not exist so Aborting."
    	exit 1
	fi
    
	if [ -d "/var/lib/designate" ]; then 
		echo "/var/lib/designate exists"
	else
    	echo "/var/lib/designate does not exist so making it"
    	sudo mkdir /var/lib/designate
	fi

	if [ -d "/home/vagrant/designate/log" ]; then 
		echo "/home/vagrant/designate/log exists"
	else
    	echo "/home/vagrant/designate/log does not exist so making it"
    	sudo mkdir /home/vagrant/designate/log
	fi
    
    resp=$(cat /etc/powerdns/pdns.d/pdns.local.gmysql | grep "gmysql-dbname=pdns" | awk '{print $1}' | tail -n 1)
    
    echo $resp
    
	if [ "${resp}" = "gmysql-dbname=pdns" ]; then
    	echo "has gmysql-dbname=pdns"
    else
    	echo "NOT has gmysql-dbname=pdns"
	fi
	
    resp=$(sudo netstat -tnlp | grep "pdns_server-in" | awk '{print $7}' | tail -n 1)
	OIFS=$IFS
	IFS='/'
	array=($resp)
	IFS=$OIFS
	echo ${array[1]}
	echo "${resp}"
	if [ "${array[1]}" = "pdns_server-in" ]; then
    	echo "has pdns_server-in"
    else
    	echo "NOT has pdns_server-in"
	fi
	
	dig @localhost openstack.com
	
    resp=$(sudo ls -latr /var/lib/mysql | grep "designate" | awk '{print $9}' | tail -n 1)
	echo "${resp}"
	if [ "$resp" = "designate" ]; then
		echo "designate mysql exists"
	else
    	echo "designate mysql does not exist so making it"
		mysql -e 'CREATE DATABASE `designate` CHARACTER SET utf8 COLLATE utf8_general_ci;'
	fi

	sudo designate-manage database init
	sudo designate-manage database sync
	
    resp=$(ps aux | grep "designate-api" | awk '{print $12}' | tail -n 1)
	echo "${resp}"
	if [ "$resp" = "/usr/local/bin/designate-api" ]; then
    	echo "has designate-api"
    else
    	echo "NOT has designate-api so starting it."
		sudo designate-api &
	fi

    resp=$(ps aux | grep "designate-central" | awk '{print $12}' | tail -n 1)
	echo "${resp}"
	if [ "$resp" = "/usr/local/bin/designate-central" ]; then
    	echo "has designate-central"
    else
    	echo "NOT has designate-central so starting it."
		sudo designate-central &
	fi
	
	echo "DONE!"
	exit 1
SCRIPTEOF

pk="$HOME/id_rsa_vagrant_designate_workshop"
if [ -f "$pk" ]; then 
	echo "$pk exists"
else
	echo "$pk does not exist so Aborting."
    exit 1
fi

host="vagrant@10.211.55.15"

scp -P 22 -o StrictHostKeyChecking=no -i "$pk" "./$prepdesignate" $host:~/$prepdesignate

if [ -f "./$prepdesignate" ]; then 
	echo "./$prepdesignate exists locally, so cleaning up because it was created dybamically."
	rm ./$prepdesignate
fi

ssh -o UserKnownHostsFile=/dev/null -i "$pk" -o StrictHostKeyChecking=no $host -p 22 << DESIGNATE_EOF

	pwd
	ls -latr

	if [ -f "/home/vagrant/prepdesignate.sh" ]; then 
		echo "/home/vagrant/prepdesignate.sh exists"
    	chmod +x /home/vagrant/prepdesignate.sh 
	else
    	echo "/home/vagrant/prepdesignate.sh does not exist so Aborting."
    	exit 1
	fi
	
	./$prepdesignate
DESIGNATE_EOF
