from distutils.core import setup
import py2exe

packages = ["vyperlogix", "pyax", "maglib"]
includes = []
excludes = ["pywin", "pywin.debugger", "pywin.debugger.dbgcon",
            "pywin.dialogs", "pywin.dialogs.list",
            "Tkconstants","Tkinter","tcl","wx",
            ]

setup(
    console=['boost.py'],
    options = {"py2exe": {"compressed": 1,
                          "optimize": 2,
                          "ascii": 1,
                          "bundle_files": 1,
                          "dll_excludes": ["w9xpopen.exe"],
                          "packages": packages,
                          "includes": includes,
                          "excludes": excludes}},
    name = "boost 1.1",
    zipfile = None,
    windows = [],
    data_files=[],
    )
