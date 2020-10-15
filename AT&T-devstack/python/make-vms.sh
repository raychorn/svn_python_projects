#!/bin/bash

cd ~/devstack
source openrc admin

vmname="vm1"

image=""
IMAGES=$(nova image-list | grep -o "[0-9a-fA-F]\{8\}-[0-9a-fA-F]\{4\}-[0-9a-fA-F]\{4\}-[0-9a-fA-F]\{4\}-[0-9a-fA-F]\{12\}")
for uuid in $IMAGES
do
	image=$uuid
	break
done

if [ "$image." = "." ]; then
	echo "missing image so aborting..."
	exit 1
fi

cnt=1
delta=18
start=25
flavor=""
FLAVORS=$(nova flavor-list)
for f in $FLAVORS
do
	if [ "$cnt" -eq $start ]; then
		start=$((start+$delta))
		flavor=$f
		break
	fi
    cnt=$((cnt+1))
done

if [ "$flavor." = "." ]; then
	echo "missing flavor so aborting..."
	exit 1
fi

cnt=1
delta=6
start=9
keyname=""
KEYPAIRS=$(nova keypair-list)
for k in $KEYPAIRS
do
	if [ "$cnt" -eq $start ]; then
		start=$((start+$delta))
		keyname=$k
		break
	fi
    cnt=$((cnt+1))
done

if [ "$keyname." = "." ]; then
	echo "missing keyname so aborting..."
	exit 1
fi

cnt=1
start=9
end=15
zonename=""
ZONES=$(nova availability-zone-list)
for z in $ZONES
do
	if [ "$cnt" -eq $start ]; then
		zonename=$z
	fi
	if [ "$cnt" -eq $end ]; then
		zonename="$zonename:$z"
		break
	fi
    cnt=$((cnt+1))
done

if [ "$zonename." = "." ]; then
	echo "missing zonename so aborting..."
	exit 1
fi

nova boot $vmname --flavor $flavor --image $image --security-groups default --key_name $keyname --availability-zone $zonename
