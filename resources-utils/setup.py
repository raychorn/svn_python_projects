from distutils.core import setup
import py2exe

packages = ["vyperlogix", "encodings", "sqlalchemy"]
includes = []
excludes = ["pywin", "pywin.debugger", "pywin.debugger.dbgcon",
            "pywin.dialogs", "pywin.dialogs.list",
            "Tkconstants","Tkinter","tcl",
            ]
setup(console=['create.py'],
    options = {"py2exe": {"compressed": 1,
                          "optimize": 2,
                          "ascii": 1,
                          "bundle_files": 1,
                          "packages": packages,
                          "includes": includes,
                          "excludes": excludes}},

    zipfile = None,
    )