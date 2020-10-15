from wrapper_conf_handler import parse_and_resequence_wrapper_conf, parse_and_resequence

if (__name__ == '__main__'):
    responses = '''
#include %ALIVE_BASE%/user/conf/collector/wrapper-license.conf
#include %ALIVE_BASE%/user/conf/email.properties

# Java Application
wrapper.java.command=%ALIVE_BASE%/jre/bin/java

wrapper.ignore_sequence_gaps=TRUE

# Java Main class.  This class must implement the WrapperListener interface
#  or guarantee that the WrapperManager class is initialized.  Helper
#  classes are provided to do this for you.  See the Integration section
#  of the documentation for details.
wrapper.java.mainclass=com.integrien.alive.collector.CollectorMain

# Java Classpath (include wrapper.jar)  Add class path elements as
#  needed starting from 1
wrapper.java.classpath.1=%ALIVE_BASE%/collector/lib/vcops-collector-1.0-SNAPSHOT.jar
wrapper.java.classpath.2=%ALIVE_BASE%/common/lib/wrapper.jar
wrapper.java.classpath.3=%ALIVE_BASE%/common/lib/junit.jar
wrapper.java.classpath.4=%ALIVE_BASE%/common/lib/alive_common.jar
wrapper.java.classpath.5=%ALIVE_BASE%/common/lib/xerces.jar
wrapper.java.classpath.6=%ALIVE_BASE%/common/lib/log4j-1.2.14.jar
wrapper.java.classpath.7=%ALIVE_BASE%/common/lib/commons-lang-2.3.jar
wrapper.java.classpath.8=%ALIVE_BASE%/collector/lib/joda-time-1.4.jar
wrapper.java.classpath.9=%ALIVE_BASE%/common/lib/activemq-all-5.5.0.jar
wrapper.java.classpath.10=%ALIVE_BASE%/common/lib/commons-logging-1.1.jar
wrapper.java.classpath.11=%ALIVE_BASE%/collector/lib/ireasoningsnmp.jar
wrapper.java.classpath.12=%ALIVE_BASE%/common/lib/commons-configuration-1.6.jar
wrapper.java.classpath.13=%ALIVE_BASE%/common/lib/commons-collections-3.1.jar
wrapper.java.classpath.14=%ALIVE_BASE%/common/lib/mail.jar
wrapper.java.classpath.15=%ALIVE_BASE%/common/lib/activation.jar
wrapper.java.classpath.16=%ALIVE_BASE%/common/lib/alive_platform.jar
wrapper.java.classpath.17=%ALIVE_BASE%/common/lib/slf4j-log4j12-1.5.11.jar
wrapper.java.classpath.18=%ALIVE_BASE%/collector/lib/commons-discovery-0.4.jar
wrapper.java.classpath.19=%ALIVE_BASE%/collector/lib/axis-1.4.jar
wrapper.java.classpath.20=%ALIVE_BASE%/collector/lib/jaxrpc-api-1.1.jar
wrapper.java.classpath.21=%ALIVE_BASE%/collector/lib/vmware_wsdl4j-1.6.2.jar
wrapper.java.classpath.22=%ALIVE_BASE%/common/lib/vcops-vc-common.jar

# Java Library Path (location of Wrapper.DLL or libwrapper.so)
wrapper.java.library.path.1=%ALIVE_BASE%/common/bin

# Java Additional Parameters
wrapper.java.additional.1=-DALIVE_BASE="%ALIVE_BASE%"
wrapper.java.additional.1.stripquotes=TRUE
wrapper.java.additional.2=-Djava.security.policy="%ALIVE_BASE%/user/conf/policy"
wrapper.java.additional.2.stripquotes=TRUE
wrapper.java.additional.3=-XX:MaxPermSize=196m
wrapper.java.additional.4=-Djava.protocol.handler.pkgs=jcifs
wrapper.java.additional.5=-Dcom.ireasoning.configDir="%ALIVE_BASE%/user/conf"
wrapper.java.additional.5.stripquotes=TRUE
#wrapper.java.additional.6=-XX:+UseGCOverheadLimit
wrapper.java.additional.6=-XX:+UseParallelOldGC
wrapper.java.additional.7=-da
wrapper.java.additional.8=-Djava.rmi.server.hostname=%RMI_ADDRESS%
wrapper.java.additional.9=-XX:+HeapDumpOnOutOfMemoryError
wrapper.java.additional.10=-XX:HeapDumpPath=/data/heapdump/
wrapper.java.additional.11=-XX:OnOutOfMemoryError="/usr/lib/vmware-vcops/user/conf/install/oom-handler.sh %p"
wrapper.java.additional.11.stripquotes=TRUE
wrapper.java.additional.12=-XX:ErrorFile=/data/vcops/log/java/java_error%p.log
wrapper.java.additional.13=-XX:+DisableExplicitGC
wrapper.java.additional.14=-Dun.rmi.dgc.client.gcInterval=3600000
wrapper.java.additional.15=-Djdk.xml.entityExpansionLimit=0


# Java debugging options. Enable them when required. Keep the sequence numbering consistent
#wrapper.java.additional.15=-Xdebug
#wrapper.java.additional.16=-Xrunjdwp:transport=dt_socket,server=y,suspend=n,address=8004

wrapper.ping.timeout=600
wrapper.ping.interval=60
wrapper.startup.timeout=120
wrapper.on_exit.default=RESTART


# Initial Java Heap Size (in MB)
wrapper.java.initmemory=128

# Maximum Java Heap Size (in MB)
wrapper.java.maxmemory=

# Application parameters.  Add parameters as needed starting from 1
#wrapper.app.parameter.1=

#********************************************************************
# Wrapper Logging Properties
#********************************************************************
# Format of output for the console.  (See docs for formats)
wrapper.console.format=PM

# Log Level for console output.  (See docs for log levels)
wrapper.console.loglevel=INFO

# Log file to use for wrapper output logging.
wrapper.logfile=%ALIVE_BASE%/user/log/collector-wrapper.log

# Format of output for the log file.  (See docs for formats)
wrapper.logfile.format=LPTM

# Log Level for log file output.  (See docs for log levels)
wrapper.logfile.loglevel=ERROR

# Maximum size that the log file will be allowed to grow to before
#  the log is rolled. Size is specified in bytes.  The default value
#  of 0, disables log rolling.  May abbreviate with the 'k' (kb) or
#  'm' (mb) suffix.  For example: 10m = 10 megabytes.
wrapper.logfile.maxsize=1024k

# Maximum number of rolled log files which will be allowed before old
#  files are deleted.  The default value of 0 implies no limit.
wrapper.logfile.maxfiles=5

# Log Level for sys/event log output.  (See docs for log levels)
wrapper.syslog.loglevel=NONE

#********************************************************************
# Wrapper Windows Properties
#********************************************************************
# Title to use when running as a console
wrapper.console.title=CollectorService

#********************************************************************
# Wrapper Windows NT/2000/XP Service Properties
#********************************************************************
# WARNING - Do not modify any of these properties when an application
#  using this configuration file has been installed as a service.
#  Please uninstall the service before modifying this section.  The
#  service can then be reinstalled.

# Name of the service
wrapper.ntservice.name=CollectorService

# Display name of the service
wrapper.ntservice.displayname=CollectorService

# Description of the service
wrapper.ntservice.description=CollectorService

# Service dependencies.  Add dependencies as needed starting from 1
wrapper.ntservice.dependency.1=

# Mode in which the service is installed.  AUTO_START or DEMAND_START
wrapper.ntservice.starttype=AUTO_START

# Allow the service to interact with the desktop.
wrapper.ntservice.interactive=false
    '''
fOut = open('wrapper.conf', 'w')
print >>fOut, '%s' % (responses)
fOut.flush()
fOut.close()

fname = fOut.name

output1 = parse_and_resequence_wrapper_conf(responses)
print output1

output2 = parse_and_resequence(fname)
print output2

assert output1 == output2, 'Better check your logic. This one has problems.'

print 'All is well !!!'