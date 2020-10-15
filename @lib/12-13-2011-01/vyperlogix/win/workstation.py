def workstation_is_locked():
    import ctypes
    user32 = ctypes.windll.User32
    OpenDesktop = user32.OpenDesktopA
    SwitchDesktop = user32.SwitchDesktop
    DESKTOP_SWITCHDESKTOP = 0x0100
    hDesktop = OpenDesktop("default", 0, False, DESKTOP_SWITCHDESKTOP)
    result = SwitchDesktop(hDesktop)
    return not result

