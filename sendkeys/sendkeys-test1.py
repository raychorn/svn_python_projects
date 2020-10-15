from vyperlogix.win import SendKeys
from vyperlogix.win import workstation

#SendKeys.SendKeys("""
    #{LWIN}
    #{PAUSE 2.25}
    #Notepad.exe{ENTER}
    #{PAUSE 2}
    #Hello{SPACE}World!
    #{PAUSE 2}
    #%{F4}
    #n
#""")

print 'DEBUG: workstation_is_locked=%s' % (workstation.workstation_is_locked())

if (0):
    SendKeys.SendKeys("""
    {LWIN}{PAUSE 0.5}{TAB}{TAB}{PAUSE 0.5}{RIGHT}{PAUSE 0.5}{DOWN}{DOWN}{PAUSE 0.5}{ENTER}
    """)
