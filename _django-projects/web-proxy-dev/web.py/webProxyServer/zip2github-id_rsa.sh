#!/bin/bash

clear

# Detect git, unzip - are they installed and functional ?

if [ $(which git) ]; then
    echo 'GIT Installed'
else
    echo 'GIT NOT Installed'
    echo 'Try: apt-get install git -V'
    echo 'Cannot continue...'
    exit
fi

if [ $(which unzip) ]; then
    echo 'UNZIP Installed'
else
    echo 'UNZIP NOT Installed'
    echo 'Try: apt-get install unzip -V'
    echo 'Cannot continue...'
    exit
fi

name=$(whoami)

if [ $name != "root" ]; then
    echo "Hey, this script only runs as the root user otherwise this script may not work as-designed."
    exit
fi

UNAME=""
EMAIL=""
DIRNAME=""
FNAME1=""
FNAME2=""
GITSPEC=""

# -u=username -e=email -d=directory -f1=filename1 -f2=filename2 -g=git@github.com:raychorn/MyRailsApp.git
for i in "$@"
do
case $i in
    -u=*|--username=*)
    UNAME=`echo $i | sed 's/[-a-zA-Z0-9]*=//'`
    ;;
    -d=*|--directory=*)
    DIRNAME=`echo $i | sed 's/[-a-zA-Z0-9]*=//'`
    ;;
    -e=*|--email=*)
    EMAIL=`echo $i | sed 's/[-a-zA-Z0-9]*=//'`
    ;;
    -f1=*|--file1=*)
    FNAME1=`echo $i | sed 's/[-a-zA-Z0-9]*=//'`
    ;;
    -f2=*|--file2=*)
    FNAME2=`echo $i | sed 's/[-a-zA-Z0-9]*=//'`
    ;;
    -g=*|--git=*)
    GITSPEC=`echo $i | sed 's/[-a-zA-Z0-9]*=//'`
    ;;
    --default)
    DEFAULT=YES
    ;;
    *)
            # unknown option
    ;;
esac
done
echo UNAME = ${UNAME}
echo EMAIL = ${EMAIL}
echo DIRNAME = ${DIRNAME}
echo FNAME1 = ${FNAME1}
echo FNAME2 = ${FNAME2}

if [ X"$UNAME" == X"" ]
then
    echo "Missing Username (-u=) from command line."
    echo 'Cannot continue...'
    exit
fi

if [ X"$GITSPEC" == X"" ]
then
    echo "Missing Git spec (-g=) from command line."
    echo "Try: git@github.com:raychorn/MyRailsApp.git or something similar"
    echo 'Cannot continue...'
    exit
fi

if [ -d "$DIRNAME" ]; then 
    echo
else
    echo "Cannot access directory ($DIRNAME)."
    echo 'Cannot continue...'
    exit
fi

group="gituser"

if grep -q $group /etc/group
then
   echo "group $group exits."
else
   groupadd $group
fi

if id -u $UNAME >/dev/null 2>&1; then
    userdel $UNAME
    if [ -d "/home/$UNAME" ]
    then
        rm -f -r /home/$UNAME
    fi
fi

useradd -s /bin/bash -m -d /home/$UNAME -c "$UNAME" -g $group $UNAME

echo -e "peekaboo\npeekaboo" | (passwd $UNAME)

