# Python MSI Generator
# (C) 2003 Martin v. Loewis
import msilib, schema, sequence, os, sets, glob
from msilib import Feature, CAB, Directory, Dialog, Binary, add_data
import uisample
from win32com.client import constants

msilib.Win64 = 0
current_version = "2.4.0"
testpackage=0

srcdir = r'e:\pyinst\python'

major, minor = current_version.split(".")[:2]
short_version = major+"."+minor

# This should never change
upgrade_code='{92A24481-3ECB-40FC-8836-04B7966EC0D5}'

# This should be extended for each Python release
product_codes = {
    '2.3.2'  : "{3ad0c9ed-7e5e-478c-b539-5cc3a2f8772a}",
    '2.3.3'  : "{aab605af-d181-4b68-bcb0-6beb32f32844}",
    '2.4.0': "{93792a5a-5bb0-43b1-904f-ba10c4f08ec8}",
}

extensions = [
    'bz2.pyd',
    'pyexpat.pyd',
    'select.pyd',
    'unicodedata.pyd',
    'winsound.pyd',
    'zlib.pyd',
    '_bsddb.pyd',
    '_socket.pyd',
    '_ssl.pyd',
    '_testcapi.pyd',
    '_tkinter.pyd',
]

if major+minor <= "23":
    extensions.extend([
    '_csv.pyd',
    '_sre.pyd',
    '_symtable.pyd',
    '_winreg.pyd',
    'datetime.pyd'
    'mmap.pyd',
    'parser.pyd',    
    ])
    

if testpackage:
    ext = 'px'
    testprefix = 'x'
else:
    ext = 'py'
    testprefix = ''

msilib.reset()    

def build_database():
    db = msilib.init_database("python%s.msi" % current_version,schema,
                          ProductName="Python "+current_version,
                  ProductCode=product_codes[current_version],
                  ProductVersion=current_version,
                  Manufacturer=u"Martin v. L\xf6wis")
    msilib.add_tables(db, sequence)
    add_data(db, "Property", [("UpgradeCode", upgrade_code),
                              ("ALLUSERS", "2")])
    db.Commit()
    return db

class PyDialog(Dialog):
    def __init__(self, *args, **kw):
        Dialog.__init__(self, *args)
        ruler = self.h - 36
        bmwidth = 152*ruler/328
        if kw.get("bitmap", True):
            self.bitmap("Bitmap", 0, 0, bmwidth, ruler, "PythonWin")
        self.line("BottomLine", 0, ruler, self.w, 0)

    def title(self, title):
        self.text("Title", 135, 20, 220, 60, 196611,
                  r"{\VerdanaBold13}%s" % title)

    def back(self, title, next, name = "Back", active = 1):
        if active:
            flags = 3
        else:
            flags = 1
        return self.pushbutton(name, 180, self.h-27 , 56, 17, flags, title, next)

    def cancel(self, title, next, name = "Cancel", active = 1):
        if active:
            flags = 3
        else:
            flags = 1
        return self.pushbutton(name, 304, self.h-27, 56, 17, flags, title, next)

    def next(self, title, next, name = "Next", active = 1):
        if active:
            flags = 3
        else:
            flags = 1
        return self.pushbutton(name, 236, self.h-27, 56, 17, flags, title, next)

    def xbutton(self, name, title, next, xpos):
        return self.pushbutton(name, int(self.w*xpos - 28), self.h-27, 56, 17, 3, title, next)

