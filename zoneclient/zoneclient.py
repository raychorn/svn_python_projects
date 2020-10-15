#!/usr/bin/python
import base64, getopt, urllib, httplib, os, re, sys, stat, string, time, telnetlib, socket, os.path

class MR814Opener(urllib.FancyURLopener):
    http_error_default = urllib.URLopener.http_error_default

    def prompt_user_passwd(self, host, realm):
        return ("admin", self.password)

    def set_password(self,password):
        self.password = password


class FWG114POpener(urllib.FancyURLopener):
    http_error_default = urllib.URLopener.http_error_default

    def prompt_user_passwd(self, host, realm):
        return ("admin", self.password)

    def set_password(self,password):
        self.password = password

class WGR614Opener(urllib.FancyURLopener):
    http_error_default = urllib.URLopener.http_error_default

    def prompt_user_passwd(self, host, realm):
        return ("admin", self.password)

    def set_password(self,password):
        self.password = password

try:
    import syslog
except:  # for platforms without syslog that try to use --syslog option
    class fake_syslog:
        def openlog(self,foo):
            raise Exception("Syslog not supported on this platform")
        def syslog(self,foo):
            raise Exception("Syslog not supported on this platform")
    syslog = fake_syslog()

try:
    from pysnmp import session 
    from pysnmp import error 
except:  
    class fake_session:
        class session:
            def __init__(self, a, c):
                raise Exception("Pysnmp missing, see http://pysnmp.sourceforge.net/")
    session = fake_session()


Version = "0.63"

#
# zoneclient.py  
#
# Copyright GNU GENERAL PUBLIC LICENSE Version 2
# http://www.gnu.org/copyleft/gpl.html
#
# Author  : Kal <kal@users.sourceforge.net>
#
# Acknowledgements
# ================
# 
# All the contributors to http://ipcheck.sourceforge.net/
# 
# OS/2 Adjusted version and minor modifications by Bas Heijermans
# Bas.Heijermans@heppen.be
#
# Jerome Sautret    -Eicon modem support
# Daryl Boyd        -Nortel Instant Internet
# Tony Scicchitano  -New SMC Barricade with password
# Sattler           -Win23 fixes
# Russ Miranda      -DI-713P mods and optfile parsing
# Joe Cotellese     -Netgear MR814 support
# Jay Taylor        -Netgear FWG114P support
# Bob Bolduc        -Netgear WGR614 support
# Glade Diviney     -DI-614_ support
# Mike White        -Netgear -T patch
# Gregory Warnes    -Belkin Pre-N and Linksys VoIP router support
# John Petrocik     -Westel 6100 patch
# Eric Floehr       -FVS318 support
# Bob Bolduc        -NetGear WGR614 support

#
# global constants
#
Updatehost = "dynamic.zoneedit.com"
Updatepage = "/auth/dynamic.html"
Useragent = "zoneclient/" + Version

Touchage = 25                       # days after which to force an update
Linuxip = "/sbin/ifconfig"          # ifconfig command under linux
Win32ip = "ipconfig /all"           # ipconfig command under win32
Sunip = "/usr/sbin/ifconfig"	    # ifconfig command under Sunos
BSDip = "/sbin/ifconfig"            # ifconfig command under BSD
Macip   = "/sbin/ifconfig"          # ifconfig command for MacOS X
Os2ip = "ifconfig"          
Otherip = "/sbin/ifconfig"          

Linuxrt = "/sbin/route -n"
Win32rt = "route print"
Sunrt   = "/bin/netstat -irn"
BSDrt   = "/sbin/route -n get default"
Macrt   = "/usr/sbin/netstat -rn"
Os2rt = "netstat -r get default"
Otherrt   = "/sbin/route -n show"


# regular expression for address
Addressgrep = re.compile ('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')

def Usage():
    print "Version: " + Version
    print
    print "Usage  : zoneclient.py [options] Username Password Hostnames"
    print "or       zoneclient.py [options] --acctfile acct_info_file "
    print "or       zoneclient.py [options] --optfile options_file "
    print
    print "Options:  -a address     manually specify the address "
    print "          -d dir         directory for data files (default current)"
    print "          -e script      execute script after a successful update "
    print "          -f             force update regardless of current state "
    print "          -h             print the detailed help text "
    print "          --help         print all available help text "
    print "          -i interface   interface for local address (default ppp0) "
    print "          -j             disable https "
    print "          -l             log debugging text to zoneclient.log file "
    print "          --syslog       log debugging text to syslog (Unix only) "
    print "          -m             set mx type"
    print "          -n             set node name (deprecated)"
    print "          -q             quiet mode (unless there is an error) "
    print "          -r URL         NAT router, use web IP detection "
    print "          -R URL         alternate web based (searches for WAN IP) "
    print "          -t             test run, do not send the update "
    print "          -v             verbose mode "
    print "          --devices      print router options (Linksys, Netgear, etc)"
    print "          --optfile      read these options from a text file"
    print
    print "Zones can be a comma separated list (no spaces).  Example: "
    print "python zoneclient.py username password zone1.org,zone2.org "

def Devices():
    print
    print "The script will locate the address of your router automatically by "
    print "looking at the default route of the machine you are running on. "
    print "Then it will read the status page for the external IP address "
    print "and use that for updates.  You need to specify the admin password "
    print "with the appropriate option. "
    print
    print "          -A password    Askey or Dynalink RTA210/110 password"
    print "          -B password    New Barricade with password on port 88"
    print "          -F password    SMC Barricade 2401 password "
    print "          -L password    Linksys NAT router password "
    print "          -N password    Netgear (RT311) NAT router password "
    print "          -8 password    Netgear MR814 or FVS318 router password "
    print "          -K password    Netgear FWG114P router password "
    print "          -z password    Netgear WGR614 router password "
    print "          -T password    Netgear (WGT634U) wireless router password "
    print "          -D password    Draytek (Vigor2000) NAT router password "
    print "          -O password    Netopia (R9100) NAT router password "
    print "          -P password    MacSense XRouter Pro password "
    print "          -H password    HawkingTech router password "
    print "          -W password    Watchguard SOHO NAT firewall password "
    print "          -Y password    Cayman DSL 3220H NAT router password "
    print "          -Q pword,iface password and interface for Instant Internet "
    print "          -2 password    Compaq iPAQ Connection Point CP-2W password "
    print 
    print "You can change the default username for the above devices with: "
    print 
    print "          -U username    override default NAT router username "
    print "                         leave this option out to use the default "
    print 
    print "Devices that do not need a username: "
    print 
    print "          -X             Nexland router (no password set) "
    print "          -J             Westel6100 DSL Router "
    print "          -Z password    ZyXEL prestige router password "
    print "          -S             SMC Barricade (no password needed) "
    print "          -M password    Compex NetPassage 15 "
    print "          -G             UgatePlus (no password needed) "
    print "          -E             Eicon Diva 2430 SE ADSL Modem (no password needed) "
    print "          -4 password    DLink DI524 password "
    print "          -5 password    DLink DI614P password "
    print "          -6 password    DLink DI704 password "
    print "          -7 password    DLink DI701 password "
    print "          -9 password    DLink DI713P password "
    print "          -0             Belkin Pre-N (no password needed)"
    print 
    print "Cisco devices: "
    print 
    print "          -C password    Cisco (667i) DSL router password "
    print "          -I password    Cisco (700 series) ISDN router password "
    print 
    print "For Cisco IOS devices and any others that understand SNMP, you "
    print "can also use --snmp to detect the external IP. "
    print 
    print "          --snmp snmp_agent,community,numeric_objectid "
    print 
    print "You will need the pysnmp module from http://pysnmp.sourceforge.net/ "
    print "You also need to know the agent, community and numeric objectid: "
    print "python zoneclient.py --snmp 172.62.254.254,public,.1.3.5.2.1.2.10.2.5.4 ..."
    print "where ... = username password hostnames "
    print

def Help():
    print
    print "Start zoneclient.py with no arguments to get the options screen."
    print
    print "If -f is set, all hosts will be updated regardless of the "
    print "current error, wait or IP state.  You should never need this. "
    print
    print "You can place your username password and hostnames in a file "
    print "(all on the first line) and use the --acctfile option if you do "
    print "not wish your password to show up on a ps. "
    print
    print "You can also place all of the command line arguments in a file "
    print "(all on the first line) and use the --optfile option if you do "
    print "not wish any of the options to show up on a ps. This also gives "
    print "you the ability to put common options in a file, and use them "
    print "from different calls to zoneclient.py. "
    print
    print "The best way to run zoneclient is in the /etc/ppp/ip-up.local file "  
    print "but this won\'t work for many setups.  The script will run from "
    print "a cronjob.  Just make sure the hostnames are the same in each "
    print "execution.  Also, you should make sure it is ran from the same "
    print "directory each time or use the -d option to specify the directory "
    print "where data and error files should be placed. "
    print
    print "The file zoneclient.dat contains the IP address and hostnames "
    print "used in the last update.  If the zoneclient.dat file is older "
    print "than " + `Touchage` + " days, an update will be made to touch "
    print "the hostnames. "
    print 
    print "The file zoneclient.err is created if the response is an error. "
    print "It will not try to update again until this error is resolved. "
    print "You must remove the file yourself once the problem is fixed. "
    print
    print "If you wish to update multiple nodes then execute the script "
    print "multiple times (in different directories): "
    print "cd myzone"
    print "python zoneclient.py -v myzone.com"
    print "cd ../ftp"
    print "python zoneclient.py -v ftp.myzone.com"
    print "cd ../mail"
    print "python zoneclient.py -v mail.myzone.com"
    print
    print "The script can find your public IP address in one of several ways:"
    print 
    print "1) interface IP detection is the default method and appropriate"
    print "if the machine you are running on has an interface with the public"
    print "IP addressed assigned.  The script knows how to query various "
    print "operating systems for the address of an interface specified "
    print "with the -i option (default ppp0).  Note on Win32 systems "
    print "you can specify the MAC address of the device after -i. "
    print 
    print "2) router IP detection is used if you have a routing device"
    print "such as a Netgear RT311.  Use the --devices option to get a"
    print "help on specific devices.  This method is used by the script"
    print "if you specify one of the device-related options."
    print 
    print "3) web IP detection may be used if your device is not supported"
    print "This method is used if you specify the -r option."
    print
    print "4) you can explicitly set the desired IP address with -a"
    print
    print "If your have an unsupported device and are willing to help with"
    print "some testing, email me. "
    print
    print "The zoneclient homepage can be found at:"
    print "http://zoneclient.sourceforge.net/"
    print
    print "Please include the zoneclient.log file if you email me with a problem. "
    print "kal@linsystems.ca"
    print


class Logger:
    #
    # open a new log file in the target dir if logging
    # a race condition if there are tons of scripts
    # starting at the same time and should really use locking
    # but that would be overkill for this app
    #
    def __init__(self, logname = "zoneclient.log", verbose = 0, logging = 0, use_syslog = 0):
        self.logname = logname
        self.verbose = verbose
        self.logging = logging
        self.syslog = use_syslog
        self.prefix = "zoneclient.py: "

        asctime = time.asctime(time.localtime(time.time()))

        if self.syslog == 1:
            syslog.openlog("zoneclient")
        if self.logging == 1:
            self.logfp = open(self.logname, "w")
            self.logfp.write(Useragent + "\n")
            self.logfp.write(self.prefix + asctime + "\n")
            self.logfp.write(self.prefix + "logging to " + self.logname + "\n")
            self.logfp.close()
        if self.verbose:
            print Useragent 
            print self.prefix + asctime 

    # normal logging message
    def logit(self, logline):
        if self.verbose:
            print self.prefix + logline
        if self.logging:
            self.logfp = open(self.logname, "a")
            self.logfp.write(self.prefix + logline + "\n")
            self.logfp.close()
        if self.syslog:
            syslog.syslog(logline)

    # logging message that gets printed even if not verbose
    def logexit(self, logline):
        print self.prefix + logline
        if self.logging:
            self.logfp = open(self.logname, "a")
            self.logfp.write(self.prefix + logline + "\n")
            self.logfp.close()
        if self.syslog:
            syslog.syslog(logline)


def DefaultRoute(logger, Tempfile):
    logger.logit("Searching default route on sys.platform = " + sys.platform)
    iphost = ""
    if sys.platform == "win32":
        logger.logit("WIN32 default route detection for router.")
        os.system (Win32rt + " > " + Tempfile)
        fp = open(Tempfile, "r")
        while 1:
            fileline = fp.readline()
            if not fileline:
                fp.close()
                break
            p1 = string.find(fileline, "0.0.0.0")
            if p1 != -1:
                #
                # replacing findall to support older python 1.5.1 sites
                #
                #ipmatch = Addressgrep.findall(fileline)
                #if ipmatch != None:
                #  if len(ipmatch) > 2:
                #    iphost = ipmatch[2]

                ipmatch = Addressgrep.search(fileline)
                #ip1 = ipmatch.group()
                #p1 = string.find(fileline, ip1) + len(ip1)
                #ipmatch = Addressgrep.search(fileline, p1)
                ip2 = ipmatch.group()
                p2 = string.find(fileline, ip2) + 18  #chris
                #p2 = string.find(fileline, ip2) + len(ip2)
                ipmatch = Addressgrep.search(fileline, p2)
                iphost = ipmatch.group()
                break

    elif string.find(sys.platform, "linux") != -1:
        logger.logit("Linux default route detection for router.")
        os.system (Linuxrt + " > " + Tempfile)
        fp = open(Tempfile, "r")
        while 1:
            fileline = fp.readline()
            if not fileline:
                fp.close()
                break
            p1 = string.find(fileline, "UG")
            if p1 != -1:
                #
                # replacing findall to support older python 1.5.1 sites
                #
                #ipmatch = Addressgrep.findall(fileline)
                #if ipmatch != None:
                #  if len(ipmatch) > 1:
                #    iphost = ipmatch[1]

                ipmatch = Addressgrep.search(fileline)
                ip1 = ipmatch.group()
                p1 = string.find(fileline, ip1) + len(ip1)
                ipmatch = Addressgrep.search(fileline, p1)
                iphost = ipmatch.group()

    elif string.find(sys.platform, "sunos") != -1:
        logger.logit("Sunos default route detection for router.")
        os.system (Sunrt + " > " + Tempfile)
        fp = open(Tempfile, "r")
        while 1:
            fileline = fp.readline()
            if not fileline:
                fp.close()
                break
            p1 = string.find(fileline, "default")
            if p1 != -1:
                ipmatch = Addressgrep.search(fileline, p1+8)
                iphost = ipmatch.group()

    elif string.find(sys.platform, "freebsd") != -1:
        logger.logit("Freebsd default route detection for router.")
        os.system (BSDrt + " > " + Tempfile)
        fp = open(Tempfile, "r")
        while 1:
            fileline = fp.readline()
            if not fileline:
                fp.close()
                break
            p1 = string.find(fileline, "gateway")
            if p1 != -1:
                ipmatch = Addressgrep.search(fileline, p1+8)
                iphost = ipmatch.group()
                break

    elif string.find(sys.platform, "os2") != -1:
        logger.logit("OS2 default route detection for router.")
        os.system (Os2rt + " > " + Tempfile)
        fp = open(Tempfile, "r")
        while 1:
            fileline = fp.readline()
            if not fileline:
                fp.close()
                break
            p1 = string.find(fileline, "default")
            if p1 != -1:
                ipmatch = Addressgrep.search(fileline, p1+8)
                iphost = ipmatch.group()
                break

    elif string.find(string.lower(sys.platform), "darwin") != -1:
        logger.logit("Darwin default route detection for router.")
        os.system (Macrt + " > " + Tempfile)
        fp = open(Tempfile, "r")
        while 1:
            fileline = fp.readline()
            if not fileline:
                break
            p1 = string.find(fileline, "default")
            if p1 != -1:
                ipmatch = Addressgrep.search(fileline, p1+8)
                iphost = ipmatch.group()
                break
        fp.close()

    else:
        logger.logit("Unknown platform default route detection for router.")
        os.system (Otherrt + " > " + Tempfile)
        fp = open(Tempfile, "r")
        while 1:
            fileline = fp.readline()
            if not fileline:
                fp.close()
                break
            p1 = string.find(fileline, "default")
            if p1 != -1:
                #
                # replacing findall to support older python 1.5.1 sites
                #
                #ipmatch = Addressgrep.findall(fileline)
                #if ipmatch != None:
                #  if len(ipmatch) > 1:
                #    iphost = ipmatch[1]

                ipmatch = Addressgrep.search(fileline, p1+8)
                iphost = ipmatch.group()
                break

    return iphost


