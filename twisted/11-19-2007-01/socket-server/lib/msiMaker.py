import msilib, schema, sequence, os, sets, glob
from msilib import Feature, CAB, Directory, Dialog, Binary, add_data
import uisample
from win32com.client import constants
import PyDialog

class msiMaker():
    def __init__(self,_package_name,_package_author,_srcdir,_current_version):
        msilib.Win64 = 0
        self.current_version = _current_version
        self.testpackage=0
        self.package_name = _package_name
        self.package_author = _package_author
        self.srcdir = _srcdir
        self.major, self.minor = self.current_version.split(".")[:2]
        self.short_version = self.major+"."+self.minor
        self.upgrade_code='{92A24481-3ECB-40FC-8836-04B7966EC0D5}'  # This should never change
        self.product_codes = {
            _current_version  : msilib.gen_uuid()
        }
        self.schema = schema
        self.sequence = sequence
        self.isDebug = True
        msilib.reset()    

    def build_database(self):
        self.db = msilib.init_database("%s%s.msi" % (self.package_name,self.current_version),self.schema,
                                  "%s %s" % (self.package_name,self.current_version),
                                  self.product_codes[self.current_version],
                                  self.current_version,
                                  self.package_author)
        if (self.isDebug):
            print '(build_database) :: db=(%s)' % (str(self.db))
        msilib.add_tables(self.db, self.sequence)
        self.db.Commit()

    def add_ui(self):
        x = y = 50
        w = 370
        h = 300
        title = "[ProductName] Setup"
    
        # Dialog styles
        modal = 3      # visible | modal
        modeless = 1   # visible
        track_disk_space = 32
    
        add_data(self.db, 'ActionText', uisample.ActionText)
        add_data(self.db, 'UIText', uisample.UIText)
    
        # Bitmaps
        #add_data(self.db, "Binary",
        #         [("PythonWin", msilib.Binary(srcdir+r"\PCbuild\installer.bmp")), # 152x328 pixels
        #          ("Up",msilib.Binary("Up.bin")),
        #          ("New",msilib.Binary("New.bin")),
        #          ("InfoIcon",msilib.Binary("info.bin")),
        #          ("ExclamationIcon",msilib.Binary("exclamic.bin")),
        #         ])
    
        # UI customization properties
        add_data(self.db, "Property",
                 [("DefaultUIFont", "DlgFont8"),
                  ("ErrorDialog", "ErrorDlg"),
                  ("Progress1", "Install"),   # modified in maintenance type dlg
                  ("Progress2", "installs"),
                  ("MaintenanceForm_Action", "Repair")])
    
        # Fonts
        add_data(self.db, "TextStyle",
                 [("DlgFont8", "Tahoma", 9, None, 0),
                  ("DlgFontBold8", "Tahoma", 8, None, 1), #bold
                  ("VerdanaBold13", "Verdana", 13, None, 1),
                 ])
    
        # Custom actions
        add_data(self.db, "CustomAction", [
            # msidbCustomActionTypeFirstSequence + msidbCustomActionTypeTextData + msidbCustomActionTypeProperty
            ("InitialTargetDir", 307, "TARGETDIR",
             "[WindowsVolume]Python%s%s" % (self.major, self.minor))
            ])
    
        # UI Sequences
        add_data(self.db, "InstallUISequence",
                 [("PrepareDlg", None, 140),
                  ("InitialTargetDir", 'TARGETDIR=""', 750),
                  ("SelectDirectoryDlg", "Not Installed", 1230),
                  # XXX notyet
                  #("ResumeDlg", "Installed AND (RESUME OR Preselected)", 1240),
                  ("MaintenanceTypeDlg", "Installed AND NOT RESUME AND NOT Preselected", 1250),
                  ("ProgressDlg", None, 1280)])
        add_data(self.db, "AdminUISequence",
                 [("InitialTargetDir", 'TARGETDIR=""', 750)])
    
        # Standard dialogs: FatalError, UserExit, ExitDialog
        fatal=PyDialog.PyDialog(self.db, "FatalError", x, y, w, h, modal, title, "Finish", "Finish", "Finish")
        fatal.title("[ProductName] Installer ended prematurely")
        fatal.back("< Back", "Finish", active = 0)
        fatal.cancel("Cancel", "Back", active = 0)
        fatal.text("Description1", 135, 70, 220, 60, 196611,
                   "[ProductName] setup ended prematurely because of an error.  Your system has not been modified.  To install this program at a later time, please run the installation again.")
        fatal.text("Description2", 135, 135, 220, 20, 196611,
                   "Click the Finish button to exit the Installer.")
        c=fatal.next("Finish", "Cancel", name="Finish")
        c.event("EndDialog", "Exit")
        
        user_exit=PyDialog.PyDialog(self.db, "UserExit", x, y, w, h, modal, title, "Finish", "Finish", "Finish")
        user_exit.title("[ProductName] Installer was interrupted")
        user_exit.back("< Back", "Finish", active = 0)
        user_exit.cancel("Cancel", "Back", active = 0)
        user_exit.text("Description1", 135, 70, 220, 40, 196611,
                   "[ProductName] setup was interrupted.  Your system has not been modified.  "
                   "To install this program at a later time, please run the installation again.")
        user_exit.text("Description2", 135, 115, 220, 20, 196611, "Click the Finish button to exit the Installer.")
        c = user_exit.next("Finish", "Cancel", name="Finish")
        c.event("EndDialog", "Exit")
        
        exit_dialog = PyDialog.PyDialog(self.db, "ExitDialog", x, y, w, h, modal, title, "Finish", "Finish", "Finish")
        exit_dialog.title("Completing the [ProductName] Installer")
        exit_dialog.back("< Back", "Finish", active = 0)
        exit_dialog.cancel("Cancel", "Back", active = 0)
        exit_dialog.text("Description", 135, 115, 220, 20, 196611, "Click the Finish button to exit the Installer.")
        c = exit_dialog.next("Finish", "Cancel", name="Finish")
        c.event("EndDialog", "Return")
    
        # Required dialog: FilesInUse, ErrorDlg
        inuse = PyDialog.PyDialog(self.db, "FilesInUse", x, y, w, h, 19, title, "Retry", "Retry", "Retry", bitmap=False)
        inuse.text("Title", 15, 6, 200, 15, 196611, r"{\DlgFontBold8}Files in Use")
        inuse.text("Description", 20, 23, 280, 20, 196611, "Some files that need to be updated are currently in use.")
        inuse.text("Text", 20, 55, 330, 50, 3,
                   "The following applications are using files that need to be updated by this setup. Close these applications and then click Retry to continue the installation or Cancel to exit it.")
        inuse.control("List", "ListBox", 20, 107, 330, 130, 7, "FileInUseProcess", None, None, None)
        c=inuse.back("Exit", "Ignore", name="Exit")
        c.event("EndDialog", "Exit")
        c=inuse.next("Ignore", "Retry", name="Ignore")
        c.event("EndDialog", "Ignore")
        c=inuse.cancel("Retry", "Exit", name="Retry")
        c.event("EndDialog","Retry")
    
        error = Dialog(self.db, "ErrorDlg", 50, 10, 330, 101, 65543, title, "ErrorText", None, None)
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
        cancel = Dialog(self.db, "CancelDlg", 50, 10, 260, 85, 3, title, "No", "No", "No")
        cancel.text("Text", 48, 15, 194, 30, 3, "Are you sure you want to cancel [ProductName] installation?")
        cancel.control("Icon", "Icon", 15, 15, 24, 24, 5242881, None, "InfoIcon", None, None)
        c=cancel.pushbutton("Yes", 72, 57, 56, 17, 3, "Yes", "No")
        c.event("EndDialog", "Exit")
        c=cancel.pushbutton("No", 132, 57, 56, 17, 3, "No", "Yes")
        c.event("EndDialog", "Return")
    
        # Global "Wait for costing" dialog
        costing = Dialog(self.db, "WaitForCostingDlg", 50, 10, 260, 85, modal, title, "Return", "Return", "Return")
        costing.text("Text", 48, 15, 194, 30, 3,
                     "Please wait while the installer finishes determining your disk space requirements.")
        costing.control("Icon", "Icon", 15, 15, 24, 24, 5242881, None, "ExclamationIcon", None, None)
        c = costing.pushbutton("Return", 102, 57, 56, 17, 3, "Return", None)
        c.event("EndDialog", "Exit")
    
        # Preparation dialog: no user input except cancellation
        prep = PyDialog.PyDialog(self.db, "PrepareDlg", x, y, w, h, modeless, title, "Cancel", "Cancel", "Cancel")
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
        seldlg = PyDialog.PyDialog(self.db, "SelectDirectoryDlg", x, y, w, h, modal, title, "Next", "Next", "Cancel")
        seldlg.title("Select Destination Directory")
        seldlg.text("Description", 135, 50, 220, 40, 196611, "Please select a directory for the [ProductName] files.")
    
        seldlg.back("< Back", None, active=0)
        c = seldlg.next("Next >", "Cancel")
        c.event("SetTargetPath", "TARGETDIR", order=1)
        c.event("SpawnWaitDialog", "WaitForCostingDlg", "CostingComplete = 1", 2)
        c.event("NewDialog", "SelectFeaturesDlg", order=3)
    
        c = seldlg.cancel("Cancel", "DirectoryCombo")
        c.event("SpawnDialog", "CancelDlg")
    
        seldlg.control("DirectoryCombo", "DirectoryCombo", 135, 70, 172, 80, 393219, "TARGETDIR", None, "DirectoryList", None)
        seldlg.control("DirectoryList", "DirectoryList", 135, 90, 208, 136, 3, "TARGETDIR", None, "PathEdit", None)
        seldlg.control("PathEdit", "PathEdit", 135, 230, 206, 16, 3, "TARGETDIR", None, "Next", None)
        c = seldlg.pushbutton("Up", 306, 70, 18, 18, 3670019, "Up", None)
        c.event("DirectoryListUp", "0")
        c = seldlg.pushbutton("NewDir", 324, 70, 18, 18, 3670019, "New", None)
        c.event("DirectoryListNew", "0")
    
        # SelectFeaturesDlg
        features = PyDialog.PyDialog(self.db, "SelectFeaturesDlg", x, y, w, h, modal|track_disk_space, title, "Tree", "Next", "Cancel")
        features.title("Customize [ProductName]")
        features.text("Description", 135, 35, 220, 15, 196611, "Select the way you want features to be installed.")
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
        features.control("Tree", "SelectionTree", 135, 75, 220, 95, 7, "_BrowseProperty", "Tree of selections", "Back", None)
    
        #c=features.pushbutton("Reset", 42, 243, 56, 17, 3, "Reset", "DiskCost")
        #c.mapping("SelectionNoItems", "Enabled")
        #c.event("Reset", "0")
        
        features.control("Box", "GroupBox", 135, 170, 225, 90, 1, None, None, None, None)
    
        c=features.xbutton("DiskCost", "Disk &Usage", None, 0.10)
        c.mapping("SelectionNoItems","Enabled")
        c.event("SpawnDialog", "DiskCostDlg")
    
        c=features.text("ItemDescription", 140, 180, 210, 50, 3, "Multiline description of the currently selected item.")
        c.mapping("SelectionDescription","Text")
        
        c=features.text("ItemSize", 140, 230, 220, 25, 3, "The size of the currently selected item.")
        c.mapping("SelectionSize", "Text")
    
        # Disk cost
        cost = PyDialog.PyDialog(self.db, "DiskCostDlg", x, y, w, h, modal, title, "OK", "OK", "OK", bitmap=False)
        cost.text("Title", 15, 6, 200, 15, 196611, "{\DlgFontBold8}Disk Space Requirements")
        cost.text("Description", 20, 20, 280, 20, 196611,
                  "The disk space required for the installation of the selected features.")
        cost.text("Text", 20, 53, 330, 60, 3,
                  "The highlighted volumes (if any) do not have enough disk space "
                  "available for the currently selected features.  You can either "
                  "remove some files from the highlighted volumes, or choose to "
                  "install less features onto local drive(s), or select different "
                  "destination drive(s).")
        cost.control("VolumeList", "VolumeCostList", 20, 100, 330, 150, 393223, None, "{120}{70}{70}{70}{70}", None, None)
        cost.xbutton("OK", "Ok", None, 0.5).event("EndDialog", "Return")
        
    
        # Installation Progress dialog (modeless)
        progress = PyDialog.PyDialog(self.db, "ProgressDlg", x, y, w, h, modeless, title, "Cancel", "Cancel", "Cancel", bitmap=False)
        progress.text("Title", 20, 15, 200, 15, 196611, "{\DlgFontBold8}[Progress1] [ProductName]")
        progress.text("Text", 35, 65, 300, 30, 3,
                      "Please wait while the Installer [Progress2] [ProductName]. "
                      "This may take several minutes.")
        progress.text("StatusLabel", 35, 100, 35, 20, 3, "Status:")
    
        c=progress.text("ActionText", 70, 100, w-70, 20, 3, "Pondering...")
        c.mapping("ActionText", "Text")
    
        #c=progress.text("ActionData", 35, 140, 300, 20, 3, None)
        #c.mapping("ActionData", "Text")
    
        c=progress.control("ProgressBar", "ProgressBar", 35, 120, 300, 10, 65537, None, "Progress done", None, None)
        c.mapping("SetProgress", "Progress")
    
        progress.back("< Back", "Next", active=False)
        progress.next("Next >", "Cancel", active=False)
        progress.cancel("Cancel", "Back").event("SpawnDialog", "CancelDlg")
    
        # Maintenance type: repair/uninstall
        maint = PyDialog.PyDialog(self.db, "MaintenanceTypeDlg", x, y, w, h, modal, title, "Next", "Next", "Cancel")
        maint.title("Welcome to the [ProductName] Setup Wizard")
        maint.text("BodyText", 135, 63, 230, 42, 3, "Select whether you want to repair or remove [ProductName].")
        g=maint.radiogroup("RepairRadioGroup", 135, 108, 230, 48, 3, "MaintenanceForm_Action", "", "Next")
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
    

    def add_features(self):
        global default_feature
        if (self.isDebug):
            print '(add_features).1 :: db=(%s)' % (str(self.db))
        default_feature = Feature(self.db, "DefaultFeature", "DSS", "DSS Installation", 1, directory = "TARGETDIR")
        #tcltk = Feature(self.db, "TclTk", "Tcl/Tk", "Tkinter, IDLE, pydoc", 3)
        #htmlfiles = Feature(self.db, "Documentation", "Documentation", "Python HTMLHelp File", 5)
        #tools = Feature(self.db, "Tools", "Utility Scripts", "Python utility scripts (Tools/", 7)
        #testsuite = Feature(self.db, "Testsuite", "Test suite", "Python test suite (Lib/test/)", 9)

    def _add_files(self):
        self.cab = CAB(self.package_name)
        self.root = Directory(self.db, self.cab, None, self.srcdir, "TARGETDIR", "SourceDir")
        
        # Add all other root files into the TARGETDIR component
        self.root.start_component("TARGETDIR", default_feature)
        self.dirs = {}
        pydirs = [(self.root,"Lib")]
        while pydirs:
            parent, dir = pydirs.pop()
            print '(_add_files) :: parent=(%s), dir=(%s)' % (str(parent),str(dir))
            if dir == "CVS" or dir.startswith("plat-"):
                continue
            else:
                default_feature.set_current()
            lib = Directory(self.db, self.cab, parent, dir, dir, "%s|%s" % (parent.make_short(dir), dir))
            self.dirs[dir]=lib
            for f in os.listdir(lib.absolute):
                if os.path.isdir(os.path.join(lib.absolute, f)):
                    pydirs.append((lib, f))
        print '(_add_files) :: self.dirs=(%s)' % (str(self.dirs))

    def add_files(self,files):
        self.cab = CAB(self.package_name)
        self.root = Directory(self.db, self.cab, None, '\\', "TARGETDIR", "SourceDir")
        print '(add_files) :: self.srcdir=(%s)' % (self.srcdir)
        
        dirs={}
        # Add all other root files into the TARGETDIR component
        self.root.start_component("TARGETDIR", default_feature)
        # BEGIN: This block MUST remain intact, as-is or bad things may happen...
        _cur_dir = '\\'
        lib = self.root
        # END! This block MUST remain intact, as-is or bad things may happen...
        _parent = self.root
        _dir = "Lib"
        for f in files:
            if ( (str(f.__class__).find("'tuple'") > -1) or (str(f.__class__).find("'list'") > -1) ):
                _f = f[1]
            else:
                _f = f
            f_dir = os.path.dirname(_f)
            print '(add_files) :: f_dir=(%s), _f=(%s)' % (f_dir,_f)
            if (_cur_dir != f_dir):
                print '(add_files) :: NEW DIRECTORY !\n'
                _dir = f_dir # .split(os.sep)[-1]
                lib = Directory(self.db, self.cab, _parent, _dir, _dir, "%s|%s" % (_parent.make_short(_dir), _dir))
                dirs[dir]=lib
                _cur_dir = f_dir
            lib.add_file(_f.split(os.sep)[-1])
    
        self.cab.commit(self.db)    

    def add_registry(self):
        # File extensions, associated with the REGISTRY component
        # msidbComponentAttributesRegistryKeyPath = 4
        add_data(self.db, "Component",
                 [("REGISTRY", msilib.gen_uuid(), "TARGETDIR", 4, None, "InstallPath")])
        add_data(self.db, "FeatureComponents", [(default_feature.id, "REGISTRY")])
        self.db.Commit()

    def make_msi(self,files):
        self.build_database()
        try:
            if (self.isDebug):
                print '(make_msi) :: BEFORE.add_features(), db=(%s)' % (str(self.db))
            self.add_features()
            if (self.isDebug):
                print '(make_msi) :: BEFORE.add_ui()'
            self.add_ui()
            if (self.isDebug):
                print '(make_msi) :: BEFORE.add_files()'
            self._add_files()
            self.add_files(files)
            if (self.isDebug):
                print '(make_msi) :: BEFORE.add_registry()'
            self.add_registry()
            if (self.isDebug):
                print '(make_msi) :: BEFORE.db.Commit()'
            self.db.Commit()
        finally:
            if (self.isDebug):
                print '(make_msi) :: BEFORE.[del self.db]'
            del self.db
