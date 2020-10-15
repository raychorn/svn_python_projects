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
FNAME=""
GITSPEC=""

# -u=username -e=email -d=directory -f=filename -g=git@github.com:raychorn/MyRailsApp.git
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
    -f=*|--file=*)
    FNAME=`echo $i | sed 's/[-a-zA-Z0-9]*=//'`
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
echo FNAME = ${FNAME}

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

FPATH="$DIRNAME/$FNAME"
FEXT=""${FPATH##*.}""
BNAME=${FNAME/.$FEXT/}

echo BNAME = ${BNAME}

if [ "$FEXT" = "zip" ]; then
    echo
else  
    echo "Cannot process files other than zip files ($FEXT)."
    echo 'Cannot continue...'
    exit
fi

if [ -f "$FPATH" ]
then
    echo
else  
    echo "Cannot access file ($FPATH)."
    echo 'Cannot continue...'
    exit
fi

# sudo su-c'./scriptname.sh'
touch /home/$UNAME/gitter.sh
cat << 'EOF' > /home/$UNAME/gitter.sh
#!/bin/bash

EOF


cd /home/$UNAME

pwd=$(pwd)

if [ "$pwd" = "/home/$UNAME" ]; then
    echo
else  
    echo "Failed to change cwd to (/home/$UNAME)."
    echo 'Cannot continue...'
    exit
fi

cp "$FPATH" "/home/$UNAME"

if [ -d "$BNAME" ]; then 
    rm -rf "$BNAME"
fi

if [ -f "$FNAME" ]; then 
    unzip "$FNAME"

    if [ -d "$BNAME" ]; then 
        cd "$BNAME"

        pwd=$(pwd)
        if [ "$pwd" = "/home/$UNAME/$BNAME" ]; then
            echo
        else  
            echo "Failed to change cwd to (/home/$UNAME/$BNAME)."
            echo 'Cannot continue...'
            exit
        fi

        echo "(1)"
        response=$(git config --global user.name "$UNAME")
        echo $response

        echo "(2)"
        response=$(git config --global user.email $EMAIL)
        echo $response

        echo "(3)"
        response=$(git init)
        echo $response

        if `echo ${response} | grep "Initialized empty Git repository in" 1>/dev/null 2>&1`
        then
            echo "(3)"
            response=$(git add *)
            echo $response
        else
            echo "Failed to Initialize empty git repo."
            echo 'Cannot continue...'
            exit
        fi

        #git commit -m "Imported from $FPATH"
        #git remote add origin "$GITSPEC"
        #git push -u origin master
    fi
fi

echo 'Done !'
