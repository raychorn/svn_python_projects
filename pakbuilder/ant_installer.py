import re
import os, sys

from vyperlogix import misc

from vyperlogix.lists.ListWrapper import ListWrapper

__is_response_iterable__ = lambda resp:misc.isIterable(resp) and (len(resp) > 0)
__is_response_iterable_empty__ = lambda resp:misc.isIterable(resp) and (len(resp) == 0)

__installer_bash_script__ = '''
#!/bin/bash

OS_VERSION_FILE=/proc/version
OS=`uname`
if [ "${OS}" = "Linux" ]; then
	if [ -r ${OS_VERSION_FILE} ]; then
		grep -i centos ${OS_VERSION_FILE} 1>/dev/null 2>&1
		if [ $? -eq 0 ]; then
			LINUX_VERSION=centos
		else
			grep -i ubuntu ${OS_VERSION_FILE} 1>/dev/null 2>&1
			if [ $? -eq 0 ]; then
				LINUX_VERSION=ubuntu
			else
				fail 2 "${SCRIPT} only supports CentOS and Ubuntu at this time."
			fi
		fi
	else
		fail 3 "Unable to find ${OS_VERSION_FILE}."
	fi
else
	fail 4 "${SCRIPT} only supports Linux at this time."
fi

r=$(lsb_release -d)
IFS=': ' read -a array <<< "$r"
distro=""
count=0
for item in $r
	do
	if [ $count -gt 0 ]; then
		distro="$distro $item"
		echo "item --> $item"
	fi
	count=1
done

if [ "${LINUX_VERSION}" = "centos" ]; then
	echo "OS is $distro"
	yum -y install java-1.6.0-openjdk-devel

	cd /opt
	wget http://www.us.apache.org/dist/ant/binaries/apache-ant-1.9.3-bin.tar.gz
	tar xvfvz apache-ant-1.9.3-bin.tar.gz -C /opt
	ln -s /opt/apache-ant-1.9.3 /opt/ant
	ln -s /opt/ant/bin/ant /usr/bin/ant
elif [ "${LINUX_VERSION}" = "ubuntu" ]; then
	echo "OS is $distro"
	apt-get -q -y install openjdk-6-jdk
	apt-get -q -y install openjdk-6-jre-headless
	apt-get -q -y install openjdk-6-jre-lib
	apt-get -q -y install ant
	apt-get -q -y install ant-doc
	apt-get -q -y install ant-optional	
fi

JAVA_HOME=$(readlink -f /usr/bin/javac | sed "s:bin/javac::")
echo "JAVA_HOME=$JAVA_HOME"

ANT_HOME=$(readlink -f /usr/bin/ant | sed "s:bin/ant::")
echo "ANT_HOME=$ANT_HOME"

file="./.bash_profile"

sed "/^JAVA_HOME=/d" -i $file
sed "/^export JAVA_HOME/d" -i $file

echo "JAVA_HOME=1234" >> $file
echo "export JAVA_HOME" >> $file
'''