def add_ui(db):
    x = y = 50
    w = 370
    h = 300
    title = "[ProductName] Setup"

    # Dialog styles
    modal = 3      # visible | modal
    modeless = 1   # visible
    track_disk_space = 32

    add_data(db, 'ActionText', uisample.ActionText)
    add_data(db, 'UIText', uisample.UIText)

    # Bitmaps
    add_data(db, "Binary",
             [("PythonWin", msilib.Binary(srcdir+r"\PCbuild\installer.bmp")), # 152x328 pixels
              ("Up",msilib.Binary("Up.bin")),
              ("New",msilib.Binary("New.bin")),
              ("InfoIcon",msilib.Binary("info.bin")),
              ("ExclamationIcon",msilib.Binary("exclamic.bin")),
             ])


    # UI customization properties
    add_data(db, "Property",
             [("DefaultUIFont", "DlgFont8"),
              ("ErrorDialog", "ErrorDlg"),
              ("Progress1", "Install"),   # modified in maintenance type dlg
              ("Progress2", "installs"),
              ("MaintenanceForm_Action", "Repair")])

    # Fonts
    add_data(db, "TextStyle",
             [("DlgFont8", "Tahoma", 9, None, 0),
              ("DlgFontBold8", "Tahoma", 8, None, 1), #bold
              ("VerdanaBold13", "Verdana", 13, None, 1),
             ])

    # Custom actions
    add_data(db, "CustomAction", [
        # msidbCustomActionTypeFirstSequence + msidbCustomActionTypeTextData + msidbCustomActionTypeProperty
        ("InitialTargetDir", 307, "TARGETDIR",
         "[WindowsVolume]Python%s%s" % (major, minor))
        ])

    # UI Sequences
    add_data(db, "InstallUISequence",
             [("PrepareDlg", None, 140),
              ("InitialTargetDir", 'TARGETDIR=""', 750),
              ("SelectDirectoryDlg", "Not Installed", 1230),
              # XXX notyet
              #("ResumeDlg", "Installed AND (RESUME OR Preselected)", 1240),
              ("MaintenanceTypeDlg", "Installed AND NOT RESUME AND NOT Preselected", 1250),
              ("ProgressDlg", None, 1280)])
    add_data(db, "AdminUISequence",
             [("InitialTargetDir", 'TARGETDIR=""', 750)])

    # Standard dialogs: FatalError, UserExit, ExitDialog
    fatal=PyDialog(db, "FatalError", x, y, w, h, modal, title,
                 "Finish", "Finish", "Finish")
    fatal.title("[ProductName] Installer ended prematurely")
    fatal.back("< Back", "Finish", active = 0)
    fatal.cancel("Cancel", "Back", active = 0)
    fatal.text("Description1", 135, 70, 220, 60, 196611,
               "[ProductName] setup ended prematurely because of an error.  Your system has not been modified.  To install this program at a later time, please run the installation again.")
    fatal.text("Description2", 135, 135, 220, 20, 196611,
               "Click the Finish button to exit the Installer.")
    c=fatal.next("Finish", "Cancel", name="Finish")
    c.event("EndDialog", "Exit")
    
    user_exit=PyDialog(db, "UserExit", x, y, w, h, modal, title,
                 "Finish", "Finish", "Finish")
    user_exit.title("[ProductName] Installer was interrupted")
    user_exit.back("< Back", "Finish", active = 0)
    user_exit.cancel("Cancel", "Back", active = 0)
    user_exit.text("Description1", 135, 70, 220, 40, 196611,
               "[ProductName] setup was interrupted.  Your system has not been modified.  "
               "To install this program at a later time, please run the installation again.")
    user_exit.text("Description2", 135, 115, 220, 20, 196611,
               "Click the Finish button to exit the Installer.")
    c = user_exit.next("Finish", "Cancel", name="Finish")
    c.event("EndDialog", "Exit")
    
    exit_dialog = PyDialog(db, "ExitDialog", x, y, w, h, modal, title,
                         "Finish", "Finish", "Finish")
    exit_dialog.title("Completing the [ProductName] Installer")
    exit_dialog.back("< Back", "Finish", active = 0)
    exit_dialog.cancel("Cancel", "Back", active = 0)
    exit_dialog.text("Description", 135, 115, 220, 20, 196611,
               "Click the Finish button to exit the Installer.")
    c = exit_dialog.next("Finish", "Cancel", name="Finish")
    c.event("EndDialog", "Return")

    # Required dialog: FilesInUse, ErrorDlg
    inuse = PyDialog(db, "FilesInUse", x, y, w, h, 19, title,
                     "Retry", "Retry", "Retry", bitmap=False)
    inuse.text("Title", 15, 6, 200, 15, 196611,
               r"{\DlgFontBold8}Files in Use")
    inuse.text("Description", 20, 23, 280, 20, 196611,
               "Some files that need to be updated are currently in use.")
    inuse.text("Text", 20, 55, 330, 50, 3,
               "The following applications are using files that need to be updated by this setup. Close these applications and then click Retry to continue the installation or Cancel to exit it.")
    inuse.control("List", "ListBox", 20, 107, 330, 130, 7, "FileInUseProcess",
                  None, None, None)
    c=inuse.back("Exit", "Ignore", name="Exit")
    c.event("EndDialog", "Exit")
    c=inuse.next("Ignore", "Retry", name="Ignore")
    c.event("EndDialog", "Ignore")
    c=inuse.cancel("Retry", "Exit", name="Retry")
    c.event("EndDialog","Retry")

    error = Dialog(db, "ErrorDlg", 50, 10, 330, 101, 65543, title,
                   "ErrorText", None, None)
    error.text("ErrorText", 50,9,280,48,3, "")
    error.control("ErrorIcon", "Icon", 15, 9, 24, 24, 5242881, None, "InfoIcon", None, None)
    error.pushbutton("N",120,72,81,21,3,"No",None).event("EndDialog","ErrorNo")
    error.pushbutton("Y",240,72,81,21,3,"Yes",None).event("EndDialog","ErrorYes")
    error.pushbutton("A",0,72,81,21,3,"Abort",None).event("EndDialog","ErrorAbort")
    error.pushbutton("C",42,72,81,21,3,"Cancel",None).event("EndDialog","ErrorCancel")
    error.pushbutton("I",81,72,81,21,3,"Ignore",None).event("EndDialog","ErrorIgnore")
    error.pushbutton("O",159,72,81,21,3,"Ok",None).event("EndDialog","ErrorOk")
    error.pushbutton("R",198,72,81,21,3,"Retry",None).event("EndDialog","ErrorRetry")

    # Global "Query Cancel" dialog
    cancel = Dialog(db, "CancelDlg", 50, 10, 260, 85, 3, title,
                    "No", "No", "No")
    cancel.text("Text", 48, 15, 194, 30, 3, 
                "Are you sure you want to cancel [ProductName] installation?")
    cancel.control("Icon", "Icon", 15, 15, 24, 24, 5242881, None,
                   "InfoIcon", None, None)
    c=cancel.pushbutton("Yes", 72, 57, 56, 17, 3, "Yes", "No")
    c.event("EndDialog", "Exit")
    
    c=cancel.pushbutton("No", 132, 57, 56, 17, 3, "No", "Yes")
    c.event("EndDialog", "Return")

    # Global "Wait for costing" dialog
    costing = Dialog(db, "WaitForCostingDlg", 50, 10, 260, 85, modal, title,
                     "Return", "Return", "Return")
    costing.text("Text", 48, 15, 194, 30, 3,
                 "Please wait while the installer finishes determining your disk space requirements.")
    costing.control("Icon", "Icon", 15, 15, 24, 24, 5242881, None,
                    "ExclamationIcon", None, None)
    c = costing.pushbutton("Return", 102, 57, 56, 17, 3, "Return", None)
    c.event("EndDialog", "Exit")

    # Preparation dialog: no user input except cancellation
    prep = PyDialog(db, "PrepareDlg", x, y, w, h, modeless, title,
                    "Cancel", "Cancel", "Cancel")
    prep.text("Description", 135, 70, 220, 40, 196611,
              "Please wait while the Installer prepares to guide you through the installation.")
    prep.title("Welcome to the [ProductName] Installer")
    c=prep.text("ActionText", 135, 110, 220, 20, 196611, "Pondering...")
    c.mapping("AxtionText", "Text")
    c=prep.text("ActionData", 135, 135, 220, 30, 196611, None)
    c.mapping("ActionData", "Text")
    prep.back("Back", None, active=0)
    prep.next("Next", None, active=0)
    c=prep.cancel("Cancel", None)
    c.event("SpawnDialog", "CancelDlg")

    # Target directory selection
    seldlg = PyDialog(db, "SelectDirectoryDlg", x, y, w, h, modal, title,
                    "Next", "Next", "Cancel")
    seldlg.title("Select Destination Directory")
    seldlg.text("Description", 135, 50, 220, 40, 196611,
               "Please select a directory for the [ProductName] files.")

    seldlg.back("< Back", None, active=0)
    c = seldlg.next("Next >", "Cancel")
    c.event("SetTargetPath", "TARGETDIR", order=1)
    c.event("SpawnWaitDialog", "WaitForCostingDlg", "CostingComplete = 1", 2)
    c.event("NewDialog", "SelectFeaturesDlg", order=3)

    c = seldlg.cancel("Cancel", "DirectoryCombo")
    c.event("SpawnDialog", "CancelDlg")

    seldlg.control("DirectoryCombo", "DirectoryCombo", 135, 70, 172, 80, 393219,
                   "TARGETDIR", None, "DirectoryList", None)
    seldlg.control("DirectoryList", "DirectoryList", 135, 90, 208, 136, 3, "TARGETDIR",
                   None, "PathEdit", None)
    seldlg.control("PathEdit", "PathEdit", 135, 230, 206, 16, 3, "TARGETDIR", None, "Next", None)
    c = seldlg.pushbutton("Up", 306, 70, 18, 18, 3670019, "Up", None)
    c.event("DirectoryListUp", "0")
    c = seldlg.pushbutton("NewDir", 324, 70, 18, 18, 3670019, "New", None)
    c.event("DirectoryListNew", "0")

    # SelectFeaturesDlg
    features = PyDialog(db, "SelectFeaturesDlg", x, y, w, h, modal|track_disk_space,
                        title, "Tree", "Next", "Cancel")
    features.title("Customize [ProductName]")
    features.text("Description", 135, 35, 220, 15, 196611,
                  "Select the way you want features to be installed.")
    features.text("Text", 135,45,220,30, 3,
                  "Click on the icons in the tree below to change the way features will be installed.")

    c=features.back("< Back", "Next")
    c.event("NewDialog", "SelectDirectoryDlg") # XXX InstallMode=""

    c=features.next("Next >", "Cancel")
    c.mapping("SelectionNoItems", "Enabled")
    c.event("EndDialog", "Return")

    c=features.cancel("Cancel", "Tree")
    c.event("SpawnDialog", "CancelDlg")

    # The browse property is not used, since we have only a single target path (selected already)    
    features.control("Tree", "SelectionTree", 135, 75, 220, 95, 7, "_BrowseProperty",
                     "Tree of selections", "Back", None)

    #c=features.pushbutton("Reset", 42, 243, 56, 17, 3, "Reset", "DiskCost")
    #c.mapping("SelectionNoItems", "Enabled")
    #c.event("Reset", "0")
    
    features.control("Box", "GroupBox", 135, 170, 225, 90, 1, None, None, None, None)

    c=features.xbutton("DiskCost", "Disk &Usage", None, 0.10)
    c.mapping("SelectionNoItems","Enabled")
    c.event("SpawnDialog", "DiskCostDlg")

    c=features.text("ItemDescription", 140, 180, 210, 50, 3,
                  "Multiline description of the currently selected item.")
    c.mapping("SelectionDescription","Text")
    
    c=features.text("ItemSize", 140, 230, 220, 25, 3,
                    "The size of the currently selected item.")
    c.mapping("SelectionSize", "Text")

    # Disk cost
    cost = PyDialog(db, "DiskCostDlg", x, y, w, h, modal, title,
                    "OK", "OK", "OK", bitmap=False)
    cost.text("Title", 15, 6, 200, 15, 196611,
              "{\DlgFontBold8}Disk Space Requirements")
    cost.text("Description", 20, 20, 280, 20, 196611,
              "The disk space required for the installation of the selected features.")
    cost.text("Text", 20, 53, 330, 60, 3,
              "The highlighted volumes (if any) do not have enough disk space "
              "available for the currently selected features.  You can either "
              "remove some files from the highlighted volumes, or choose to "
              "install less features onto local drive(s), or select different "
              "destination drive(s).")
    cost.control("VolumeList", "VolumeCostList", 20, 100, 330, 150, 393223,
                 None, "{120}{70}{70}{70}{70}", None, None)
    cost.xbutton("OK", "Ok", None, 0.5).event("EndDialog", "Return")
    

    # Installation Progress dialog (modeless)
    progress = PyDialog(db, "ProgressDlg", x, y, w, h, modeless, title,
                        "Cancel", "Cancel", "Cancel", bitmap=False)
    progress.text("Title", 20, 15, 200, 15, 196611,
                  "{\DlgFontBold8}[Progress1] [ProductName]")
    progress.text("Text", 35, 65, 300, 30, 3,
                  "Please wait while the Installer [Progress2] [ProductName]. "
                  "This may take several minutes.")
    progress.text("StatusLabel", 35, 100, 35, 20, 3, "Status:")

    c=progress.text("ActionText", 70, 100, w-70, 20, 3, "Pondering...")
    c.mapping("ActionText", "Text")

    #c=progress.text("ActionData", 35, 140, 300, 20, 3, None)
    #c.mapping("ActionData", "Text")

    c=progress.control("ProgressBar", "ProgressBar", 35, 120, 300, 10, 65537,
                       None, "Progress done", None, None)
    c.mapping("SetProgress", "Progress")

    progress.back("< Back", "Next", active=False)
    progress.next("Next >", "Cancel", active=False)
    progress.cancel("Cancel", "Back").event("SpawnDialog", "CancelDlg")

    # Maintenance type: repair/uninstall
    maint = PyDialog(db, "MaintenanceTypeDlg", x, y, w, h, modal, title,
                     "Next", "Next", "Cancel")
    maint.title("Welcome to the [ProductName] Setup Wizard")
    maint.text("BodyText", 135, 63, 230, 42, 3,
               "Select whether you want to repair or remove [ProductName].")
    g=maint.radiogroup("RepairRadioGroup", 135, 108, 230, 48, 3,
                        "MaintenanceForm_Action", "", "Next")
    g.add("Repair", 0, 0, 200, 17, "&Repair [ProductName]")
    g.add("Remove", 0, 18, 200, 17, "Re&move [ProductName]")
    
    maint.back("< Back", None, active=False)
    c=maint.next("Finish", "Cancel")
    # Reinstall: Change progress dialog to "Repair", then invoke reinstall
    # Also set list of reinstalled features to "ALL"
    c.event("[REINSTALL]", "ALL", 'MaintenanceForm_Action="Repair"', 1)
    c.event("[Progress1]", "Repairing", 'MaintenanceForm_Action="Repair"', 2)
    c.event("[Progress2]", "repaires", 'MaintenanceForm_Action="Repair"', 3)
    c.event("Reinstall", "ALL", 'MaintenanceForm_Action="Repair"', 4)

    # Uninstall: Change progress to "Remove", then invoke uninstall
    # Also set list of removed features to "ALL"
    c.event("[REMOVE]", "ALL", 'MaintenanceForm_Action="Remove"', 11)
    c.event("[Progress1]", "Removing", 'MaintenanceForm_Action="Remove"', 12)
    c.event("[Progress2]", "removes", 'MaintenanceForm_Action="Remove"', 13)
    c.event("Remove", "ALL", 'MaintenanceForm_Action="Remove"', 14)

    # Close dialog when maintenance action scheduled    
    c.event("EndDialog", "Return", order=20)
            
    maint.cancel("Cancel", "RepairRadioGroup").event("SpawnDialog", "CancelDlg")
    

