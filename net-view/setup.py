from distutils.core import setup
import py2exe

packages = ["vyperlogix"]
includes = []
excludes = ["pywin", "pywin.debugger", "pywin.debugger.dbgcon",
            "pywin.dialogs", "pywin.dialogs.list",
            "Tkconstants","Tkinter","tcl","wx",
            "Crypto.PublicKey._fastmath",
            "Crypto.Util.winrandom",
            "_pybsddb", "bsddb3.dbutils", "psyco_linux", "r_hmac"
            ]

setup(
    console=['nbtscanner.py'],
    options = {"py2exe": {"compressed": 1,
                          "optimize": 2,
                          "ascii": 1,
                          "bundle_files": 1,
                          "dll_excludes": ["w9xpopen.exe"],
                          "packages": packages,
                          "includes": includes,
                          "excludes": excludes}},
    name = "nbtscanner 1.0",
    zipfile = None,
    windows = [],
    data_files=[],
    )
