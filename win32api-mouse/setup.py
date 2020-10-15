from distutils.core import setup
import py2exe

packages = ["vyperlogix", "pyHook", "pythoncom", "win32api", "win32con", "win32gui", "win32process"]
includes = []
excludes = ["pywin", "pywin.debugger", "pywin.debugger.dbgcon",
            "pywin.dialogs", "pywin.dialogs.list",
            "Tkconstants","Tkinter","tcl","wx"
            ]

setup(
    console=['go2_harvester.py'],
    options = {"py2exe": {"compressed": 1,
                          "optimize": 2,
                          "ascii": 1,
                          "bundle_files": 1,
                          "dll_excludes": ["w9xpopen.exe",
                          "iconv.dll","intl.dll","libatk-1.0-0.dll",
                          "libgdk_pixbuf-2.0-0.dll","libgdk-win32-2.0-0.dll",
                          "libglib-2.0-0.dll","libgmodule-2.0-0.dll",
                          "libgobject-2.0-0.dll","libgthread-2.0-0.dll",
                          "libgtk-win32-2.0-0.dll","libpango-1.0-0.dll",
                          "libpangowin32-1.0-0.dll","mswsock.dll", "powrprof.dll"],
                          "packages": packages,
                          "includes": includes,
                          "excludes": excludes}},
    name = "go2_harvester 1.0",
    zipfile = None,
    windows = [],
    data_files=[],
    )
