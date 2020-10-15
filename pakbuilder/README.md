vcopspakbuilderforwindows
=========================

VCOPS PAK Builder for Windows automates the build process for VmWare VCOPS PAK files.

VCOPS PAK Builder for Windows is protected by (c). Copyright 2014, Vyper Logix Corp., See the LICENSE file for Licensing Details.

pakbuilder Version 1.5.0.0

Usage: pakbuilder ip-address [options]

Options:

DEBUG: Logging to "j:\@Vyper Logix Corp\@Projects\python-projects\pakbuilder\PAKbuilder1.5.0.0_1397666370.12.log".
2014-04-16 11:39:30,118 - PAKbuilder1.5.0.0 - INFO - PAKbuilder v1.5.0.0
INFO:PAKbuilder1.5.0.0:PAKbuilder v1.5.0.0
Usage: pakbuilder.py ip-address [options]

Options:
  -h, --help            show this help message and exit
  -p PORT, --port=PORT  linux host ssh port, typically 22
  -u USERNAME, --username=USERNAME
                        Linux username, typically root
  -w PASSWORD, --password=PASSWORD
                        Linux password, typically Compaq123
  -v, --verbose         verbose
  -s SOURCE, --source=SOURCE
                        Source of project, typically the fully qualified
                        folder path of project root.
  -d DEST, --dest=DEST  Destination of project, typically the fully qualified
                        directory path of project root on Linux box that
                        matches the AdapterPakFileBuilder/adapter-installer-
                        conf/adapter-config.properties::ADAPTER_LOCATION.
  -c COPYPAKTOFOLDER, --copypaktofolder=COPYPAKTOFOLDER
                        Copy the PAK file to a different directory other than
                        the parent of the project source; this allows the PAK
                        file to be copied directly to your local disk in case
                        you run this command from your development VM.
  -a ADAPTERPAKFILEBUILDER, --adapterpakfilebuilder=ADAPTERPAKFILEBUILDER
                        The fully qualified directory path on Linux box for
                        the parent of the AdapterPakFileBuilder directory.
  -n ADAPTERNAME, --adaptername=ADAPTERNAME
                        The Adapter Name for the AdapterPakFileBuilder
                        /adapter-installer-conf/adapter-config.properties
                        file.
  -b BUILDNUMBER, --buildnumber=BUILDNUMBER
                        The Adapter Build Number for the AdapterPakFileBuilder
                        /adapter-installer-conf/adapter-config.properties
                        file.
  -i, --incrementbuildnumber
                        Auto-increments the build number for each build; you
                        must specify the build number but this option
                        automates the build number and the version number in
                        the describe.xml for you otherwise you may wish to
                        change the build number for each build manually.
  -o, --override        Override handling the key value of the AdapterKind tag
                        so it does not have to match the adaptername option.
  -r, --remotedebugger  Enables remote debugging for the Analytics VM given
                        the ipaddress, port, username, password and
                        destination with override; override will be taken for
                        remote debugging flags like
                        "server=y,suspend=n,address=8004" options.
  -f FLAGS, --flags=FLAGS
                        Remote debugging flags.

After you issue the run.cmd and it completes without warnings or errors your PAK file will be in the SOURCE parent folder of your local computer.

For instance, let's assume the following command appears in your run.cmd file:

"pakbuilder" 16.83.121.151 -v -p 22 -u root -w Compaq123 -s "c:\workspaces\vcops\Helloworld" -d "/root" -a "/root" -n hpOneViewAdapter3 -b 115 -i

This tells pakbuilder your Linux IP address is 16.83.121.151 (this is not a real IP address as it appears in this document) and the username is root
with password of Compaq123 with your Eclipse SOURCE of "c:\workspaces\vcops\Helloworld" and DEST on Linux box of "/root" and ADAPTERPAKFILEBUILDER
in "/root" and ADAPTERNAME of hpOneViewAdapter3 with BUILDNUMBER of 115.

The SOURCE must be a valid Eclipse project.

The JAR file must be in SOURCE\build\deploy\ADAPTERNAME.jar.

The PAK file will appear in SOURCE\.. which is SOURCE without the \Helloworld using this example.

Change Log:

Version 1.5.0.0 -- The -x option is no longer required for this release however it may be used by a future release.  
                   Initial remote debugger support has been rolled into this release in the form of handling the wrapper.conf file setup.

Version 1.4.0.0 -- Use the -x option to use the latest optimizations.

Version 1.2.0.0 -- Optimized and almost deploys the ADAPTERPAKFILEBUILDER.

https://github.com/raychorn/vcopspakbuilderforwindows