FPATH1="$FNAME1"
FPATH2="$FNAME2"
FEXT1=""${FPATH1##*.}""
FEXT2=""${FPATH2##*.}""
BNAME1=${FNAME1/.$FEXT1/}
BNAME1=${BNAME1/$DIRNAME\//}
BNAME2=${FNAME2/.$FEXT2/}
BNAME2=${BNAME2/$DIRNAME\//}

if [ "$FEXT1" = "$FPATH1" ]; then
    FEXT1=""
fi

if [ "$FEXT2" = "$FPATH2" ]; then
    FEXT2=""
fi

echo FPATH1 = ${FPATH1}
echo FPATH2 = ${FPATH2}

echo FEXT1 = ${FEXT1}
echo FEXT2 = ${FEXT2}

echo BNAME1 = ${BNAME1}
echo BNAME2 = ${BNAME2}

if [ "$FEXT1" = "zip" ]; then
    echo
else  
    if [ "$FEXT2" = "zip" ]; then
        echo
    else  
        echo "Cannot process files other than zip files ($FEXT1)."
        echo "Cannot process files other than zip files ($FEXT2)."
        echo 'Cannot continue...'
        exit
    fi
fi

if [ "$FEXT2" = "zip" ]; then
    # swap file1 and file2 because they are out of sequence...
    echo "Swap $FPATH1 for $FPATH2"

    T="$FPATH1"
    FPATH1="$FPATH2"
    FPATH2="$T"

    T="$FEXT1"
    FEXT1="$FEXT2"
    FEXT2="$T"

    T="$BNAME1"
    BNAME1="$BNAME2"
    BNAME2="$T"
fi

if [ -f "$FPATH1" ]
then
    echo
else  
    if [ -f "$FPATH2" ]
    then
        echo
    else  
        echo "Cannot access file ($FPATH1)."
        echo "Cannot access file ($FPATH2)."
        echo 'Cannot continue...'
        exit
    fi
fi

touch /home/$UNAME/gitter.sh
cat << 'EOF' > /home/$UNAME/gitter.sh
#!/bin/bash

UNAME=$(cat UNAME.txt)
BNAME1=$(cat BNAME1.txt)
BNAME2=$(cat BNAME2.txt)
FNAME1=$(cat FNAME1.txt)
FNAME2=$(cat FNAME2.txt)
FEXT1=$(cat FEXT1.txt)
FEXT2=$(cat FEXT2.txt)
EMAIL=$(cat EMAIL.txt)
FPATH1="/home/$UNAME/$BNAME1.$FEXT1"
FPATH2="/home/$UNAME/.ssh/$BNAME2"
GITSPEC=$(cat GITSPEC.txt)
echo "UNAME=$UNAME"
echo "BNAME1=$BNAME1"
echo "BNAME2=$BNAME2"
echo "FNAME1=$FNAME1"
echo "FNAME2=$FNAME2"
echo "FEXT1=$FEXT1"
echo "FEXT2=$FEXT2"
echo "EMAIL=$EMAIL"
echo "FPATH1=$FPATH1"
echo "FPATH2=$FPATH2"
echo "GITSPEC=$GITSPEC"

cd ~

pwd=$(pwd)

if [ "$pwd" = "/home/$UNAME" ]; then
    echo
else  
    echo "Failed to change cwd to (/home/$UNAME)."
    echo 'Cannot continue...'
    exit
fi

if [ -d "$BNAME1" ]; then 
    rm -rf "$BNAME1"
fi

if [ -d "$BNAME2" ]; then 
    rm -rf "$BNAME2"
fi

if [ -f "$FPATH1" ]; then 
    if [ "$FEXT1" = "zip" ]; then
        unzip "$FPATH1"

        if [ -d "$BNAME1" ]; then 
            cd "$BNAME1"

            pwd=$(pwd)
            if [ "$pwd" = "/home/$UNAME/$BNAME1" ]; then
                echo
            else  
                echo "Failed to change cwd to (/home/$UNAME/$BNAME1)."
                echo 'Cannot continue...'
                exit
            fi

            echo "(1/7)"
            response=$(git config --global user.name "$UNAME")
            echo $response

            echo "(2/7)"
            response=$(git config --global user.email $EMAIL)
            echo $response

            echo "(3/7)"
            response=$(git init)
            echo $response

            if `echo ${response} | grep "Initialized empty Git repository in" 1>/dev/null 2>&1`
            then
                echo "(4/7)"
                response=$(git add *)
                echo $response
            else
                echo "Failed to Initialize empty git repo."
                echo 'Cannot continue...'
                exit
            fi

            echo "(5/7)"
            git commit -m "Imported from $FPATH1"

            echo "(6/7)"
            git remote add origin "$GITSPEC"

            echo "(7/7)"
            git push -u origin master
        fi
        else
        echo "Missing $FEXT1 or it's not .ZIP."
    fi
else
    echo "Missing $FPATH1."
fi

echo 'Gitter Done !!!'
EOF

cp "$FPATH1" "/home/$UNAME"

if [ -d "/home/$UNAME/.ssh" ]; then 
    echo
else
    mkdir "/home/$UNAME/.ssh"
fi

cp "$FPATH2" "/home/$UNAME/.ssh"
cp "$FPATH2.pub" "/home/$UNAME/.ssh"

if [ -f "/home/$UNAME/.ssh/$BNAME2" ]; then 
    echo
else
    echo "Cannot continue without the $BNAME2 file in-place."
    exit
fi

if [ -f "/home/$UNAME/.ssh/$BNAME2.pub" ]; then 
    echo
else
    echo "Cannot continue without the $BNAME2.pub file in-place."
    exit
fi

chmod 400 "/home/$UNAME/.ssh/$BNAME2"
chmod 400 "/home/$UNAME/.ssh/$BNAME2.pub"

gitter="/home/$UNAME/gitter.sh"

chown $UNAME:$group $gitter
chmod +x $gitter

chown $UNAME:$group "/home/$UNAME/$BNAME1.$FEXT1"
chown $UNAME:$group "/home/$UNAME/.ssh"
chown $UNAME:$group "/home/$UNAME/.ssh/$BNAME2"
chown $UNAME:$group "/home/$UNAME/.ssh/$BNAME2.pub"

printf "%s" "$UNAME" >> /home/$UNAME/UNAME.txt
printf "%s" "$BNAME1" >> /home/$UNAME/BNAME1.txt
printf "%s" "$BNAME2" >> /home/$UNAME/BNAME2.txt
printf "%s" "$FNAME1" >> /home/$UNAME/FNAME1.txt
printf "%s" "$FNAME2" >> /home/$UNAME/FNAME2.txt
printf "%s" "$FEXT2" >> /home/$UNAME/FEXT2.txt
printf "%s" "$FEXT1" >> /home/$UNAME/FEXT1.txt
printf "%s" "$EMAIL" >> /home/$UNAME/EMAIL.txt
printf "./%s" "$FPATH1" >> /home/$UNAME/FPATH1.txt
printf "./%s" "$FPATH2" >> /home/$UNAME/FPATH2.txt
printf "%s" "$GITSPEC" >> /home/$UNAME/GITSPEC.txt

echo $gitter
sudo su - $UNAME -c './gitter.sh 1>./output.txt 2>&1'

while read p; do
    echo $p
done < /home/$UNAME/output.txt

echo 'Done !'