def install_ant(__sftp__,logger,callback=None):
    def scan_for_blank_lines(item,pattern):
        return item == pattern

    sname = '%s%sinstall-ant.sh' % (os.path.expanduser('~'),os.sep)
    fOut = open(sname,'w')
    lst = ListWrapper(__installer_bash_script__.split('\n'))
    items = lst.findAllMatching('', callback=scan_for_blank_lines, returnIndexes=True)
    if (len(items) > 1) and (items[0] < 1):
        del lst[items[0]:items[1]-1]
    for l in lst:
        print >>fOut, l.rstrip()
    fOut.flush()
    fOut.close()

    sftp = __sftp__()
    cmd = 'echo ${HOME}'
    responses = sftp.exec_command(cmd)
    logger.info(cmd)
    logger.info('\n'.join(responses))
    lines = [l for l in responses if (len(l.strip()) > 0) if (len(l.strip().split('/')) > 1)]
    if (len(lines) == 0):
        logger.warning('Cannot proceed without a valid Home directory for the user who is being used as the user context for this program. This should never happen unless your Linux box is broken.')
    else:
        __linux_home__ = lines[0]

        sname_dest = '%s/%s' % (__linux_home__,os.path.basename(sname))
        logger.info('(+++) scp put.1 "%s" --> "%s".' % (sname, sname_dest))

        sftp = __sftp__()
        cmd = 'rm %s' % (sname_dest)
        responses = sftp.exec_command(cmd)
        logger.info(cmd)
        logger.info('\n'.join(responses))

        sftp = __sftp__()
        sftp.put(sname, sname_dest,callback=callback)

        unix_command = 'dos2unix'
        __re__ = re.compile(r".*no\s*%s\s*in.*" % (unix_command), re.DOTALL | re.MULTILINE)

        sftp = __sftp__()
        cmd = '%s %s' % (unix_command,sname_dest)
        responses = sftp.exec_command(cmd)
        logger.info(cmd)
        logger.info('\n'.join(responses))
        errors = [l for l in responses if (__re__.match(l))]
        if (len(errors) > 0):
            logger.warning('Camnnot continue unless "%s" exists.' % (unix_command))

        sftp = __sftp__()
        cmd = 'ls -la %s' % (sname_dest)
        responses = sftp.exec_command(cmd)
        logger.info(cmd)
        logger.info('\n'.join(responses))
        lines = [l for l in responses if (l.find('cannot access') > -1) or (l.lower().find('no such file or directory') > -1)]
        if (len(lines) > 0):
            logger.warning('Camnnot continue unless "%s" exists and it should under programmatic control however this is not the case.' % (sname_dest))
            __terminate__()

        sftp = __sftp__()
        cmd = 'ls -la %s' % (sname_dest)
        responses = sftp.exec_command(cmd)
        logger.info(cmd)
        logger.info('\n'.join(responses))
        lines = [l for l in responses if (l.find('cannot access') > -1) or (l.lower().find('no such file or directory') > -1)]
        if (len(lines) > 0):
            logger.warning('Camnnot continue unless "%s" exists and it should under programmatic control however this is not the case.' % (sname_dest))
            __terminate__()

        sftp = __sftp__()
        cmd = 'chmod +x %s' % (sname_dest)
        responses = sftp.exec_command(cmd)
        lines = []
        logger.debug('1. __is_response_iterable__(responses)=%s' % (__is_response_iterable__(responses)))
        if (__is_response_iterable__(responses)):
            logger.debug('2. type(responses[0])=%s' % (type(responses[0])))
            lines = responses[0].split('\n')
        elif (not __is_response_iterable_empty__(responses)):
            logger.debug('3. type(responses)=%s' % (type(responses)))
            lines = responses.split('\n')
        else:
            logger.debug('4. type(responses)=%s' % (type(responses)))
        logger.debug('5. __is_response_iterable__(responses)=%s' % (__is_response_iterable__(responses)))
        lines = [l.strip() for l in lines if (len(l.strip()) > 0)]
        logger.info(cmd)
        logger.info('\n'.join(responses))

        #sftp = __sftp__()
        #cmd = 'cat %s' % (sname_dest)
        #responses = sftp.exec_command(cmd)
        #logger.info(cmd)
        #logger.info('\n'.join(responses))
        #lines = [l for l in responses if (l.find('cannot access') > -1) or (l.lower().find('no such file or directory') > -1)]
        #if (len(lines) > 0):
            #logger.warning('Camnnot continue unless "%s" exists and it should under programmatic control however this is not the case.' % (sname_dest))
            #__terminate__()
            
        __re2__ = re.compile("(?P<name>(JAVA_HOME|ANT_HOME))=(?P<value>.*)", re.DOTALL | re.MULTILINE)

        sftp = __sftp__()
        cmd = '%s' % (sname_dest)
        responses = sftp.exec_command(cmd)
        __lines__ = [r.split('\n') for r in responses] if (__is_response_iterable__(responses)) else responses.split('\n')
        lines = []
        for l in __lines__:
            for ll in l:
                lines.append(ll.strip())
        lines = [l.strip() for l in lines if (len(l.strip()) > 0)]
        errors = [l.strip() for l in lines if (l.strip().find('Aborting') > -1)]
        variables = dict([(__re2__.match(l).groupdict()['name'],__re2__.match(l).groupdict()['value']) for l in lines if (__re2__.match(l))])
        logger.info(cmd)
        logger.info('\n'.join(responses))

        logger.debug('len(errors)=%s' % (len(errors)))
        if (len(variables) != 2) or ('JAVA_HOME' not in variables.keys()) or ('ANT_HOME' not in variables.keys()):
            logger.warning('1. Cannot proceed without JAVA_HOME and ANT_HOME; something has gone wrong with the ANT installer.')
            __terminate__()
            
        # ANT_HOME and JAVA_HOME need to be installed in the appropriate file(s) to allow the current user to use these environment variables.

        if (os.path.exists(sname)):
            logger.debug('os.remove("%s")' % (sname))
            os.remove(sname)

        sftp = __sftp__()
        cmd = 'rm %s' % (sname_dest)
        responses = sftp.exec_command(cmd)
        logger.info(cmd)
        logger.info('\n'.join(responses))

        logger.info('ANT has been successfully installed.')
        