#
# taken directly from the examples directory in pysnmp distribution
# http://pysnmp.sourceforge.net/
#
# results of run are stored in retval and returned
#
class snmptable (session.session):
    """Retrieve a table from remote SNMP process
    """
    def __init__ (self, agent, community):
        """Explicitly call superclass's constructor as it gets overloaded
           by this class constructor and pass a few arguments alone.
        """   
        session.session.__init__ (self, agent, community)

    def run (self, objids):
        """Query SNMP agent for one or more Object IDs. The objid
           argument should be a list of strings where each string
           represents an Object ID in dotted numbers notation
           (e.g. ['.1.3.6.1.4.1.307.3.2.1.1.1.4.1']).
        """   

        # clear the retval
        retval = []

        # Convert string type Object ID's into numeric representation
        numeric_objids = map (self.str2nums, objids)

        # BER encode SNMP Object ID's to query
        encoded_objids = map (self.encode_oid, numeric_objids)

        # Since we are going to _query_ SNMP agent for Object ID's
        # associated value, there will be no variable values passed to
        # SNMP agent.
        encoded_values = []

        # Remember the beginning of the table
        head_encoded_objid = encoded_objids[0]

        # Traverse the agent's MIB
        while 1:
            # Build a complete SNMP message of type 'GETNEXTREQUEST', pass it
            # a list BER encoded Object ID's to query and an empty list of values
            # associated with these Object ID's (empty list as there is no point
            # to pass any variables values along the SNMP GETNEXT request)
            question = self.encode_request ('GETNEXTREQUEST', encoded_objids, encoded_values)

            # Try to send SNMP message to SNMP agent and receive a response.
            answer = self.send_and_receive (question)

            # Catch SNMP exceptions
            try:
                # As we get a response from SNMP agent, try to disassemble SNMP reply
                # and extract two lists of BER encoded SNMP Object ID's and 
                # associated values).
                (encoded_objids, encoded_values) = self.decode_response (answer)

            # SNMP agent reports 'no such name' when table is over
            except error.SNMPError, why:
                # If NoSuchName
                if why.status == 2:
                    # Return as we are done
                    return retval
                else:
                    raise error.SNMPError(why.status, why.index)

            # Stop at the end of the table
            if not self.oid_prefix_check (head_encoded_objid, encoded_objids[0]):
                # Return as we are done
                return retval

            # Decode BER encoded Object ID.
            objids = map (self.decode_value, encoded_objids)

            # Decode BER encoded values associated with Object ID's.
            values = map (self.decode_value, encoded_values)

            # Convert two lists into a list of tuples for easier printing
            results = map (None, objids, values)

            # Just print them out
            # for (objid, value) in results:
            #    print objid + ' ---> ' + str(value)
            retval = retval + results