def add_features(db):
    global default_feature, tcltk, htmlfiles, tools, testsuite
    default_feature = Feature(db, "DefaultFeature", "Python",
                              "Python Interpreter and Libraries",
                              1, directory = "TARGETDIR")
    tcltk = Feature(db, "TclTk", "Tcl/Tk", "Tkinter, IDLE, pydoc", 3)
    htmlfiles = Feature(db, "Documentation", "Documentation",
                        "Python HTMLHelp File", 5)
    tools = Feature(db, "Tools", "Utility Scripts",
                    "Python utility scripts (Tools/", 7)
    testsuite = Feature(db, "Testsuite", "Test suite",
                        "Python test suite (Lib/test/)", 9)

def add_files(db):
    cab = CAB("python")
    root = Directory(db, cab, None, srcdir, "TARGETDIR", "SourceDir")
    # Create separate components for python.exe and pythonw.exe so we can
    # create advertised shortcuts
    root.start_component("python.exe", default_feature, "python.exe")
    root.add_file("PCBuild/python.exe")
    root.start_component("pythonw.exe", default_feature, "pythonw.exe")
    root.add_file("PCBuild/pythonw.exe")
    
    # Add all other root files into the TARGETDIR component
    root.start_component("TARGETDIR", default_feature)
    root.add_file("PCBuild/w9xpopen.exe") # XXX: separate component to only install on W9x
    root.add_file("PCBuild/python%s%s.dll" % (major, minor)) # XXX separate component for system32
    root.add_file("README.txt", src="README")
    root.add_file("NEWS.txt", src="Misc/NEWS")
    root.add_file("LICENSE.txt", src="LICENSE")
    dirs={}
    # Add all .py files in Lib, except lib-tk, test
    pydirs = [(root,"Lib")]
    while pydirs:
        parent, dir = pydirs.pop()
        if dir == "CVS" or dir.startswith("plat-"):
            continue
        elif dir in ["lib-tk", "idlelib", "Icons"]:
            tcltk.set_current()
        elif dir in ['test', 'output']:
            testsuite.set_current()
        else:
            default_feature.set_current()
        lib = Directory(db, cab, parent, dir, dir, "%s|%s" % (parent.make_short(dir), dir))
        dirs[dir]=lib
        lib.glob("*.txt")
        if dir=='site-packages':
            continue
        files = lib.glob("*.py")
        files += lib.glob("*.pyw")
        if files:
            lib.remove_pyc()
        if dir=='output':
            lib.glob("test_*")
        if dir=='idlelib':
            lib.glob("*.def")
            lib.add_file("idle.bat")
        if dir=="Icons":
            lib.glob("*.gif")
            lib.add_file("idle.icns")
        for f in os.listdir(lib.absolute):
            if os.path.isdir(os.path.join(lib.absolute, f)):
                pydirs.append((lib, f))
    # Add DLLs
    default_feature.set_current()
    lib = Directory(db, cab, root, srcdir+"/PCBuild", "DLLs", "DLLS|DLLs")
    dlls = []
    tclfiles = []
    for f in extensions:
        if f=="_tkinter.pyd":
            continue
        if not os.path.exists(srcdir+"/PCBuild/"+f):
            print "WARNING: Missing extension", f
            continue
        dlls.append(f)
        lib.add_file(f)
    if not os.path.exists(srcdir+"/PCBuild/_tkinter.pyd"):
        print "WARNING: Missing _tkinter.pyd"
    else:
        lib.start_component("TkDLLs", tcltk)
        lib.add_file("_tkinter.pyd")
        dlls.append("_tkinter.pyd")
        tcldir = os.path.normpath(srcdir+"/../tcl84/bin")
        for f in glob.glob1(tcldir, "*.dll"):
            lib.add_file(f, src=os.path.join(tcldir, f))
    # check whether there are any unknown extensions
    for f in glob.glob1(srcdir+"/PCBuild", "*.pyd"):
        if f.endswith("_d.pyd"): continue # debug version
        if f in dlls: continue
        print "WARNING: Unknown extension", f
    
    # Add headers
    default_feature.set_current()
    lib = Directory(db, cab, root, "include", "include", "INCLUDE|include")
    lib.glob("*.h")
    # Add import libraries
    lib = Directory(db, cab, root, "PCBuild", "libs", "LIBS|libs")
    for f in dlls:
        lib.add_file(f.replace('pyd','lib'))
    lib.add_file('python%s%s.lib' % (major, minor))
    # Add Tcl/Tk
    tcldirs = [(root, '../tcl84/lib', 'tcl')]
    tcltk.set_current()
    while tcldirs:
        parent, phys, dir = tcldirs.pop()
        lib = Directory(db, cab, parent, phys, dir, "%s|%s" % (parent.make_short(dir), dir))
        for f in os.listdir(lib.absolute):
            if os.path.isdir(os.path.join(lib.absolute, f)):
                tcldirs.append((lib, f, f))
            else:
                lib.add_file(f)
    # Add tools
    tools.set_current()
    tooldir = Directory(db, cab, root, "Tools", "Tools", "TOOLS|Tools")
    for f in ['i18n', 'pynche', 'Scripts', 'versioncheck', 'webchecker']:
        lib = Directory(db, cab, tooldir, f, f, "%s|%s" % (tooldir.make_short(f), f))
        lib.glob("*.py")
        lib.glob("*.pyw")
        lib.remove_pyc()
        lib.glob("*.txt")
        if f == "pynche":
            x = Directory(db, cab, lib, "X", "X", "X|X")
            x.glob("*.txt")
        if f == 'Scripts':
            lib.add_file("README.txt", src="README")
    # Add documentation
    htmlfiles.set_current()
    lib = Directory(db, cab, root, "Doc", "Doc", "DOC|Doc")
    lib.add_file("Python%s%s.chm" % (major, minor))

    cab.commit(db)    

def add_registry(db):
    # File extensions, associated with the REGISTRY component
    # msidbComponentAttributesRegistryKeyPath = 4
    add_data(db, "Component",
             [("REGISTRY", msilib.gen_uuid(), "TARGETDIR", 4, None,
               "InstallPath")])
    add_data(db, "FeatureComponents",
             [(default_feature.id, "REGISTRY")])
    add_data(db, "Extension",
             # Apparently, the key file of the component is used as the command;
             # the verb table only contributes the arguments. As the result, all
             # verbs for an extension must use the same command.
             # (Verb.Command is just the localized UI label of the verb)
             [(ext, 'python.exe', testprefix+'Python.File', None, default_feature.id),
              (ext+'w', 'pythonw.exe', testprefix+'Python.NoConFile', None, default_feature.id),
              (ext+'c', 'python.exe', testprefix+'Python.CompiledFile', None, default_feature.id),
             ])
    add_data(db, "ProgId",
             [(testprefix+'Python.File', None, None, 'Python File', 'py.ico', None),
              (testprefix+'Python.NoConFile', None, None,
               'Python File (no console)', 'py.ico', None),
              (testprefix+'Python.CompiledFile', None, None,
               'Compiled Python File', 'pyc.ico', None)])
    add_data(db, "Icon",
             [('py.ico', Binary(srcdir+r"\PC\py.ico")),
              ('pyc.ico', Binary(srcdir+r"\PC\pyc.ico"))])
    add_data(db, "Verb",
             [(ext, 'open', 1, None, '"%1" %*'),
              (ext+'w', 'open', 1, None, '"%1" %*'),
              (ext+'c', 'open', 1, None, '"%1" %*'),
              ])
    # IDLE verbs depend on the tcltk feature.
    # For several reasons (see above) we cannot author them into the Verb table
    add_data(db, "Component",
             [("REGISTRY.tcl", msilib.gen_uuid(), "TARGETDIR", 4, None,
               None)])
    add_data(db, "FeatureComponents", [(tcltk.id, "REGISTRY.tcl")])
    pat = r"Software\Classes\%sPython.%sFile\shell\Edit with IDLE\command"
    add_data(db, "Registry",
            [("IDLE.py", -1, pat % (testprefix, ""), "",
              r'"[TARGETDIR]pythonw.exe" "[TARGETDIR]Lib\idlelib\idle.pyw" -n -e "%1"',
              "REGISTRY.tcl"),
             ("IDLE.pyw", -1, pat % (testprefix, "NoCon"), "",
              r'"[TARGETDIR]pythonw.exe" "[TARGETDIR]Lib\idlelib\idle.pyw" -n -e "%1"',
              "REGISTRY.tcl")
            ])
    # Registry keys
    # -1 for Root specifies "dependent on ALLUSERS property"
    prefix = r"Software\%sPython\PythonCore\%s" % (testprefix, short_version)
    add_data(db, "Registry",
             [("InstallPath", -1, prefix+r"\InstallPath", "", "[TARGETDIR]", "REGISTRY"),
              ("InstallGroup", -1, prefix+r"\InstallPath\InstallGroup", "",
               "Python %s" % short_version, "REGISTRY"),
              ("PythonPath", -1, prefix+r"\PythonPath", "",
               "[TARGETDIR]Lib;[TARGETDIR]DLLs;[TARGETDIR]lib-tk", "REGISTRY"),
              ("Documentation", -1, prefix+r"\Help\Main Python Documentation", "",
               r"[TARGETDIR]Doc\Python%s%s.chm" % (major, minor), "REGISTRY"),
              ("Modules", -1, prefix+r"\Modules", "+", None, "REGISTRY"),
              ("AppPaths", -1, r"Software\Microsoft\Windows\CurrentVersion\App Paths\Python.exe",
               "", r"[TARGETDIR]Python.exe", "REGISTRY")
              ])
    # Shortcuts
    add_data(db, "Directory",
             [("ProgramMenuFolder", "TARGETDIR", "."),
              ("MENUDIR", "ProgramMenuFolder", "PY%s%s|%sPython %s.%s" % (major,minor,testprefix,major,minor))])
    add_data(db, "Shortcut",
             [# Advertised shortcuts: targets are features, not files
              # The key file of the component is then entered as the real target
              # XXX, advertised shortcuts don't work, so make them unadvertised
              # for now
              #("IDLE", "MENUDIR", "IDLE|IDLE (Python GUI)", "pythonw.exe",
              # default_feature.id, r"[TARGETDIR]Lib\idlelib\idle.pyw",
              # None, None, None, None, None, "TARGETDIR"),
              #("PyDoc", "MENUDIR", "MODDOCS|Module Docs", "pythonw.exe",
              # default_feature.id, r"[TARGETDIR]Tools\scripts\pydocgui.pyw",
              # None, None, None, None, None, "TARGETDIR"),
              #("Python", "MENUDIR", "PYTHON|Python (command line)", "python.exe",
              # default_feature.id, None,
              # None, None, None, None, None, "TARGETDIR"),
              ("IDLE", "MENUDIR", "IDLE|IDLE (Python GUI)", "REGISTRY",
               r"[TARGETDIR]pythonw.exe", r"[TARGETDIR]Lib\idlelib\idle.pyw",
               None, None, None, None, None, "TARGETDIR"),
              ("PyDoc", "MENUDIR", "MODDOCS|Module Docs", "REGISTRY",
               r"[TARGETDIR]pythonw.exe", r"[TARGETDIR]Tools\scripts\pydocgui.pyw",
               None, None, None, None, None, "TARGETDIR"),
              ("Python", "MENUDIR", "PYTHON|Python (command line)", "REGISTRY",
               r"[TARGETDIR]python.exe", None,
               None, None, None, None, None, "TARGETDIR"),
              # Non-advertised features: must be associated with a registry component
              ("Manual", "MENUDIR", "MANUAL|Python Manuals", "REGISTRY",
               r"[TARGETDIR]Doc\python%s%s.chm" % (major, minor), None,
               None, None, None, None, None, None),
              # XXX: System64Folder on Win64
              ("Uninstall", "MENUDIR", "UNINST|Uninstall Python", "REGISTRY",
               "[SystemFolder]msiexec",  "/x%s" % product_codes[current_version],
               None, None, None, None, None, None),
              ])
    db.Commit()

db = build_database()
try:
    add_features(db)
    add_ui(db)
    add_files(db)
    add_registry(db)
    db.Commit()
finally:
    del db