def _main(argv):

    # utility function to write response data into a file for debugging
    # !! defined here to pick up definition of 'logger' !!
    def write_response(dir, filename, data):
        # create an output file for the router response
        if dir != "":
            filename = os.path.join(dir, filename)
        fp = open(filename, "w")
        fp.write(data)
        fp.close()
        logger.logit("Wrote router http response to " + filename )


    # 
    # ROUTER SUPPORT GLOBALS 
    # 
    # leave Linksys_host = "" to autodetect via the default route 
    # enter an ip here to skip the autodetect, this goes for all
    # the xxxx_host variables below
    # 

    # 
    # Linksys router support details from bgriggs@pobox.com
    # 
    Linksys_host = ""
    Linksys_user = " "

    # structure holding 'router':router id,
    #                   'page': status page path,
    #                   'markers': list of regular expressions used to locate
    #                             external ip
    Linksys_info = (
        {'router':'BEFSR41',
         'page':'/Status.htm',
         'markers':('WAN','IP')
         },

        {'router':'RT31P2',
         'page':'/RouterStatus.htm',
         'markers':('Internet IP Address:',)
         },

        {'router':'WRT54GL',
         'page':'/Status_Router.asp',
         'markers':('Internet IP',)
         },

        {'router':'WRT54GX2',
         'page':'/Status_Router.asp',
         'markers':('dw(inia)',)
         },

        {'router':'WRT54GS-1',
         'page':'/Status_Router.asp',
         'markers':('Capture(share.ipaddr)',)
         },

        {'router':'WRT54GS-2',
         'page':'/StaRouter.htm',
         'markers':('Capture(share.ipaddr)',)
         },

        {'router':'E4200',
         'page':'/Status_Router.asp',
         'markers':('Capture(setupcontent.interipaddr)',)
         },

        {'router':'unknown',
         'page':'/Status_Router.htm',
         'markers':('Internet IP',)
         }
    )

    # 
    # DLink DI-704 router support 
    # 
    DI704_host = ""
    DI704_user = "root"
    DI704_page = "/cgi-bin/logi"

    # DLink DI-524 router support
    DI524_host = ""
    DI524_user = "admin"
    DI524_page = "/st_device.html"

    # DLink DI-614+ router support
    DI614P_host = ""
    DI614P_user = "admin"
    DI614P_page = "/st_devic.html"

    Macsense_host = ""
    Macsense_user = " "
    Macsense_page = "/Status.htm"

    # 
    # DLink DI-713P router support 
    # 
    DI713P_host = ""
    DI713P_user = "root"
    DI713P_page = "/cgi-bin/logi"

    Macsense_host = ""
    Macsense_user = " "
    Macsense_page = "/Status.htm"

    # 
    # Netgear router support 
    # 
    Netgear_host = ""
    Netgear_user = "admin"
    Netgear_page = "/mtenSysStatus.html" 
    #
    # Netgear MR814
    #
    MR814_host = ""
    MR814_user = "admin"
    MR814_page = "/sysstatus.html"

    #
    # Netgear FWG114P
    #
    FWG114P_host = ""
    FWG114P_user = "admin"
    FWG114P_page = "/s_status.htm"
    # need logout url so that the router wont freak out at people who try to
    # manage it after this script has been recently run (allowing only 1 user
    # to be logged in at a time seems kind of silly if you ask me :P)
    FWG114P_exit = "/logout.htm"

    #
    # Netgear WGR614
    #
    WGR614_host = ""
    WGR614_user = "admin"
    WGR614_page = "/RST_status.htm"

    #
    # Netgear FWG114P
    #
    FWG114P_host = ""
    FWG114P_user = "admin"
    FWG114P_page = "/s_status.htm"
    # need logout url so that the router wont freak out at people who try to
    #
    # Netgear WGT634U
    #
    WGT634U_host = ""
    WGT634U_user = "admin"
    WGT634U_page = "/cgi-bin/maintenance_status.html"

    # 
    # Draytek Vigor2000 router support 
    # 
    Draytek_host = ""
    Draytek_user = "admin"
    Draytek_page = "/doc/digisdn.sht"

    # 
    # Netopia R9100 router support 
    # 
    Netopia_host = ""
    Netopia_user = ""
    Netopia_page = "/WanEvtLog"

    # 
    # Cisco routers (667 and 770) 
    # uses telnet with no user name
    # 
    Cisco_host = ""
    ISDNCisco_host = ""

    # 
    # SMC Barricade
    # 
    SMC_host = ""
    SMC_page = "/status.htm"
    #username and password are not needed 

    # Newer SMC Barricade with password on port 88
    # 
    Barricade_host = ""
    Barricade_user = "admin"
    Barricade_page = "/status.HTM"

    SMC2401_host = ""
    SMC2401_user = "admin"
    SMC2401_page = "/admin\wan.htm"

    # 
    # HawkingTech router support 
    # 
    Hawking_host = ""
    Hawking_user = "admin"
    Hawking_page = "/Monitor.htm"

    # 
    # ZyXEL router support, uses telnet
    # 
    Zyxel_host = ""

    #
    # DI701 router support, uses telnet
    #
    DI701_host = ""

    #
    # Watchguard SOHO firewall/router support
    #
    Watchguard_host = ""
    Watchguard_user = "admin"
    Watchguard_page = "/sysstat.htm"
    Watchguard_page2 = "/external.htm"

    # 
    # Nexland 
    # 
    Nexland_host = ""
    Nexland_page = "/status.htm"
    #username and password are not needed 

    # 
    # Westel
    # 
    Westel_host = ""
    Westel_page = "/advstat.htm"
    #username and password are not needed 

    # 
    # UgatePlus 
    # 
    Ugate_host = ""
    Ugate_page = "/st_dhcp.htm"
    #username and password are not needed 

    # 
    # Belkin Pre-N
    # 
    BelkinPreN_host = ""
    BelkinPreN_page = "/index.html"
    #username and password are not needed 

    # 
    # Eicon Diva 2430 SE ADSL Modem
    # 
    Eicon_host = ""
    Eicon_page = "/Status.htm"
    #username and password are not needed 


    # 
    # Compex NetPassage 15
    # uses telnet with no username
    # 
    Compex_host = ""

    Askey_host = ""

    #
    # Cayman DSL 3220-H
    # uses telnet
    #
    Cayman_host = ""
    Cayman_user = "zoneclient"

    # Instant Internet router
    II_host = ""

    # 
    # Compaq iPAQ Connection Point CP-2W router support details from tom@tomgoff.com
    # 
    iPAQ_host = ""
    iPAQ_user = "admin"
    iPAQ_page = "/_firstpage.htm"

    #
    # default options
    #
    opt_no_https = 0
    opt_gateway = ""
    opt_address = ""
    opt_force = 0
    opt_logging = 0
    opt_syslog  = 0
    opt_verbose = 0
    opt_hostnames = ""
    opt_interface = "ppp0"
    opt_username = ""
    opt_password = ""
    opt_static = 0
    opt_wildcard = 0
    opt_backupmx = 0
    opt_mxhost = ""
    opt_proxy = 0
    opt_router = ""
    opt_wan_router = ""
    opt_guess = 0
    opt_quiet = 0
    opt_offline = 0
    opt_execute = ""
    opt_directory = ""
    opt_acctfile = ""
    opt_natuser = ""
    opt_Linksys_password = ""
    opt_Macsense_password = ""
    opt_Linksys_router = 0
    opt_Netgear_password = ""
    opt_MR814_password = ""
    opt_WGT634U_password = ""
    opt_Draytek_password = ""
    opt_Netopia_password = ""
    opt_Cisco_password = ""
    opt_SMC_router = 0
    opt_Nexland_router = 0
    opt_Westel_router = 0
    opt_ISDNCisco_password = ""
    opt_Hawking_password = ""
    opt_Zyxel_password = ""
    opt_Watchguard_password = ""
    opt_DI701_password = ""
    opt_snmp_agent = ""
    opt_snmp_community = ""
    opt_snmp_objectid = ""
    opt_snmp_agent_prefix = ""
    opt_custom = 0
    opt_testrun = 0
    opt_makedat = 0
    opt_Compex_password = ""
    opt_Cayman_password = ""
    opt_II_password = ""
    opt_II_interface = ""
    opt_Ugate_router = 0
    opt_FWG114P_password = ""
    opt_WGR614_password = ""
    opt_BelkinPreN_router = 0
    opt_Eicon_router = 0
    opt_Barricade_password = ""
    opt_SMC2401_password = ""
    opt_DI704_password = ""
    opt_DI713P_password = ""
    opt_DI614P_password = ""
    opt_DI524_password = ""
    opt_Askey_password = ""
    opt_iPAQ_password = ""
    opt_iPAQ_router = 0

    opt_mxtype = 0
    opt_node = ""

    #
    # parse the command line options
    #
    if len(argv) == 1:
        Usage()
        sys.exit(0)

    short1 = "a:d:e:fhi:jlmn:qr:tv"
    short2 = "A:B:C:D:EF:G:H:IK:L:M:N:O:P:Q:R:T:SU:W:XY:Z:Jz:"
    short3 = "2:4:5:6:7:8:9:0"
    short_opts = short1 + short2 + short3
    long_opts = ["gateway=", "syslog", "acctfile=", "help", "devices", "snmp=", "optfile="]

    try:
        opts, args = getopt.getopt(argv[1:], short_opts, long_opts)
    except getopt.error, reason:
        print reason
        sys.exit(-1)

    #
    # PYTHON GURU NEEDED
    #
    # Is there any way in python to set argv to hide the command line?
    # ala the perl $0 = "orcus [accepting connections]";
    #
    # http://theoryx5.uwinnipeg.ca/CPAN/perl/pod/perlfaq8/Is_there_a_way_to_hide_perl_s_command_line_from_programs_such_as_ps_.html
    #

    # This doesn't hide the command line, but it's effective enough to
    # just get the options from a file instead.
    # Expand --optfile arguments (they can nest, be careful of loops!)

    build_opts = 1
    start_pos = 0
    while build_opts:
        for pos in range(start_pos, len(opts)):
            (lopt, ropt) = opts[pos]
            if lopt == "--optfile":
                if os.path.isfile(ropt):
                    try:
                        fp = open (ropt, "r")
                        optdata = fp.read()
                        spltopt = string.split(optdata)
                        filopts, filargs = getopt.getopt(spltopt, short_opts, long_opts)
                        opts[pos:pos + 1] = filopts
                        args = args + filargs
                        fp.close()
                        start_pos = pos
                        break
                    except:
                        print "bad optfile: " + ropt
                        sys.exit(-1)
                else:
                    print "bad optfile: " + ropt
                    sys.exit(-1)
        build_opts = 0
    #
    # check verbose, logging and detailed help options first
    # check directory to place logging file
    #
    for opt in opts:
        (lopt, ropt) = opt
        if lopt == "-l":
            opt_logging = 1
        elif lopt == "--syslog":
            opt_syslog = 1
        elif lopt == "-v":
            opt_verbose = 1
        elif lopt == "--devices":
            Devices()
            sys.exit(0)
        elif lopt == "--help":
            Usage()
            Devices()
            Help()
            sys.exit(0)
        elif lopt == "-h":
            Help()
            sys.exit(0)
        elif lopt == "-d":
            if os.path.isdir(ropt):
                opt_directory = ropt
            else:
                print "bad directory option"
                sys.exit()

            # fix the dir name to end in slash
            if opt_directory[-1:] != "/":
                opt_directory = opt_directory + "/"

    #
    # create the logger object
    #
    if opt_directory == "":
        logger = Logger("zoneclient.log", opt_verbose, opt_logging, opt_syslog)
    else:
        logger = Logger(opt_directory + "zoneclient.log", opt_verbose, opt_logging, opt_syslog)
        logline = "opt_directory set to " + opt_directory
        logger.logit(logline)

    #
    # check acctfile option
    #
    for opt in opts:
        (lopt, ropt) = opt
        if lopt == "--acctfile":
            opt_acctfile = ropt
            logline = "opt_acctfile set to " + opt_acctfile
            logger.logit(logline)

    if len(args) != 3 and opt_acctfile == "":
        Usage()
        sys.exit(0)

    #
    # okay now parse rest of the options and log as needed

    for opt in opts:
        (lopt, ropt) = opt
        if lopt == "-a":
            opt_address = ropt
            logline = "opt_address set to " + opt_address
            logger.logit(logline)
        elif lopt == "-i":
            opt_interface = ropt
            logline = "opt_interface set to " + opt_interface
            logger.logit(logline)
        elif lopt == "-f":
            opt_force = 1
            logline = "opt_force set " 
            logger.logit(logline)
        elif lopt == "-j":
            opt_no_https = 1
            logline = "opt_no_https set " 
            logger.logit(logline)
        elif lopt == "-w":
            opt_wildcard = 1
            logline = "opt_wildcard set " 
            logger.logit(logline)
        elif lopt == "-s":
            opt_static = 1
            logline = "opt_static set " 
            logger.logit(logline)
        elif lopt == "-c":
            opt_custom = 1
            logline = "opt_custom set " 
            logger.logit(logline)
        elif lopt == "-b":
            opt_backupmx = 1
            logline = "opt_backupmx set " 
            logger.logit(logline)
        elif lopt == "-p":
            opt_proxy = 1
            logline = "opt_proxy set " 
            logger.logit(logline)
        elif lopt == "-m":
            opt_mxtype = 1
            logline = "opt_mxtype set"
            logger.logit(logline)
        elif lopt == "-n":
            opt_node = ropt
            logline = "opt_node set to " + opt_node
            logger.logit(logline)
        elif lopt == "-R":
            opt_wan_router = ropt
            logline = "opt_wan_router set to " + opt_wan_router
            logger.logit(logline)
        elif lopt == "-r":
            opt_router = ropt
            logline = "opt_router set to " + opt_router
            logger.logit(logline)
        elif lopt == "-g":
            opt_guess = 1
            logline = "opt_guess set " 
            logger.logit(logline)
        elif lopt == "-t":
            opt_testrun = 1
            logline = "opt_testrun set " 
            logger.logit(logline)
        elif lopt == "--makedat":
            opt_makedat = 1
            logline = "opt_makedat set " 
            logger.logit(logline)
        elif lopt == "-q":
            opt_quiet = 1
            logline = "opt_quiet set " 
            logger.logit(logline)
        elif lopt == "-o":
            opt_offline = 1
            logline = "opt_offline set " 
            logger.logit(logline)
        elif lopt == "-e":
            opt_execute = ropt
            logline = "opt_execute set to " + opt_execute
            logger.logit(logline)
        elif lopt == "-U":
            opt_natuser = ropt
            logline = "opt_natuser set to " + opt_natuser
            logger.logit(logline)

            Linksys_user = opt_natuser
            DI524_user = opt_natuser
            DI614P_user = opt_natuser
            DI704_user = opt_natuser
            Macsense_user = opt_natuser
            DI713P_user = opt_natuser
            Macsense_user = opt_natuser
            Netgear_user = opt_natuser
            WGT634U_user = opt_natuser
            Draytek_user = opt_natuser
            Netopia_user = opt_natuser
            Barricade_user = opt_natuser
            SMC2401_user = opt_natuser
            Hawking_user = opt_natuser
            Watchguard_user = opt_natuser
            Cayman_user = opt_natuser
            iPAQ_user = opt_natuser

        elif lopt == "-B":
            opt_Barricade_password = ropt
            logline = "opt_Barricade_password = "
            for x in xrange(0, len(ropt)):
                logline = logline + "*"
            logger.logit(logline)
        elif lopt == "-F":
            opt_SMC2401_password = ropt
            logline = "opt_SMC2401_password = "
            for x in xrange(0, len(ropt)):
                logline = logline + "*"
            logger.logit(logline)
        elif lopt == "-L":
            opt_Linksys_router = 1
            opt_Linksys_password = ropt
            logline = "opt_Linksys_password = "
            for x in xrange(0, len(ropt)):
                logline = logline + "*"
            logger.logit(logline)
        elif lopt == "-P":
            opt_Macsense_password = ropt
            logline = "opt_Macsense_password = "
            for x in xrange(0, len(ropt)):
                logline = logline + "*"
            logger.logit(logline)
        elif lopt == "-N":
            opt_Netgear_password = ropt
            logline = "opt_Netgear_password = "
            for x in xrange(0, len(ropt)):
                logline = logline + "*"
            logger.logit(logline)
        elif lopt == "-8":
            opt_MR814_password = ropt
            logline = "opt_MR814_password = "
            for x in xrange (0, len(ropt)):
                logline = logline + "*"
            logger.logit(logline)
        elif lopt == "-K":
            opt_FWG114P_password = ropt
            logline = "opt_FWG114P_password = "
            for x in xrange (0, len(ropt)):
                logline = logline + "*"
            logger.logit(logline)
        elif lopt == "-z":
            opt_WGR614_password = ropt
            logline = "opt_MGR614_password = "
            for x in xrange (0, len(ropt)):
                logline = logline + "*"
            logger.logit(logline)
        elif lopt == "-T":
            opt_WGT634U_password = ropt
            logline = "opt_WGT634U_password = "
            for x in xrange (0, len(ropt)):
                logline = logline + "*"
            logger.logit(logline)
        elif lopt == "-D":
            opt_Draytek_password = ropt
            logline = "opt_Draytek_password = "
            for x in xrange(0, len(ropt)):
                logline = logline + "*"
            logger.logit(logline)
        elif lopt == "-O":
            opt_Netopia_password = ropt
            logline = "opt_Netopia_password = "
            for x in xrange(0, len(ropt)):
                logline = logline + "*"
            logger.logit(logline)
        elif lopt == "-C":
            opt_Cisco_password = ropt
            logline = "opt_Cisco_password = "
            for x in xrange(0, len(ropt)):
                logline = logline + "*"
            logger.logit(logline)
        elif lopt == "-S":
            opt_SMC_router = 1
            logline = "opt_SMC_router set " 
            logger.logit(logline)
        elif lopt == "-G":
            opt_Ugate_router = 1
            logline = "opt_Ugate_router set " 
            logger.logit(logline)
        elif lopt == "-0":
            opt_BelkinPreN_router = 1
            logline = "opt_BelkinPreN_router set " 
            logger.logit(logline)
        elif lopt == "-E":
            opt_Eicon_router = 1
            logline = "opt_Eicon_router set " 
            logger.logit(logline)
        elif lopt == "-X":
            opt_Nexland_router = 1
            logline = "opt_Nexland_router set " 
            logger.logit(logline)
        elif lopt == "-J":
            opt_Westel_router = 1
            logline = "opt_Westel_router set " 
            logger.logit(logline)
        elif lopt == "-I":
            opt_ISDNCisco_password = ropt
            logline = "opt_ISDNCisco_password = "
            for x in xrange(0, len(ropt)):
                logline = logline + "*"
            logger.logit(logline)
        elif lopt == "-H":
            opt_Hawking_password = ropt
            logline = "opt_Hawking_password = "
            for x in xrange(0, len(ropt)):
                logline = logline + "*"
            logger.logit(logline)
        elif lopt == "-Z":
            opt_Zyxel_password = ropt
            logline = "opt_Zyxel_password = "
            for x in xrange(0, len(ropt)):
                logline = logline + "*"
            logger.logit(logline)
        elif lopt == "-4":
            opt_DI524_password = ropt
            logline = "opt_D524_password = "
            for x in xrange(0, len(ropt)):
                logline = logline + "*"
            logger.logit(logline)
        elif lopt == "-5":
            opt_DI614P_password = ropt
            logline = "opt_D614P_password = "
            for x in xrange(0, len(ropt)):
                logline = logline + "*"
            logger.logit(logline)
        elif lopt == "-6":
            opt_DI704_password = ropt
            logline = "opt_DI704_password = "
            for x in xrange(0, len(ropt)):
                logline = logline + "*"
            logger.logit(logline)
        elif lopt == "-7":
            opt_DI701_password = ropt
            logline = "opt_DI701_password = "
            for x in xrange(0, len(ropt)):
                logline = logline + "*"
            logger.logit(logline)
        elif lopt == "-9":
            opt_DI713P_password = ropt
            logline = "opt_DI713_password = "
            for x in xrange(0, len(ropt)):
                logline = logline + "*"
            logger.logit(logline)
        elif lopt == "-W":
            opt_Watchguard_password = ropt
            logline = "opt_Watchguard_password = "
            for x in xrange(0, len(ropt)):
                logline = logline + "*"
            logger.logit(logline)
        elif lopt == "-M":
            opt_Compex_password = ropt
            logline = "opt_Compex_password = "
            for x in xrange(0, len(ropt)):
                logline = logline + "*"
            logger.logit(logline)
        elif lopt == "-Y":
            opt_Cayman_password = ropt
            logline = "opt_Cayman_password = "
            for x in xrange(0, len(ropt)):
                logline = logline + "*"
            logger.logit(logline)

        elif lopt == "-A":
            opt_Askey_password = ropt
            logline = "opt_Askey_password = "
            for x in xrange(0, len(ropt)):
                logline = logline + "*"
            logger.logit(logline)

        elif lopt == "-Q":
            Qopts = string.split(ropt, ",")
            if len(Qopts) != 2:
                logline = "Bad -Q option: " + ropt
                logger.logexit(logline)
                sys.exit(-1)
            opt_II_password = Qopts[0]
            opt_II_interface = Qopts[1]
            logline = "opt_II_password = "
            for x in xrange(0, len(opt_II_password)):
                logline = logline + "*"
            logger.logit(logline)
            logline = "opt_II_interface = " + opt_II_interface
            logger.logit(logline)

        elif lopt == "-2":
            opt_iPAQ_router = 1
            opt_iPAQ_password = ropt
            logline = "opt_iPAQ_password = "
            for x in xrange(0, len(ropt)):
                logline = logline + "*"
            logger.logit(logline)

        elif lopt == "--gateway":
            opt_gateway = ropt
            logline = "opt_gateway = " + opt_gateway
            logger.logit(logline)

        elif lopt == "--snmp":

            snmpopts = string.split(ropt, ",")
            if len(snmpopts) != 3:
                logline = "Bad --snmp option: " + ropt
                logger.logexit(logline)
                sys.exit(-1)

            #
            # check snmp agent is an IP address
            #
            opt_snmp_agent = snmpopts[0]
            p1 = string.find(opt_snmp_agent, ".")
            p2 = string.find(opt_snmp_agent, ".", p1+1)
            p3 = string.find(opt_snmp_agent, ".", p2+1)
            p4 = string.find(opt_snmp_agent, ".", p3+1)
            if p1 == -1 or p2 == -1 or p3 == -1 or p4 != -1:
                logline = opt_snmp_agent + " bad snmp agent, IP address required"
                logger.logexit(logline)
                sys.exit(-1)
            opt_snmp_agent_prefix = opt_snmp_agent[:p2]

            #
            # community can be anything
            #
            opt_snmp_community = snmpopts[1]

            #
            # check the objectid is numeric
            #
            opt_snmp_objectid = snmpopts[2]
            #objid_s = string.split(opt_snmp_objectid, '.')
            #objid_s = filter(lambda x: len(x), objid_s)
            #try:
            #  objid_n = map(lambda x: string.atol(x), objid_s)
            #except:
            #  logline = opt_snmp_objectid + " bad snmp objectid, numeric id required"
            #  logger.logexit(logline)
            #  sys.exit(-1)

            logger.logit("opt_snmp_agent = " + opt_snmp_agent)
            logger.logit("opt_snmp_agent_prefix = " + opt_snmp_agent_prefix)
            logger.logit("opt_snmp_community = " + opt_snmp_community)
            logger.logit("opt_snmp_objectid = " + opt_snmp_objectid)


    #
    # store the command line arguments
    #
    if opt_acctfile != "":
        try:
            fp = open (opt_acctfile, "r")
            acctdata = fp.read()
            fp.close()
        except:
            logline = "Bad acctfile: " + opt_acctfile
            logger.logexit(logline)
            sys.exit(-1)
        args = string.split(acctdata)
        if len(args) != 3:
            logline = "File does not contain 3 arguments: " + opt_acctfile
            logger.logexit(logline)
            sys.exit(-1)

    opt_username = args[0] 
    logline = "opt_username = " + opt_username
    logger.logit(logline)

    opt_password = args[1] 
    logline = "opt_password = " 
    for x in xrange(0, len(opt_password)):
        logline = logline + "*"
    logger.logit(logline)

    opt_hostnames = args[2] 
    logline = "opt_hostnames = " + opt_hostnames
    logger.logit(logline)
    hostnames = string.split(opt_hostnames, ",")

    #
    # taint check, make sure each hostname is a dotted fqdn
    #
    for host in hostnames:
        if string.find(host, ".") == -1:
            logline = "Bad hostname: " + host
            logger.logexit(logline)
            sys.exit(-1)

    #
    # taint check the mx host
    #
    if opt_mxhost != "":
        if string.find(opt_mxhost, ".") == -1:
            logline = "Bad mxhost: " + opt_mxhost
            logger.logexit(logline)
            sys.exit(-1)

    #
    # log the pwd
    #
    if os.environ.has_key("PWD"):
        logger.logit("PWD = " + os.environ["PWD"])

    #
    # create the full path names
    #
    Datfile = ""
    if opt_node == "":
        Datfile = "zoneclient.dat"
    else:
        Datfile = opt_node + ".dat"
    if opt_directory != "":
        Datfile = opt_directory + Datfile
        logger.logit("Datfile = " + Datfile)
    Errfile = "zoneclient.err"
    if opt_directory != "":
        Errfile = opt_directory + Errfile
        logger.logit("Errfile = " + Errfile)
    Waitfile = "zoneclient.wait"
    if opt_directory != "":
        Waitfile = opt_directory + Waitfile
        logger.logit("Waitfile = " + Waitfile)
    Htmlfile = "zoneclient.html"
    if opt_directory != "":
        Htmlfile = opt_directory + Htmlfile
        logger.logit("Htmlfile = " + Htmlfile)
    Tempfile = "zoneclient.tmp"
    if opt_directory != "":
        Tempfile = opt_directory + Tempfile
        logger.logit("Tempfile = " + Tempfile)


    #
    # determine the local machine's ip
    #
    localip = ""
    if opt_address != "":
        logger.logit("manually setting localip with -a")
        localip = opt_address
    elif opt_snmp_agent != "":
        logger.logit("trying snmp localip detection")

        # Create an instance of snmptable class
        instance = snmptable (opt_snmp_agent, opt_snmp_community)

        # Run snmptable against passed Object ID's 
        retval = []
        try:
            retval = instance.run([opt_snmp_objectid])
        except:
            logline = "Snmp session failed." 
            logger.logexit(logline)
            sys.exit(-1)

        agentlen = len(opt_snmp_agent_prefix)
        objectlen = len(opt_snmp_objectid) + 1
        for (objid, value) in retval:
            logger.logit(objid + ' ---> ' + str(value))
            objval = objid[objectlen:]
            if objval[:agentlen] != opt_snmp_agent_prefix:
                localip = objval
                logger.logit("IP matched: " + localip)
                # match the last one so all options are printed in the log
                #break

    elif opt_SMC2401_password != "":
        # 
        # 
        ipdir = SMC2401_page

        #
        # determine the router host address
        # 
        iphost = ""
        if SMC2401_host != "":
            logger.logit("SMC2401_host set explicitly.")
            iphost = SMC2401_host
        else:
            iphost = DefaultRoute(logger, Tempfile)

        if iphost == "":
            logger.logit("No router ip detected.  Assuming 192.168.1.1")
            iphost = "192.168.1.1"
        else:
            logline = "Trying router at " + iphost
            logger.logit(logline)

        logger.logit("Trying SMC2401 with user " + SMC2401_user)

        # connect to the router's admin webpage
        try:
            h1 = httplib.HTTP(iphost)

            h1.putrequest("GET", SMC2401_page)
            h1.putheader("USER-AGENT", Useragent)
            authstring = base64.encodestring(SMC2401_user + ":" + opt_SMC2401_password)
            authstring = string.replace(authstring, "\012", "")
            h1.putheader("AUTHORIZATION", "Basic " + authstring)
            h1.endheaders()
            errcode, errmsg, headers = h1.getreply()
            fp = h1.getfile()
            ipdata = fp.read()
            fp.close()
        except:
            logline = "No address found on router at " + iphost
            logger.logexit(logline)
            sys.exit(-1)

        # create an output file of the response
        filename = "smc2401.out"
        if opt_directory != "":
            filename = opt_directory + filename
        fp = open(filename, "w")
        fp.write(ipdata)
        fp.close()
        logger.logit("smc2401.out file created")

        # look for local ip in the log
        p1 = 0
        if p1 != -1:
            ipmatch = Addressgrep.search(ipdata, p1)
            if ipmatch != None:
                localip = ipmatch.group()
                logger.logit("IP matched: " + localip)


    elif opt_Barricade_password != "":
        # 
        # Newer SMC Barricade with passwords on port 88
        # 
        ipdir = Barricade_page

        #
        # determine the router host address
        # 
        iphost = ""
        if Barricade_host != "":
            logger.logit("Barricade_host set explicitly.")
            iphost = Barricade_host
        else:
            iphost = DefaultRoute(logger, Tempfile)

        if iphost == "":
            logger.logit("No router ip detected.  Assuming 192.168.2.1")
            iphost = "192.168.2.1"
        else:
            logline = "Trying router at " + iphost
            logger.logit(logline)

        logger.logit("Trying new Barricade with password")

        try:
            #ipurl = "http://" + iphost + ":88/login.htm"
            ipurl = "http://" + iphost + ":88/"
            logger.logit("urlopen " + ipurl)
            urlfp = urllib.urlopen(ipurl)
            logger.logit("urlfp.read")
            ipdata = urlfp.read()
            logger.logit("urlfp.close")
            urlfp.close()
            logger.logit("filename = login.out")
            filename = "login.out"
            if opt_directory != "":
                filename = opt_directory + filename
            logger.logit("file open")
            fp = open(filename, "w")
            logger.logit("write data")
            fp.write(ipdata)
            logger.logit("file close")
            fp.close()
            logger.logit("login.out file created")
        except:
            logline = "Failed to get login form"
            logger.logexit(logline)
            sys.exit(-1)

        try:
            logger.logit("Try to post to form")
            params = urllib.urlencode({'pws': opt_Barricade_password, 'page':'login'})
            #ipurl = "http://" + iphost + ":88/login.htm"
            ipurl = "http://" + iphost + ":88/"
            logger.logit("urlopen " + ipurl)
            urlfp = urllib.urlopen(ipurl, params)
            logger.logit("urlfp.read")
            ipdata = urlfp.read()
            logger.logit("urlfp.close")
            urlfp.close()
            filename = "post.out"
            if opt_directory != "":
                filename = opt_directory + filename
            fp = open(filename, "w")
            fp.write(ipdata)
            fp.close()
            logger.logit("post.out file created")
        except:
            logline = "Failed to post password to login form"
            logger.logexit(logline)
            sys.exit(-1)

        try:
            logger.logit("Now try to access status.HTM on port 88")
            params = urllib.urlencode({'pws': opt_Barricade_password})
            ipurl = "http://" + iphost + ":88/status.HTM"
            urlfp = urllib.urlopen(ipurl, params)
            ipdata = urlfp.read()
            urlfp.close()

            filename = "barricade.out"
            if opt_directory != "":
                filename = opt_directory + filename
            fp = open(filename, "w")
            fp.write(ipdata)
            fp.close()
            logger.logit("barricade.out file created")
        except:
            logline = "Failed accessing status page "
            logger.logexit(logline)
            sys.exit(-1)

        # look for the last Default gateway 
        p1 = string.rfind(ipdata, "WAN IP")
        if p1 != -1:
            ipmatch = Addressgrep.search(ipdata, p1)
            if ipmatch != None:
                localip = ipmatch.group()
                logger.logit("IP matched: " + localip)


    elif opt_Cayman_password != "":
        #
        # Cayman DSL 3220H router ip detection
        #
        #   This code was written for and tested on Device Firmware
        #   GatorSurf version 5.6.2 (build R0)
        #   with PPP / NAT

        #
        # determine the router host address
        #
        iphost = ""
        if Cayman_host != "":
            logger.logit("Cayman_host set explicitly.")
            iphost = Cayman_host
        else:
            iphost = DefaultRoute(logger, Tempfile)

        if iphost == "":
            logger.logit("No router ip detected.  Assuming 192.168.1.254")
            iphost = "192.168.1.254"
        else:
            logline = "Trying router at " + iphost
            logger.logit(logline)

        # connect to the router's admin console interface
        try:
            logger.logit("Trying Cayman DSL 3220H")
            tn = telnetlib.Telnet(iphost)
            logger.logit("Creating telnetlib obj done")
            tn.read_until("ogin:")
            logger.logit("Login prompt found")
            tn.write(Cayman_user + "\r\n")
            logger.logit("Cayman_user sent")
            tn.read_until("assword:")
            logger.logit("Password prompt found")
            tn.write(opt_Cayman_password + "\r\n")
            logger.logit("opt_Cayman_password sent")
            tn.read_until(">")
            tn.write("show ip interface\r\n")
            logger.logit("show ip interface command sent")
            ipdata = tn.read_until(">", 2000)
            tn.write("exit\r\n")
            logger.logit("exit command sent")
        except:
            logline = "No address found on router at " + iphost
            logger.logexit(logline)
            sys.exit(-1)

        # create an output file of the response
        filename = "cayman.out"
        if opt_directory != "":
            filename = opt_directory + filename
        fp = open(filename, "w")
        fp.write(ipdata)
        fp.close()
        logger.logit("cayman.out file created")

        # look for the WAN device in ipdata
        p1 = string.rfind(ipdata, "PPP")
        if p1 != -1:
            ipmatch = Addressgrep.search(ipdata, p1+1)
            if ipmatch != None:
                localip = ipmatch.group()
                logger.logit("IP matched: " + localip)

    elif opt_Askey_password != "":
        #
        # Askey
        #

        #
        # determine the router host address
        #
        iphost = ""
        if Askey_host != "":
            logger.logit("Askey_host set explicitly.")
            iphost = Askey_host
        else:
            iphost = DefaultRoute(logger, Tempfile)

        if iphost == "":
            logger.logit("No router ip detected.  Assuming 170.20.1.220")
            iphost = "170.20.1.220"
        else:
            logline = "Trying router at " + iphost
            logger.logit(logline)

        # connect to the router's admin console interface
        ipdata = ""
        try:
            logger.logit("Trying Askey")
            tn = telnetlib.Telnet(iphost)
            logger.logit("Creating telnetlib obj done")
            tn.read_until("assword:")
            logger.logit("Password prompt found")
            tn.write(opt_Askey_password + "\r\n")
            logger.logit("opt_Askey_password sent")
            tn.read_until(">")
            tn.write("menu start\r\n")
            logger.logit("menu start command sent")
            tn.read_until("Select")
            tn.write("5\r\n")
            logger.logit("menu option 5 sent")
            tn.read_until("Select")
            tn.write("52\r\n")
            logger.logit("menu option 52 sent")
            ipdata = tn.read_until("Select", 2000)
            tn.write("99\r\n")
            logger.logit("menu option 99 sent")
            tn.write("@close\r\n")
            logger.logit("@close sent")
        except:
            logline = "Telnet object exception " + iphost
            logger.logexit(logline)

        if len(ipdata) == 0:
            logline = "No data found on router at " + iphost
            logger.logexit(logline)
            sys.exit(-1)

        # create an output file of the response
        filename = "askey.out"
        if opt_directory != "":
            filename = opt_directory + filename
        fp = open(filename, "w")
        fp.write(ipdata)
        fp.close()
        logger.logit("askey.out file created")

        # look for the WAN device in ipdata
        ipmatch = Addressgrep.search(ipdata)
        if ipmatch != None:
            localip = ipmatch.group()
            logger.logit("IP matched: " + localip)

    elif opt_Compex_password != "":
        #
        # Compex NetPassage 15 router ip detection
        #
        #   This code was written for and tested on Device Firmware
        #   version "2.67 Build 1005, Mar 5 2001"

        #
        # determine the router host address
        #
        iphost = ""
        if Compex_host != "":
            logger.logit("Compex_host set explicitly.")
            iphost = Compex_host
        else:
            iphost = DefaultRoute(logger, Tempfile)

        if iphost == "":
            logger.logit("No router ip detected.  Assuming 192.168.168.1")
            iphost = "192.168.168.1"
        else:
            logline = "Trying router at " + iphost
            logger.logit(logline)

        # connect to the router's admin console interface
        try:
            logger.logit("Trying Compex NetPassage 15")
            tn = telnetlib.Telnet(iphost)
            logger.logit("Creating telnetlib obj done")
            tn.read_until("assword:")
            logger.logit("Password prompt found")
            tn.write(opt_Compex_password + "\r\n")
            logger.logit("opt_Compex_password sent")
            tn.read_until("ommand>")
            tn.write("show ip\r\n")
            logger.logit("show ip command sent")
            ipdata = tn.read_until("ommand>", 2000)
            tn.write("exit\r\n")
            logger.logit("exit command sent")
        except:
            logline = "No address found on router at " + iphost
            logger.logexit(logline)
            sys.exit(-1)

        # create an output file of the response
        filename = "compex.out"
        if opt_directory != "":
            filename = opt_directory + filename
        fp = open(filename, "w")
        fp.write(ipdata)
        fp.close()
        logger.logit("compex.out file created")

        # look for the WAN device in ipdata
        p1 = string.rfind(ipdata, "WAN")
        if p1 != -1:
            ipmatch = Addressgrep.search(ipdata, p1)
            if ipmatch != None:
                localip = ipmatch.group()
                logger.logit("IP matched: " + localip)

    elif opt_II_password != "":
        # 
        # Instant Internet router ip detection
        # 

        #
        # determine the router host address
        # 
        iphost = ""
        if II_host != "":
            logger.logit("II_host set explicitly.")
            iphost = II_host
        else:
            iphost = DefaultRoute(logger, Tempfile)

        if iphost == "":
            logger.logit("No router ip detected.  Assuming 192.168.1.1")
            iphost = "192.168.1.1"
        else:
            logline = "Trying router at " + iphost
            logger.logit(logline)

        # connect to the router's admin webpage
        try:
            logger.logit("Trying Instant Internet ")
            tn = telnetlib.Telnet(iphost)
            logger.logit("Creating telnetlib obj done")
            tn.read_until("assword:")
            logger.logit("Password prompt found")
            tn.write(opt_II_password + "\r\n")
            logger.logit("opt_II_password sent")
            tn.write("ppp " + opt_II_interface + "\r\n")
            logger.logit("ppp " + opt_II_interface + " sent")
            ip1 = tn.read_until("state:", 2000)
            logger.logit("ip read")
            tn.write("exit\r\n")
            logger.logit("exit sent")
            ipdata = ip1
        except:
            logline = "No address found on router at " + iphost
            logger.logexit(logline)
            sys.exit(-1)


        # create an output file of the response
        filename = "II.out"
        if opt_directory != "":
            filename = opt_directory + filename
        fp = open(filename, "w")
        fp.write(ipdata)
        fp.close()
        logger.logit("II.out file created")

        # look for the last ipadr device in the log
        p1 = string.rfind(ipdata, "ipadr local:")
        if p1 != -1:
            ipmatch = Addressgrep.search(ipdata, p1)
            if ipmatch != None:
                localip = ipmatch.group()
                logger.logit("IP matched: " + localip)

    elif opt_Zyxel_password != "":
        # 
        # ZyXEL router ip detection
        # 

        #
        # determine the router host address
        # 
        iphost = ""
        if Zyxel_host != "":
            logger.logit("Zyxel_host set explicitly.")
            iphost = Zyxel_host
        else:
            iphost = DefaultRoute(logger, Tempfile)

        if iphost == "":
            logger.logit("No router ip detected.  Assuming 192.168.1.1")
            iphost = "192.168.1.1"
        else:
            logline = "Trying router at " + iphost
            logger.logit(logline)

        # connect to the router's admin webpage
        try:
            logger.logit("Trying ZyXEL Prestige 312")
            tn = telnetlib.Telnet(iphost)
            logger.logit("Creating telnetlib obj done")
            tn.read_until("assword:")
            logger.logit("Password prompt found")
            tn.write(opt_Zyxel_password + "\r\n")
            logger.logit("opt_Zyxel_password sent")
            #tn.read_until("Menu Selection Number:")
            tn.write("24\r\n")
            logger.logit("menu number 24 sent")
            #tn.read_until("Menu Selection Number:")
            tn.write("8\r\n")
            logger.logit("menu number 8 sent")
            tn.write("ip ifconfig\r\n")
            logger.logit("ip ifconfig sent")
            ip1 = tn.read_until("netmask", 3000)
            ip2 = tn.read_until("netmask 0xf", 3000)
            logger.logit("ip1 and ip2 read")
            tn.write("exit\r\n")
            logger.logit("exit sent")
            #tn.read_until("Menu Selection Number:")
            tn.write("99\r\n")
            logger.logit("menu number 99 sent")
            ipdata = ip1 + ip2
        except:
            logline = "No address found on router at " + iphost
            logger.logexit(logline)
            sys.exit(-1)

        # create an output file of the response
        filename = "zyxel.out"
        if opt_directory != "":
            filename = opt_directory + filename
        fp = open(filename, "w")
        fp.write(ipdata)
        fp.close()
        logger.logit("zyxel.out file created")

        # look for the last device in the log
        p1 = string.rfind(ipdata, "wanif")
        if p1 != -1:
            ipmatch = Addressgrep.search(ipdata, p1)
            if ipmatch != None:
                localip = ipmatch.group()
                logger.logit("IP matched: " + localip)
        else:
            p1 = string.rfind(ipdata, "enif")
            if p1 != -1:
                ipmatch = Addressgrep.search(ipdata, p1)
                if ipmatch != None:
                    localip = ipmatch.group()
                    logger.logit("IP matched: " + localip)

    elif opt_Hawking_password != "":
        # 
        # Hawking router ip detection
        # 
        ipdir = Hawking_page

        #
        # determine the router host address
        # 
        iphost = ""
        if Hawking_host != "":
            logger.logit("Hawking_host set explicitly.")
            iphost = Hawking_host
        else:
            iphost = DefaultRoute(logger, Tempfile)

        if iphost == "":
            logger.logit("No router ip detected.  Assuming 192.168.10.10")
            iphost = "192.168.10.10"
        else:
            logline = "Trying router at " + iphost
            logger.logit(logline)

        # connect to the router's admin webpage
        try:
            logger.logit("Trying HawkingTech")
            h1 = httplib.HTTP(iphost)

            h1.putrequest("GET", Hawking_page)
            h1.putheader("USER-AGENT", Useragent)
            authstring = base64.encodestring(Hawking_user + ":" + opt_Hawking_password)
            authstring = string.replace(authstring, "\012", "")
            h1.putheader("AUTHORIZATION", "Basic " + authstring)
            h1.endheaders()
            errcode, errmsg, headers = h1.getreply()
            fp = h1.getfile()
            ipdata = fp.read()
            fp.close()
        except:
            logline = "No address found on router at " + iphost
            logger.logexit(logline)
            sys.exit(-1)

        # create an output file of the response
        filename = "hawking.out"
        if opt_directory != "":
            filename = opt_directory + filename
        fp = open(filename, "w")
        fp.write(ipdata)
        fp.close()
        logger.logit("hawking.out file created")

        # look for local ip in the log
        p1 = string.find(ipdata, "WAN")
        if p1 != -1:
            ipmatch = Addressgrep.search(ipdata, p1)
            if ipmatch != None:
                localip = ipmatch.group()
                logger.logit("IP matched: " + localip)

    elif opt_Ugate_router != 0:
        # 
        # UgatePlus router ip detection
        # 
        ipdir = Ugate_page

        #
        # determine the router host address
        # 
        iphost = ""
        if Ugate_host != "":
            logger.logit("Ugate_host set explicitly.")
            iphost = Ugate_host
        else:
            iphost = DefaultRoute(logger, Tempfile)

        if iphost == "":
            logger.logit("No router ip detected.  Assuming 192.168.0.1")
            iphost = "192.168.0.1"
        else:
            logline = "Trying router at " + iphost
            logger.logit(logline)

        # connect to the router's admin webpage
        try:
            logger.logit("Trying UgatePlus")
            ipurl = "http://" + iphost + Ugate_page
            urlfp = urllib.urlopen(ipurl)
            ipdata = urlfp.read()
            urlfp.close()
        except:
            logline = "No address found on router at " + iphost
            logger.logexit(logline)
            sys.exit(-1)

        # create an output file of the response
        filename = "ugate.out"
        if opt_directory != "":
            filename = opt_directory + filename
        fp = open(filename, "w")
        fp.write(ipdata)
        fp.close()
        logger.logit("ugate.out file created")

        # look for the last Default gateway 
        p1 = string.rfind(ipdata, "I.P. Address")
        if p1 != -1:
            ipmatch = Addressgrep.search(ipdata, p1)
            if ipmatch != None:
                localip = ipmatch.group()
                logger.logit("IP matched: " + localip)

    elif opt_BelkinPreN_router != 0:
        # 
        # BelkinPreN router ip detection
        # 
        ipdir = BelkinPreN_page

        #
        # determine the router host address
        # 
        iphost = ""
        if BelkinPreN_host != "":
            logger.logit("BelkinPreN_host set explicitly.")
            iphost = BelkinPreN_host
        else:
            iphost = DefaultRoute(logger, Tempfile)

        if iphost == "":
            logger.logit("No router ip detected.  Assuming 192.168.2.1")
            iphost = "192.168.2.1"
        else:
            logline = "Trying router at " + iphost
            logger.logit(logline)

        # connect to the router's admin webpage
        try:
            logger.logit("Trying BelkinPreN")
            ipurl = "http://" + iphost + BelkinPreN_page
            urlfp = urllib.urlopen(ipurl)
            ipdata = urlfp.read()
            urlfp.close()
        except:
            logline = "No address found on router at " + iphost
            logger.logexit(logline)
            sys.exit(-1)

        # create an output file of the response
        filename = "BelkinPreN.out"
        if opt_directory != "":
            filename = opt_directory + filename
        fp = open(filename, "w")
        fp.write(ipdata)
        fp.close()
        logger.logit("BelkinPreN.out file created")

        # look for the WAN IP address 
        p1 = string.rfind(ipdata, "i17")
        if p1 != -1:
            ipmatch = Addressgrep.search(ipdata, p1)
            if ipmatch != None:
                localip = ipmatch.group()
                logger.logit("IP matched: " + localip)

    elif opt_Eicon_router != 0:
        # 
        # Eicon Diva 2430 SE ADSL Modem ip detection
        # 
        ipdir = Eicon_page

        #
        # determine the router host address
        # 
        iphost = ""
        if Eicon_host != "":
            logger.logit("Eicon_host set explicitly.")
            iphost = Eicon_host
        else:
            iphost = DefaultRoute(logger, Tempfile)

        if iphost == "":
            logger.logit("No router ip detected.  Assuming 192.168.1.1")
            iphost = "192.168.1.1"
        else:
            logline = "Trying router at " + iphost
            logger.logit(logline)

        # connect to the router's admin webpage
        try:
            logger.logit("Trying Eicon")
            ipurl = "http://" + iphost + Eicon_page
            urlfp = urllib.urlopen(ipurl)
            ipdata = urlfp.read()
            urlfp.close()
        except:
            logline = "No address found on router at " + iphost
            logger.logexit(logline)
            sys.exit(-1)

        # create an output file of the response
        filename = "eicon.out"
        if opt_directory != "":
            filename = opt_directory + filename
        fp = open(filename, "w")
        fp.write(ipdata)
        fp.close()
        logger.logit("eicon.out file created")

        # look for the last Default gateway 
        p1 = string.rfind(ipdata, "WAN IP address")
        if p1 != -1:
            ipmatch = Addressgrep.search(ipdata, p1)
            if ipmatch != None:
                localip = ipmatch.group()
                logger.logit("IP matched: " + localip)


    elif opt_Nexland_router != 0:
        # 
        # Nexland router ip detection
        # 
        ipdir = Nexland_page

        #
        # determine the router host address
        # 
        iphost = ""
        if Nexland_host != "":
            logger.logit("Nexland_host set explicitly.")
            iphost = Nexland_host
        else:
            iphost = DefaultRoute(logger, Tempfile)

        if iphost == "":
            logger.logit("No router ip detected.  Assuming 192.168.1.1")
            iphost = "192.168.1.1"
        else:
            logline = "Trying router at " + iphost
            logger.logit(logline)

        # connect to the router's admin webpage
        try:
            logger.logit("Trying Nexland")
            ipurl = "http://" + iphost + Nexland_page
            urlfp = urllib.urlopen(ipurl)
            ipdata = urlfp.read()
            urlfp.close()
        except:
            logline = "No address found on router at " + iphost
            logger.logexit(logline)
            sys.exit(-1)

        # create an output file of the response
        filename = "nexland.out"
        if opt_directory != "":
            filename = opt_directory + filename
        fp = open(filename, "w")
        fp.write(ipdata)
        fp.close()
        logger.logit("nexland.out file created")

        # look for the last Default gateway 
        p1 = string.rfind(ipdata, "Default gateway")
        if p1 != -1:
            ipmatch = Addressgrep.search(ipdata, p1)
            if ipmatch != None:
                localip = ipmatch.group()
                logger.logit("IP matched: " + localip)


    elif opt_Westel_router != 0:
        # 
        # Westel router ip detection
        # 
        ipdir = Westel_page

        #
        # determine the router host address
        # 
        iphost = ""
        if Westel_host != "":
            logger.logit("Westel_host set explicitly.")
            iphost = Westel_host
        else:
            iphost = DefaultRoute(logger, Tempfile)

        if iphost == "":
            logger.logit("No router ip detected.  Assuming 192.168.1.1")
            iphost = "192.168.1.1"
        else:
            logline = "Trying router at " + iphost
            logger.logit(logline)

        # connect to the router's admin webpage
        try:
            logger.logit("Trying Westel")
            ipurl = "http://" + iphost + Westel_page
            urlfp = urllib.urlopen(ipurl)
            ipdata = urlfp.read()
            urlfp.close()
        except:
            logline = "No address found on router at " + iphost
            logger.logexit(logline)
            sys.exit(-1)

        # create an output file of the response
        filename = "Westel.out"
        if opt_directory != "":
            filename = opt_directory + filename
        fp = open(filename, "w")
        fp.write(ipdata)
        fp.close()
        logger.logit("Westel.out file created")

        # look for the last Default gateway 
        p1 = string.rfind(ipdata, "IP&nbsp;Address")
        if p1 != -1:
            ipmatch = Addressgrep.search(ipdata, p1)
            if ipmatch != None:
                localip = ipmatch.group()
                logger.logit("IP matched: " + localip)

    elif opt_SMC_router != 0:
        # 
        # SMC barricade router ip detection
        # 
        ipdir = SMC_page

        #
        # determine the router host address
        # 
        iphost = ""
        if SMC_host != "":
            logger.logit("SMC_host set explicitly.")
            iphost = SMC_host
        else:
            iphost = DefaultRoute(logger, Tempfile)

        if iphost == "":
            logger.logit("No router ip detected.  Assuming 192.168.0.254")
            iphost = "192.168.0.254"
        else:
            logline = "Trying router at " + iphost
            logger.logit(logline)

        # connect to the router's admin webpage
        try:
            logger.logit("Trying SMC")
            ipurl = "http://" + iphost + SMC_page
            urlfp = urllib.urlopen(ipurl)
            ipdata = urlfp.read()
            urlfp.close()
        except:
            logline = "No address found on router at " + iphost
            logger.logexit(logline)
            sys.exit(-1)

        # create an output file of the response
        filename = "smc.out"
        if opt_directory != "":
            filename = opt_directory + filename
        fp = open(filename, "w")
        fp.write(ipdata)
        fp.close()
        logger.logit("smc.out file created")

        # grab first thing that looks like an IP address
        ipmatch = Addressgrep.search(ipdata)
        if ipmatch != None:
            localip = ipmatch.group()
            logger.logit("IP matched: " + localip)

    elif opt_Cisco_password != "":
        # 
        # Cisco router ip detection
        # 

        #
        # determine the router host address
        # 
        iphost = ""
        if Cisco_host != "":
            logger.logit("Cisco_host set explicitly.")
            iphost = Cisco_host
        else:
            iphost = DefaultRoute(logger, Tempfile)

        if iphost == "":
            logger.logit("No router ip detected.  Assuming 192.168.10.5")
            iphost = "192.168.10.5"
        else:
            logline = "Trying router at " + iphost
            logger.logit(logline)

        # connect to the router's admin webpage
        # first try to talk to a Cisco 667i
        try:
            logger.logit("Trying Cisco DSL 677i")
            tn = telnetlib.Telnet(iphost)
            logger.logit("Creating telnetlib obj done")
            tn.read_until("assword:")
            logger.logit("Password prompt found")
            tn.write(opt_Cisco_password + "\r\n")
            logger.logit("opt_Cisco_password sent")
            tn.write("show er\r\n")
            logger.logit("show er sent")
            ipdata = tn.read_until("Total Number", 1000)
            logger.logit("ipdata read")
            tn.write("exit\r\n")
            logger.logit("exit sent")
        except:
            logline = "No address found on router at " + iphost
            logger.logexit(logline)
            sys.exit(-1)

        # create an output file of the response
        filename = "cisco.out"
        if opt_directory != "":
            filename = opt_directory + filename
        fp = open(filename, "w")
        fp.write(ipdata)
        fp.close()
        logger.logit("cisco.out file created")

        # look for the last (rfind) negotiated IP in the log
        p1 = string.rfind(ipdata, "Negotiated IP Address")
        if p1 != -1:
            ipmatch = Addressgrep.search(ipdata, p1)
            if ipmatch != None:
                localip = ipmatch.group()
                logger.logit("IP matched: " + localip)

    elif opt_ISDNCisco_password != "":
        # 
        # ISDNCisco router ip detection
        # 

        #
        # determine the router host address
        # 
        iphost = ""
        if ISDNCisco_host != "":
            logger.logit("ISDNCisco_host set explicitly.")
            iphost = ISDNCisco_host
        else:
            iphost = DefaultRoute(logger, Tempfile)

        if iphost == "":
            logger.logit("No router ip detected.  Assuming 192.168.10.5")
            iphost = "192.168.10.5"
        else:
            logline = "Trying router at " + iphost
            logger.logit(logline)

        # connect to the router's admin webpage
        # first try to talk to a Cisco 667i
        try:
            logger.logit("Trying Cisco ISDN 700 series")
            tn = telnetlib.Telnet(iphost)
            logger.logit("Creating telnetlib obj done")
            tn.read_until("assword:")
            logger.logit("Password prompt found")
            tn.write(opt_ISDNCisco_password + "\r\n")
            logger.logit("opt_ISDNCisco_password sent")
            tn.write("show ip co\r\n")
            logger.logit("show ip co sent")
            ipdata = tn.read_until("Profile     PAT", 1000)
            logger.logit("ipdata read")
            tn.write("bye\r\n")
            logger.logit("bye sent")
        except:
            logline = "No address found on router at " + iphost
            logger.logexit(logline)
            sys.exit(-1)

        # create an output file of the response
        filename = "cisco.out"
        if opt_directory != "":
            filename = opt_directory + filename
        fp = open(filename, "w")
        fp.write(ipdata)
        fp.close()
        logger.logit("cisco.out file created")

        # look for the last negotiated IP in the log
        # you may have to change this to a user defined profile
        p1 = string.rfind(ipdata, "RemoteNet") 
        if p1 != -1:
            ipmatch = Addressgrep.search(ipdata, p1)
            if ipmatch != None:
                localip = ipmatch.group()
                logger.logit("IP matched: " + localip)

    elif opt_Netopia_password != "":
        # 
        # Netopia router ip detection
        # 
        ipdir = Netopia_page

        #
        # determine the router host address
        # 
        iphost = ""
        if Netopia_host != "":
            logger.logit("Netopia_host set explicitly.")
            iphost = Netopia_host
        else:
            iphost = DefaultRoute(logger, Tempfile)

        if iphost == "":
            logger.logit("No router ip detected.  Assuming 192.168.0.1")
            iphost = "192.168.0.1"
        else:
            logline = "Trying router at " + iphost
            logger.logit(logline)

        # connect to the router's admin webpage
        try:
            logger.logit("Trying Netopia")
            h1 = httplib.HTTP(iphost)

            h1.putrequest("GET", Netopia_page)
            h1.putheader("USER-AGENT", Useragent)
            authstring = base64.encodestring(Netopia_user + ":" + opt_Netopia_password)
            authstring = string.replace(authstring, "\012", "")
            h1.putheader("AUTHORIZATION", "Basic " + authstring)
            h1.endheaders()
            errcode, errmsg, headers = h1.getreply()
            fp = h1.getfile()
            ipdata = fp.read()
            fp.close()
        except:
            logline = "No address found on router at " + iphost
            logger.logexit(logline)
            sys.exit(-1)

        # create an output file of the response
        filename = "netopia.out"
        if opt_directory != "":
            filename = opt_directory + filename
        fp = open(filename, "w")
        fp.write(ipdata)
        fp.close()
        logger.logit("netopia.out file created")

        # look for local ip in the log
        p1 = string.find(ipdata, "local")
        if p1 != -1:
            ipmatch = Addressgrep.search(ipdata, p1)
            if ipmatch != None:
                localip = ipmatch.group()
                logger.logit("IP matched: " + localip)

    elif opt_Draytek_password != "":
        # 
        # Draytek router ip detection
        # 
        ipdir = Draytek_page

        #
        # determine the router host address
        # 
        iphost = ""
        if Draytek_host != "":
            logger.logit("Draytek_host set explicitly.")
            iphost = Draytek_host
        else:
            iphost = DefaultRoute(logger, Tempfile)

        if iphost == "":
            logger.logit("No router ip detected.  Assuming 192.168.1.1")
            iphost = "192.168.1.1"
        else:
            logline = "Trying router at " + iphost
            logger.logit(logline)

        # connect to the router's admin webpage
        try:
            logger.logit("Trying Draytek")
            h1 = httplib.HTTP(iphost)

            h1.putrequest("GET", Draytek_page)
            h1.putheader("USER-AGENT", Useragent)
            authstring = base64.encodestring(Draytek_user + ":" + opt_Draytek_password)
            authstring = string.replace(authstring, "\012", "")
            h1.putheader("AUTHORIZATION", "Basic " + authstring)
            h1.endheaders()
            errcode, errmsg, headers = h1.getreply()
            fp = h1.getfile()
            ipdata = fp.read()
            fp.close()
        except:
            logline = "No address found on router at " + iphost
            logger.logexit(logline)
            sys.exit(-1)

        # create an output file of the response
        filename = "draytek.out"
        if opt_directory != "":
            filename = opt_directory + filename
        fp = open(filename, "w")
        fp.write(ipdata)
        fp.close()
        logger.logit("draytek.out file created")

        # grab first thing that looks like an IP address
        ipmatch = Addressgrep.search(ipdata)
        if ipmatch != None:
            localip = ipmatch.group()
            logger.logit("IP matched: " + localip)

    elif opt_Netgear_password != "":
        # 
        # Netgear router ip detection
        # 
        ipdir = Netgear_page

        #
        # determine the router host address
        # 
        iphost = ""
        if Netgear_host != "":
            logger.logit("Netgear_host set explicitly.")
            iphost = Netgear_host
        else:
            iphost = DefaultRoute(logger, Tempfile)

        if iphost == "":
            logger.logit("No router ip detected.  Assuming 192.168.0.1")
            iphost = "192.168.0.1"
        else:
            logline = "Trying router at " + iphost
            logger.logit(logline)

        # connect to the router's admin webpage
        try:
            logger.logit("Trying Netgear")
            h1 = httplib.HTTP(iphost)

            h1.putrequest("GET", Netgear_page)
            h1.putheader("USER-AGENT", Useragent)
            authstring = base64.encodestring(Netgear_user + ":" + opt_Netgear_password)
            authstring = string.replace(authstring, "\012", "")
            h1.putheader("AUTHORIZATION", "Basic " + authstring)
            h1.endheaders()
            errcode, errmsg, headers = h1.getreply()
            fp = h1.getfile()
            ipdata = fp.read()
            fp.close()
        except:
            logline = "No address found on router at " + iphost
            logger.logexit(logline)
            sys.exit(-1)

        # create an output file of the response
        filename = "netgear.out"
        if opt_directory != "":
            filename = opt_directory + filename
        fp = open(filename, "w")
        fp.write(ipdata)
        fp.close()
        logger.logit("netgear.out file created")

        # look for the last WAN Port in the log
        p1 = string.rfind(ipdata, "WAN Port")
        if p1 != -1:
            ipmatch = Addressgrep.search(ipdata, p1)
            if ipmatch != None:
                localip = ipmatch.group()
                logger.logit("IP matched: " + localip)

    elif opt_FWG114P_password != "":
        #
        # Netgear reouter ip detection
        #
        ipdir = FWG114P_page

        #
        # Determine the router host address
        #
        iphost = ""
        if FWG114P_host != "":
            logger.logit("FWG114P_host set explicitly.")
            iphost = FWG114P_host
        else:
            iphost = DefaultRoute(logger, Tempfile)

        if iphost == "":
            logger.logit("No router ip detected.  Assuming 192.168.1.1")
            iphost = "192.168.1.1"
        else:
            logline = "Trying router at " + iphost
            logger.logit(logline)

        # connect to the routers admin webpage
        success = 0
        try:
            logger.logit("Trying FWG114P")
            u = FWG114POpener()
            u.set_password(opt_FWG114P_password)
            url = "http://" + iphost + ipdir
            #print url
            ipdata = u.open(url).read()
            u.close()
            success = 1
        except:
            #logline = "No address found using old method."
            #logger.logexit(logline)
            success = 0
        if success == 0:
            try:
                logger.logit("Try composing auth header manually.")
                logger.logit("iphost = " + iphost)
                logger.logit("ipdir = " + ipdir)

                h1 = httplib.HTTP(iphost)
                h1.putrequest('GET', ipdir)
                authstring = base64.encodestring(FWG114P_user + ":" + opt_FWG114P_password)
                h1.putheader("Authorization", "Basic " + authstring)
                h1.endheaders()
                errcode, errmsg, headers = h1.getreply()
                fp = h1.getfile()
                ipdata = fp.read()
                fp.close()
            except:
                logger.logit("PAGE NOT FOUND")
                logger.logit("iphost = " + iphost)
                logger.logit("ipdir = " + ipdir)
                logger.logit("authstring = " + authstring)
                logger.logexit("Exiting before parse.")
                sys.exit(-1)


        # create an output file of the response
        logger.logit("create output file")
        filename = "fwg114p.out"
        if opt_directory != "":
            filename = opt_directory + filename
        fp = open(filename, "w")
        fp.write(ipdata)
        fp.close()
        logger.logit("fwg114p.out file created")

        # look for the last WAN Port in the log
        logger.logit("parse page data")

        p1 = string.rfind(ipdata, "Internet Port")
        if p1 == -1:
            p1 = string.find(ipdata, "IP Address")
        if p1 != -1:
            ipmatch = Addressgrep.search(ipdata, p1)
            if ipmatch != None:
                localip = ipmatch.group()
                logger.logit("IP matched: " + localip)

        # now logout so others will not be blocked
        # as the router thinks you're still managing it
        try:
            logger.logit("Attempting to logout")
            u = FWG114POpener()
            u.set_password(opt_FWG114P_password)
            url = "http://" + iphost + FWG114P_exit
            ipdata = u.open(url).read()
            u.close()
            success = 1
        except:
            logger.logit("FAILED TO LOGOUT")
            success = 0
        if success == 1:
            logger.logit("Sucessfully logged out")

    elif opt_WGR614_password != "":
        # 
        # Netgear router ip detection
        # 
        ipdir = WGR614_page

        #
        # determine the router host address
        # 
        iphost = ""
        if Netgear_host != "":
            logger.logit("WGR614_host set explicitly.")
            iphost = WGR614_host
        else:
            iphost = DefaultRoute(logger, Tempfile)

        if iphost == "":
            logger.logit("No router ip detected.  Assuming 192.168.0.1")
            iphost = "192.168.0.1"
        else:
            logline = "Trying router at " + iphost
            logger.logit(logline)

        # connect to the router's admin webpage
        try:              
            logger.logit("Trying WGR614")
            u = WGR614Opener()
            u.set_password(opt_WGR614_password)
            print "BOB: " + ipdir
            url = "http://"+ iphost + ipdir
            print url
            ipdata = u.open(url).read()
            u.close()
        except:
            logline = "No address found on router at " + iphost
            logger.logexit(logline)
            sys.exit(-1)

        # create an output file of the response
        filename = "mr814.out"
        if opt_directory != "":
            filename = opt_directory + filename
        fp = open(filename, "w")
        fp.write(ipdata)
        fp.close()
        logger.logit("mr814.out file created")

        # look for the last WAN Port in the log
        p1 = string.rfind(ipdata, "Internet Port")
        if p1 != -1:
            ipmatch = Addressgrep.search(ipdata, p1)
            if ipmatch != None:
                localip = ipmatch.group()
                logger.logit("IP matched: " + localip)

    elif opt_MR814_password != "":
        # 
        # Netgear router ip detection
        #
        ipdir = MR814_page

        #
        # determine the router host address
        #
        iphost = ""
        if Netgear_host != "":
            logger.logit("MR814_host set explicitly.")
            iphost = MR814_host
        else:
            iphost = DefaultRoute(logger, Tempfile)

        if iphost == "":
            logger.logit("No router ip detected.  Assuming 192.168.0.1")
            iphost = "192.168.0.1"
        else:
            logline = "Trying router at " + iphost
            logger.logit(logline)

        # connect to the router's admin webpage
        success = 0
        try:              
            logger.logit("Trying MR814")
            u = MR814Opener()
            u.set_password(opt_MR814_password)
            url = "http://" + iphost + ipdir
            #print url
            ipdata = u.open(url).read()
            u.close()
            success = 1
        except:
            #logline = "No address found using old method."
            #logger.logexit(logline)
            success = 0

        if success == 0:
            try:
                logger.logit("Try composing auth header manually.")
                logger.logit("iphost = " + iphost)
                logger.logit("ipdir = " + ipdir)

                h1 = httplib.HTTP(iphost)
                h1.putrequest('GET', ipdir)
                authstring = base64.encodestring(MR814_user + ":" + opt_MR814_password)
                h1.putheader("Authorization", "Basic " + authstring)
                h1.endheaders()
                errcode, errmsg, headers = h1.getreply()
                fp = h1.getfile()
                ipdata = fp.read()
                fp.close()
            except:
                logger.logit("PAGE NOT FOUND")
                logger.logit("iphost = " + iphost)
                logger.logit("ipdir = " + ipdir)
                logger.logit("authstring = " + authstring)
                logger.logexit("Exiting before parse.")
                sys.exit(-1)


        # create an output file of the response
        logger.logit("create output file")
        filename = "mr814.out"
        if opt_directory != "":
            filename = opt_directory + filename
        fp = open(filename, "w")
        fp.write(ipdata)
        fp.close()
        logger.logit("mr814.out file created")

        # look for the last WAN Port in the log
        logger.logit("parse page data")

        p1 = string.rfind(ipdata, "Internet Port")
        if p1 == -1:
            p1 = string.find(ipdata, "IP Address")
        if p1 != -1:
            ipmatch = Addressgrep.search(ipdata, p1)
            if ipmatch != None:
                localip = ipmatch.group()
                logger.logit("IP matched: " + localip)

    elif opt_WGT634U_password != "":
        # 
        # Netgear WGT634U router ip detection
        # 
        ipdir = WGT634U_page

        #
        # determine the router host address
        # 
        iphost = ""
        if WGT634U_host != "":
            logger.logit("WGT634U_host set explicitly.")
            iphost = WGT634U_host
        else:
            iphost = DefaultRoute(logger, Tempfile)

        if iphost == "":
            logger.logit("No router ip detected.  Assuming 192.168.0.1")
            iphost = "192.168.0.1"
        else:
            logline = "Trying router at " + iphost
            logger.logit(logline)

        # connect to the router's admin webpage
        try:
            logger.logit("Trying WGT634U")
            h1 = httplib.HTTP(iphost)

            h1.putrequest("GET", WGT634U_page)
            h1.putheader("USER-AGENT", Useragent)
            authstring = base64.encodestring(WGT634U_user + ":" + opt_WGT634U_password)
            authstring = string.replace(authstring, "\012", "")
            h1.putheader("AUTHORIZATION", "Basic " + authstring)
            h1.endheaders()
            errcode, errmsg, headers = h1.getreply()
            fp = h1.getfile()
            ipdata = fp.read()
            fp.close()
        except:
            logline = "No address found on router at " + iphost
            logger.logexit(logline)
            sys.exit(-1)

        # create an output file of the response
        filename = "WGT634U.out"
        if opt_directory != "":
            filename = opt_directory + filename
        fp = open(filename, "w")
        fp.write(ipdata)
        fp.close()
        logger.logit("WGT634U.out file created")

        # look for "var the_wan_ip" in the javascript
        p1 = string.find(ipdata, "var the_wan_ip")
        if p1 != -1:
            ipmatch = Addressgrep.search(ipdata, p1)
            if ipmatch != None:
                localip = ipmatch.group()
                logger.logit("IP matched: " + localip)



    elif opt_Macsense_password != "":
        # 
        # MacSense router ip detection
        # 
        ipdir = Macsense_page

        #
        # determine the router host address
        # 
        iphost = ""
        if Macsense_host != "":
            logger.logit("Macsense_host set explicitly.")
            iphost = Macsense_host
        else:
            iphost = DefaultRoute(logger, Tempfile)

        if iphost == "":
            logger.logit("No router ip detected.  Assuming 192.168.1.1")
            iphost = "192.168.1.1"
        else:
            logline = "Trying MacSense XRouter Pro router at " + iphost
            logger.logit(logline)

        # connect to the router's admin webpage
        try:
            logger.logit("Trying MacSense")
            h1 = httplib.HTTP(iphost)

            authstring = base64.encodestring(Macsense_user + ":" + opt_Macsense_password)
            authstring = string.replace(authstring, "\012", "")
            ipdir = Macsense_page + ' \r\n' \
                  + 'Authorization: Basic ' \
                  + authstring + '\r\n'
            h1.putrequest('GET', ipdir)
            h1.endheaders()

            errcode, errmsg, headers = h1.getreply()
            fp = h1.getfile()
            ipdata = fp.read()
            fp.close()
        except:
            logline = "No address found on router at " + iphost
            logger.logexit(logline)
            sys.exit(-1)

        # create an output file of the linksys response
        filename = "macsense.out"
        if opt_directory != "":
            filename = opt_directory + filename
        fp = open(filename, "w")
        fp.write(ipdata)
        fp.close()
        logger.logit("macsense.out file created")

        p1 = string.find(ipdata, "Public IP")
        if p1 != -1:
            ipmatch = Addressgrep.search(ipdata, p1)
            if ipmatch != None:
                localip = ipmatch.group()
                logger.logit("IP matched: " + localip)

    elif opt_Linksys_router != 0:
        # 
        # Linksys router ip detection
        #

        #
        # determine the linksys router host address
        # 
        iphost = ""
        if Linksys_host != "":
            logger.logit("Linksys_host set explicitly.")
            iphost = Linksys_host
        else:
            iphost = DefaultRoute(logger, Tempfile)

        if iphost == "":
            logger.logit("No router ip detected.  Assuming 192.168.1.1")
            iphost = "192.168.1.1"
        else:
            logline = "Trying linksys router at " + iphost
            logger.logit(logline)

        # Try each possible Linksys router admin webpage.
        ipdata = ""
        localip = ""
        for info in Linksys_info:
            router = info['router']
            ipdir = info['page']
            markers = info['markers']
            logger.logit( "Linksys router: %s %s" % (router, ipdir) )

            try:
                h1 = httplib.HTTP(iphost)
                h1.putrequest("GET", ipdir)
                h1.putheader("USER-AGENT", Useragent)
                authstring = base64.encodestring(Linksys_user + ":" + opt_Linksys_password)
                authstring = string.replace(authstring, "\012", "")
                h1.putheader("AUTHORIZATION", "Basic " + authstring)
                h1.endheaders()
                errcode, errmsg, headers = h1.getreply()
                fp = h1.getfile()
                ipdata = fp.read()
                fp.close()

                write_response(opt_directory, "linksys.out", ipdata)
                index = 0
                for mstr in markers:
                    logger.logit( "Linksys marker: %s" % (mstr) )
                    index = string.find(ipdata, mstr, index)
                    if index == -1:
                        logger.logit( "Failed to find marker: %s" % (mstr) )
                        break

                if index != -1:
                    logger.logit( "All markers complete.  Going for IP." )
                    ipmatch = Addressgrep.search(ipdata, index)
                    if ipmatch != None:
                        localip = ipmatch.group()
                        logger.logit("IP matched: " + localip)
                        break

            except Exception, e:
                logger.logit("Unable to access page: %s" % e )


        if not localip:
            logline = "Unable to locate router IP address, exiting"
            sys.exit(-1)

    elif opt_iPAQ_router != 0:
        # Code taken from Linksys

        # 
        # iPAQ router ip detection
        # 
        ipdir = iPAQ_page

        #
        # determine the iPAQ router host address
        # 
        iphost = ""
        if iPAQ_host != "":
            logger.logit("iPAQ_host set explicitly.")
            iphost = iPAQ_host
        else:
            iphost = DefaultRoute(logger, Tempfile)

        if iphost == "":
            logger.logit("No router ip detected.  Assuming 192.168.1.1")
            iphost = "192.168.1.1"
        else:
            logline = "Trying iPAQ router at " + iphost
            logger.logit(logline)

        # connect to the router's admin webpage
        try:
            logger.logit("Trying iPAQ")
            h1 = httplib.HTTP(iphost)
            authstring = base64.encodestring(iPAQ_user + ":" + opt_iPAQ_password)
            authstring = string.replace(authstring, "\012", "")
            ipdir = iPAQ_page + ' \r\n' \
                  + 'Authorization: Basic ' \
                  + authstring + '\r\n'
            h1.putrequest('GET', ipdir)

            h1.endheaders()

            errcode, errmsg, headers = h1.getreply()
            fp = h1.getfile()
            ipdata = fp.read()
            fp.close()
        except:
            logline = "No address found on router at " + iphost
            logger.logexit(logline)
            sys.exit(-1)


        # create an output file of the iPAQ response
        filename = "ipaq.out"
        if opt_directory != "":
            filename = opt_directory + filename
        fp = open(filename, "w")
        fp.write(ipdata)
        fp.close()
        logger.logit("ipaq.out file created")

        #
        # replacing findall to support older python 1.5.1 sites
        #
        #ipmatch = Addressgrep.findall(ipdata)
        #if ipmatch != None:
        #  if len(ipmatch) > 2:
        #    localip = ipmatch[2]

        p1 = string.find(ipdata, "IP Address")
        if p1 != -1:
            ipmatch = Addressgrep.search(ipdata, p1)
            if ipmatch != None:
                localip = ipmatch.group()
                logger.logit("IP matched: " + localip)

    elif opt_DI524_password != "":
        # 
        # DI524 router ip detection
        # 
        ipdir = DI524_page

        #
        # determine the router host address
        # 
        iphost = ""
        if DI524_host != "":
            logger.logit("DI524_host set explicitly.")
            iphost = DI524_host
        else:
            iphost = DefaultRoute(logger, Tempfile)

        if iphost == "":
            logger.logit("No router ip detected.  Assuming 192.168.0.1")
            iphost = "192.168.0.1"
        else:
            logline = "Trying router at " + iphost
            logger.logit(logline)

        # connect to the router's admin webpage
        try:
            logger.logit("Trying DI524")
            h1 = httplib.HTTP(iphost)

            h1.putrequest("GET", DI524_page)
            h1.putheader("USER-AGENT", Useragent)
            authstring = base64.encodestring(DI524_user + ":" + opt_DI524_password)
            authstring = string.replace(authstring, "\012", "")
            h1.putheader("AUTHORIZATION", "Basic " + authstring)
            h1.endheaders()
            errcode, errmsg, headers = h1.getreply()
            fp = h1.getfile()
            ipdata = fp.read()
            fp.close()
        except:
            logline = "No address found on router at " + iphost
            logger.logexit(logline)
            sys.exit(-1)

        # create an output file of the response
        filename = "di524.out"
        if opt_directory != "":
            filename = opt_directory + filename
        fp = open(filename, "w")
        fp.write(ipdata)
        fp.close()
        logger.logit("di524.out file created")

        # look for the last "WAN" in the log
        p1 = string.rfind(ipdata, "WAN")
        if p1 != -1:
            ipmatch = Addressgrep.search(ipdata, p1)
            if ipmatch != None:
                localip = ipmatch.group()
                logger.logit("IP matched: " + localip)

    elif opt_DI614P_password != "":
        # 
        # DI614+ router ip detection
        # 
        ipdir = DI614P_page

        #
        # determine the router host address
        # 
        iphost = ""
        if DI614P_host != "":
            logger.logit("DI614P_host set explicitly.")
            iphost = DI614P_host
        else:
            iphost = DefaultRoute(logger, Tempfile)

        if iphost == "":
            logger.logit("No router ip detected.  Assuming 192.168.0.1")
            iphost = "192.168.0.1"
        else:
            logline = "Trying router at " + iphost
            logger.logit(logline)

        # connect to the router's admin webpage
        try:
            logger.logit("Trying DI614P")
            h1 = httplib.HTTP(iphost)

            h1.putrequest("GET", DI614P_page)
            h1.putheader("USER-AGENT", Useragent)
            authstring = base64.encodestring(DI614P_user + ":" + opt_DI614P_password)
            authstring = string.replace(authstring, "\012", "")
            h1.putheader("AUTHORIZATION", "Basic " + authstring)
            h1.endheaders()
            errcode, errmsg, headers = h1.getreply()
            fp = h1.getfile()
            ipdata = fp.read()
            fp.close()
        except:
            logline = "No address found on router at " + iphost
            logger.logexit(logline)
            sys.exit(-1)

        # create an output file of the response
        filename = "di614p.out"
        if opt_directory != "":
            filename = opt_directory + filename
        fp = open(filename, "w")
        fp.write(ipdata)
        fp.close()
        logger.logit("di614p.out file created")

        # look for the last "WAN" in the log
        p1 = string.rfind(ipdata, "WAN")
        if p1 != -1:
            ipmatch = Addressgrep.search(ipdata, p1)
            if ipmatch != None:
                localip = ipmatch.group()
                logger.logit("IP matched: " + localip)

    elif opt_DI704_password != "":
        # 
        # DI704 router ip detection
        # 
        ipdir = DI704_page

        #
        # determine the router host address
        # 
        iphost = ""
        if DI704_host != "":
            logger.logit("DI704_host set explicitly.")
            iphost = DI704_host
        else:
            iphost = DefaultRoute(logger, Tempfile)

        if iphost == "":
            logger.logit("No router ip detected.  Assuming 192.168.0.1")
            iphost = "192.168.0.1"
        else:
            logline = "Trying router at " + iphost
            logger.logit(logline)

        logger.logit("Trying DI704")
        try:
            logger.logit("Try to post to form")
            params = urllib.urlencode({'RC': '@D', 'ACCT' : "root", 'PSWD' : "71:29:26", 'URL': opt_DI704_password })
            ipurl = "http://" + iphost + "/cgi-bin/logi"
            logger.logit("urlopen " + ipurl)
            urlfp = urllib.urlopen(ipurl, params)
            logger.logit("urlfp.read")
            ipdata = urlfp.read()
            logger.logit("urlfp.close")
            urlfp.close()
            filename = "post.out"
            if opt_directory != "":
                filename = opt_directory + filename
            fp = open(filename, "w")
            fp.write(ipdata)
            fp.close()
            logger.logit("post.out file created")
        except:
            logline = "Failed to post password to login form"
            logger.logexit(logline)
            sys.exit(-1)

        try:
            logger.logit("Now try to access status.htm now")
            ipurl = "http://" + iphost + "/status.htm"
            urlfp = urllib.urlopen(ipurl)
            ipdata = urlfp.read()
            urlfp.close()

            filename = "di704.out"
            if opt_directory != "":
                filename = opt_directory + filename
            fp = open(filename, "w")
            fp.write(ipdata)
            fp.close()
            logger.logit("di704.out file created")
        except:
            logline = "Failed accessing status page "
            logger.logexit(logline)
            sys.exit(-1)

        # look for the first WAN Port in the log
        p1 = string.find(ipdata, "IP Address")

        if p1 != -1:
            ipmatch = Addressgrep.search(ipdata, p1)
            if ipmatch != None:
                localip = ipmatch.group()
                logger.logit("IP matched: " + localip)

    elif opt_DI713P_password != "":
        # 
        # DI713P router ip detection
        # 
        ipdir = DI713P_page

        #
        # determine the router host address
        # 
        iphost = ""
        if DI713P_host != "":
            logger.logit("DI713P_host set explicitly.")
            iphost = DI713P_host
        else:
            iphost = DefaultRoute(logger, Tempfile)

        if iphost == "":
            logger.logit("No router ip detected.  Assuming 192.168.0.1")
            iphost = "192.168.0.1"
        else:
            logline = "Trying router at " + iphost
            logger.logit(logline)

        logger.logit("Trying DI713P")
        try:
            logger.logit("Try to post to form")
            params = urllib.urlencode({'RC': '@D', 'ACCT' : "root", 'PSWD' : "46:34:40 (S=00:00:00,P=0)", 'URL': opt_DI713P_password, 'KEY':"3C95.3C76.3C95/3100+ADA4@Toronto 194a2", 'htm':"2.57 build 3a" })
            ipurl = "http://" + iphost + "/cgi-bin/logi"
            logger.logit("urlopen " + ipurl)
            urlfp = urllib.urlopen(ipurl, params)
            logger.logit("urlfp.read")
            ipdata = urlfp.read()
            logger.logit("urlfp.close")
            urlfp.close()
            filename = "post.out"
            if opt_directory != "":
                filename = opt_directory + filename
            fp = open(filename, "w")
            fp.write(ipdata)
            fp.close()
            logger.logit("post.out file created")
        except:
            logline = "Failed to post password to login form"
            logger.logexit(logline)
            sys.exit(-1)

        try:
            logger.logit("Now try to access status.htm now")
            ipurl = "http://" + iphost + "/status.htm"
            urlfp = urllib.urlopen(ipurl)
            ipdata = urlfp.read()
            urlfp.close()

            filename = "di713p.out"
            if opt_directory != "":
                filename = opt_directory + filename
            fp = open(filename, "w")
            fp.write(ipdata)
            fp.close()
            logger.logit("di713p.out file created")
        except:
            logline = "Failed accessing status page "
            logger.logexit(logline)
            sys.exit(-1)

        # look for the first WAN Port in the log
        p1 = string.find(ipdata, "IP Address")

        if p1 != -1:
            ipmatch = Addressgrep.search(ipdata, p1)
            if ipmatch != None:
                localip = ipmatch.group()
                logger.logit("IP matched: " + localip)

    elif opt_DI701_password != "":

        #
        # determine the router host address
        #
        iphost = ""
        if DI701_host != "":
            logger.logit("DI701_host set explicitly.")
            iphost = DI701_host
        else:
            iphost = DefaultRoute(logger, Tempfile)

        if iphost == "":
            logger.logit("No router ip detected.  Assuming 192.168.1.1")
            iphost = "192.168.1.1"
        else:
            logline = "Trying router at " + iphost
            logger.logit(logline)

        # connect to the router's admin webpage
        try:
            logger.logit("Trying DLink DI701")
            tn = telnetlib.Telnet(iphost,333)
            logger.logit("Creating telnetlib obj done")
            tn.read_until("assword : ")
            logger.logit("Password prompt found")
            tn.write(opt_DI701_password + "\r")
            logger.logit("opt_DI701_password sent")
            tn.read_until("command>")
            tn.write("show\r")
            logger.logit("show command sent")
            tn.read_until("address of global port : [", 2000)
            ip2 = tn.read_until("]", 2000)
            logger.logit("ip read")
            #tn.write("exit\r\n")
            #logger.logit("exit sent")
            ipdata = ip2[:-1]
        except:
            logline = "No address found on router at " + iphost
            logger.logexit(logline)
            sys.exit(-1)

        # create an output file of the response
        filename = "di701.out"
        if opt_directory != "":
            filename = opt_directory + filename
        open(filename, "w").write(ipdata)
        logger.logit("di701.out file created")

        localip = ipdata
        logger.logit("IP matched: " + localip)

    elif opt_Watchguard_password != "":
        # 
        # Watchguard firewall/router ip detection
        # 
        ipdir = Watchguard_page

        #
        # determine the watchguard soho router host address
        # 
        iphost = ""
        if Watchguard_host != "":
            logger.logit("Watchguard_host set explicitly.")
            iphost = Watchguard_host
        else:
            iphost = DefaultRoute(logger, Tempfile)

        if iphost == "":
            logger.logit("No router ip detected.  Assuming 192.168.111.1")
            iphost = "192.168.111.1"
        else:
            logline = "Trying Watchguard SOHO firewall at " + iphost
            logger.logit(logline)

        # connect to the router's admin webpage
        try:
            logger.logit("Trying Watchguard")
            h1 = httplib.HTTP(iphost)

            authstring = base64.encodestring(Watchguard_user + ":" + opt_Watchguard_password)
            authstring = string.replace(authstring, "\012", "")
            ipdir = Watchguard_page + ' \r\n' \
                  + 'Authorization: Basic ' \
                  + authstring + '\r\n'
            h1.putrequest('GET', ipdir)
            h1.putheader("AUTHORIZATION", "Basic " + authstring)

            h1.endheaders()

            errcode, errmsg, headers = h1.getreply()
            fp = h1.getfile()
            ipdata = fp.read()
            fp.close()
        except:
            logline = "No address found on router at " + iphost
            logger.logexit(logline)
            sys.exit(-1)

        ipmatch = Addressgrep.search(ipdata)
        if ipmatch != None:
            localip = ipmatch.group()
            logger.logit("IP matched: " + localip)
        else:
            logger.logit("Trying Watchguard new firmware")
            h1 = httplib.HTTP(iphost)

            authstring = base64.encodestring(Watchguard_user + ":" + opt_Watchguard_password)
            authstring = string.replace(authstring, "\012", "")
            ipdir = Watchguard_page2 + ' \r\n' \
                  + 'Authorization: Basic ' \
                  + authstring + '\r\n'
            h1.putrequest('GET', ipdir)
            h1.putheader("AUTHORIZATION", "Basic " + authstring)
            h1.endheaders()

            errcode, errmsg, headers = h1.getreply()
            fp = h1.getfile()
            ipdata = fp.read()
            fp.close()

        # create an output file of the watchguard response
        filename = "watchguard.out"
        if opt_directory != "":
            filename = opt_directory + filename
        fp = open(filename, "w")
        fp.write(ipdata)
        fp.close()
        logger.logit("watchguard.out file created")

        ipmatch = Addressgrep.search(ipdata)
        if ipmatch != None:
            localip = ipmatch.group()
            logger.logit("IP matched: " + localip)

    elif opt_wan_router != "":
        logger.logit("WAN IP simple router")
        ipurl = ""

        # strip off the http part, if any
        if opt_wan_router[:7] == "HTTP://" or opt_wan_router[:7] == "http://":
            ipurl = opt_wan_router[7:]
        else:
            ipurl = opt_wan_router

        # stick it back on for urllib usage
        ipurl = "http://" + ipurl

        # grab the data
        try:
            logger.logit("Trying URL " + ipurl)
            urlfp = urllib.urlopen(ipurl)
            ipdata = urlfp.read()
            urlfp.close()
        except:
            logline = "Unable to open url " + ipurl
            logger.logexit(logline)
            sys.exit(-1)


        # create an output file of the ip detection response
        filename = "webip.out"
        if opt_directory != "":
            filename = opt_directory + filename
        fp = open(filename, "w")
        fp.write(ipdata)
        fp.close()
        logger.logit("webip.out file created")

        # grab first thing that looks like an IP address
        p1 = string.find(ipdata, "Wan IP")
        ipmatch = Addressgrep.search(ipdata[p1:])
        if ipmatch != None:
            localip = ipmatch.group()
            logger.logit("router IP detected = " + localip)

    elif opt_router != "":
        logger.logit("web based ip detection for localip")
        ipurl = ""

        # strip off the http part, if any
        if opt_router[:7] == "HTTP://" or opt_router[:7] == "http://":
            ipurl = opt_router[7:]
        else:
            ipurl = opt_router

        # stick it back on for urllib usage
        ipurl = "http://" + ipurl

        # grab the data
        try:
            logger.logit("Trying URL " + ipurl)
            urlfp = urllib.urlopen(ipurl)
            ipdata = urlfp.read()
            urlfp.close()
        except:
            logline = "Unable to open url " + ipurl
            logger.logexit(logline)
            sys.exit(-1)


        # create an output file of the ip detection response
        filename = "webip.out"
        if opt_directory != "":
            filename = opt_directory + filename
        fp = open(filename, "w")
        fp.write(ipdata)
        fp.close()
        logger.logit("webip.out file created")

        # grab first thing that looks like an IP address
        ipmatch = Addressgrep.search(ipdata)
        if ipmatch != None:
            localip = ipmatch.group()
            logger.logit("webip detected = " + localip)

    else:
        logger.logit("Interface ip detection on sys.platform = " + sys.platform)
        if sys.platform == "win32":
            logger.logit("win32 interface ip detection for localip")
            localip = ""
            getip = Win32ip 
            os.system (getip + " > " + Tempfile)
            fp = open(Tempfile, "r")
            ipdata = fp.read()
            fp.close()
            # grab the first dotted quad after the interface
            p1 = string.find(ipdata, opt_interface)
            if p1 != -1:
                ipmatch = Addressgrep.search(ipdata, p1)
                if ipmatch != None:
                    localip = ipmatch.group()
                    logger.logit("IP matched: " + localip)

        elif string.find(sys.platform, "sunos") != -1:
            logger.logit("Sunos interface ip detection for localip (untested)")
            getip = Sunip + " " + opt_interface
            os.system (getip + " > " + Tempfile)
            fp = open(Tempfile, "r")
            ipdata = fp.read()
            fp.close()
            # grab the first dotted quad after the interface
            p1 = string.find(ipdata, opt_interface)
            if p1 != -1:
                ipmatch = Addressgrep.search(ipdata, p1)
                if ipmatch != None:
                    localip = ipmatch.group()
                    logger.logit("IP matched: " + localip)

        elif string.find(sys.platform, "linux") != -1:
            logger.logit("linux interface ip detection for localip")
            getip = Linuxip + " " + opt_interface
            os.system (getip + " > " + Tempfile)
            fp = open(Tempfile, "r")
            ipdata = fp.read()
            fp.close()
            # grab the first dotted quad after the interface
            p1 = string.find(ipdata, opt_interface)
            if p1 != -1:
                ipmatch = Addressgrep.search(ipdata, p1)
                if ipmatch != None:
                    localip = ipmatch.group()
                    logger.logit("IP matched: " + localip)

        elif string.find(sys.platform, "Darwin") != -1:
            logger.logit("Darwin interface ip detection for localip")
            getip = Macip + " " + opt_interface 
            os.system (getip + " > " + Tempfile)
            fp = open(Tempfile, "r")
            ipdata = fp.read()
            fp.close()
            # grab the first dotted quad after the LAST inet (to avoid dead routes)
            p1 = string.rfind(ipdata, "inet ")
            if p1 != -1:
                ipmatch = Addressgrep.search(ipdata, p1)
                if ipmatch != None:
                    localip = ipmatch.group()
                    logger.logit("IP matched: " + localip)

        elif string.find(sys.platform, "bsd") != -1:
            logger.logit("*BSD* interface ip detection for localip")
            getip = BSDip + " " + opt_interface 
            os.system (getip + " > " + Tempfile)
            fp = open(Tempfile, "r")
            ipdata = fp.read()
            fp.close()
            # grab the first dotted quad after the LAST inet (to avoid dead routes)
            p1 = string.rfind(ipdata, "inet ")
            if p1 != -1:
                ipmatch = Addressgrep.search(ipdata, p1)
                if ipmatch != None:
                    localip = ipmatch.group()
                    logger.logit("IP matched: " + localip)

        elif string.find(sys.platform, "os2") != -1:
            logger.logit("OS2 interface ip detection for localip")
            getip = Os2ip + " " + opt_interface 
            os.system (getip + " > " + Tempfile)
            fp = open(Tempfile, "r")
            ipdata = fp.read()
            fp.close()
            # grab the first dotted quad after the LAST inet (to avoid dead routes)
            p1 = string.rfind(ipdata, "inet ")
            if p1 != -1:
                ipmatch = Addressgrep.search(ipdata, p1)
                if ipmatch != None:
                    localip = ipmatch.group()
                    logger.logit("IP matched: " + localip)


        else:
            logger.logit("Default interface ip detection for localip (untested)")
            getip = Otherip + " " + opt_interface 
            os.system (getip + " > " + Tempfile)
            fp = open(Tempfile, "r")
            ipdata = fp.read()
            fp.close()
            # grab the first dotted quad after the LAST inet (to avoid dead routes)
            p1 = string.rfind(ipdata, "inet ")
            if p1 != -1:
                ipmatch = Addressgrep.search(ipdata, p1)
                if ipmatch != None:
                    localip = ipmatch.group()
                    logger.logit("IP matched: " + localip)

        # check if we have a localip from all the above elifs
        if localip == "":
            logline = "No address found on interface " + opt_interface + " use -i"
            logger.logexit(logline)
            sys.exit(-1)


    # end of all determining localip cases
    # check if the router elif's found no address
    if localip == "":
        logline = "No address found on router." 
        logger.logexit(logline)
        sys.exit(-1)

    # check if detected ip is not valid
    if localip == "0.0.0.0":
        logline = "The router has external IP 0.0.0.0 assigned. " 
        logger.logexit(logline)
        sys.exit(-1)

    if localip == "":
        logline = "Unable to find external IP (localip is empty). " 
        logger.logexit(logline)
        sys.exit(-1)


    #
    # check the IP to make sure it is sensible
    #
    p1 = string.find(localip, ".")
    p2 = string.find(localip, ".", p1+1)
    p3 = string.find(localip, ".", p2+1)
    p4 = string.find(localip, ".", p3+1)
    if p1 == -1 or p2 == -1 or p3 == -1 or p4 != -1:
        logline = "Invalid local address " + localip
        logger.logexit(logline)
        sys.exit(-1)

    try:
        ip1 = string.atoi(localip[0:p1])
        ip2 = string.atoi(localip[p1+1:p2])
        ip3 = string.atoi(localip[p2+1:p3])
        ip4 = string.atoi(localip[p3+1:])
    except:
        ip1 = 0
        ip2 = 0
        ip3 = 0
        ip4 = 0
        # 0-255 in first three allowed, 0 to 255 in last 
    if ip1 < 0 or ip1 > 255 or ip2 < 0 or ip2 > 255 or ip3 < 0 or ip3 > 255 or ip4 < 0 or ip4 > 255:
        logline = "Invalid local address " + localip
        logger.logexit(logline)
        sys.exit(-1)

    #
    # read the data from file of last update, if any
    #
    fileip = ""
    filehosts = []
    fileage = 0
    try:
        fp = open (Datfile, "r")
        fileip = fp.readline()
        if fileip[-1] == "\n": 
            fileip = fileip[:-1]
        while 1:
            fileline = fp.readline()
            if not fileline:
                break
            filehosts.append(fileline[:-1])
        fp.close()

        #
        # get the age of the file
        #
        currtime = time.time()
        statinfo = os.stat(Datfile)
        fileage = (currtime - statinfo[8]) / (60*60*24)

    except:
        # do not create the file automatically cause people could get
        # into loops and use up a lot of bandwidth doing dns lookup
        logger.logit("Okay, no zoneclient.dat file found.")


    #
    # check filehosts list versus hostnames list
    #
    mismatch = 0
    for h in filehosts:
        if h not in hostnames:
            mismatch = 1
    for h in hostnames:
        if h not in filehosts:
            mismatch = 1
    if mismatch == 0:
        logger.logit("Good, filehosts and hostnames are the same.")
    else:
        logger.logit("Warning: The hostnames listed do not match the dat file.")



    #
    # determine whether and which hosts need updating
    #
    updatehosts = []

    # if opt_force is set then update all hosts
    # or offline mode selected
    if opt_force == 1 or opt_offline:
        logger.logit("Updates forced by -f option.")
        for host in hostnames:
            updatehosts.append(host)

    # else if file age is older than update all hosts
    elif fileage > Touchage:
        logger.logit("Updates required by stale dat file.")
        for host in hostnames:
            updatehosts.append(host)

    # else check the address used in last update
    elif localip != fileip:
        logger.logit("Updates required by dat address mismatch.")
        for host in hostnames:
            updatehosts.append(host)

    # This case is probably deprecated but will leave it in
    # case I missed something.  When reading the dat file,
    # I'm going to now only proceed if hostnames == filehosts.
    # Otherwise, a message will be printed out and an option
    # to create a dat file from dns lookups will be recommended.

    else:
        logger.logit("Checking hosts in file vs command line.")
        updateflag = 0
        for host in hostnames:
            if host not in filehosts:
                updateflag = 1

        # If anyone of the hosts on the command line needs updating,
        # put them all in the updatehosts list so they will get the
        # same last updated timestamp at dyndns.  This way they all 
        # won't need to be touched again for Touchage days, instead 
        # of having multiple touches for different last updated dates.
        if updateflag == 1:
            for host in hostnames:
                updatehosts.append(host)

    if updatehosts == []:
        # Quietly log this message then exit too.
        logger.logit("The database matches local address.  No hosts update.")
        sys.exit(0)





    #
    # build the query strings
    #
    updateprefix = Updatepage + "?"

    hostlist = "host="
    for host in updatehosts:
        hostlist = hostlist + host + ","
        logger.logit(host + " needs updating")
    if hostlist[-1:] == ",":
        hostlist = hostlist[:-1]

    if opt_guess == 1:
        logger.logit("Letting zoneedit guess the IP.")
        updatesuffix = ""
        localip = ""
    else:
        updatesuffix = "&dnsto=" + localip 

    if opt_mxtype == 1:
        updatesuffix = updatesuffix + "&type=MX"

    if opt_node != "":
        updatesuffix = updatesuffix + "&dnsfrom=" + opt_node

    logger.logit("Prefix = " + updateprefix)
    logger.logit("Hosts  = " + hostlist)
    logger.logit("Suffix = " + updatesuffix)

    if opt_testrun == 1:
        logger.logit("test run exits here")
        sys.exit()

    #
    # update those hosts 
    #
    if not opt_no_https:
        logline = "trying to open HTTPS connection"
        logger.logit(logline)
        try:
            if not opt_proxy:
                h2 = httplib.HTTPS(Updatehost)
                logline = "HTTPS connection successful"
                logger.logit(logline)
            else:
                h2 = httplib.HTTPS(Updatehost, 8245)
                logline = "HTTPS connection successful"
                logger.logit(logline)
        except:
            logline = "trying to open normal HTTP connection"
            logger.logit(logline)
            if not opt_proxy:
                h2 = httplib.HTTP(Updatehost)
                logline = "normal HTTP connection successful"
                logger.logit(logline)
            else:
                h2 = httplib.HTTP(Updatehost, 8245)
                logline = "normal HTTP connection successful"
                logger.logit(logline)
    else:
        logline = "trying to open normal HTTP connection"
        logger.logit(logline)
        if not opt_proxy:
            h2 = httplib.HTTP(Updatehost)
            logline = "normal HTTP connection successful"
            logger.logit(logline)
        else:
            h2 = httplib.HTTP(Updatehost, 8245)
            logline = "normal HTTP connection successful"
            logger.logit(logline)


    h2 = httplib.HTTP(Updatehost)
    h2.putrequest("GET", updateprefix + hostlist + updatesuffix)
    h2.putheader("HOST", Updatehost)
    h2.putheader("USER-AGENT", Useragent)
    authstring = base64.encodestring(opt_username + ":" + opt_password)
    authstring = string.replace(authstring, "\012", "")
    h2.putheader("AUTHORIZATION", "Basic " + authstring)
    h2.endheaders()
    errcode, errmsg, headers = h2.getreply()

    # log the result
    logline = "http code = " + `errcode`
    logger.logit(logline)
    logline = "http msg  = " + errmsg
    logger.logit(logline)

    # try to get the html text
    try:
        fp = h2.getfile()
        httpdata = fp.read()
        fp.close()
    except:
        httpdata = "No output from http request."

    # create the output file
    fp = open(Htmlfile, "w")
    fp.write(httpdata)
    fp.close()
    logger.logit("zoneclient.html file created")

    #
    # check the result for fatal errors
    #
    res200 = string.find(httpdata, "200")
    res201 = string.find(httpdata, "201")
    if (res200 != -1) or (res201 != -1):
        if opt_quiet == 0:
            logger.logexit("Success")
            logger.logexit(httpdata)

        #
        # write the update data to file
        #
        if localip != "":
            fp = open (Datfile, 'w')
            fp.write(localip + "\n")

            # hostnames == updatehosts in the current version 
            # but that may change in future versions of the client
            for host in hostnames:
                fp.write(host + "\n")
            fp.close()
            logger.logit("dat file created.")

            if opt_execute != "":
                os.system (opt_execute)

        else:
            if os.path.isfile(Datfile):
                os.unlink(Datfile)
                logger.logit("dat file removed.")

    else:
        logger.logexit("ERROR RETURNED")

        #
        # save the error to an zoneclient.err file
        #
        fp = open (Errfile, 'w')
        fp.write(httpdata + "\n")
        fp.close()
        logger.logit("zoneclient.err file created.")
        sys.exit(-1)



if __name__=="__main__":

    _main(sys.argv)


