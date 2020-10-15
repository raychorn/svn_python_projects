import MainWindowApp
import CumulativeLogger
import logging
import gettext
_ = gettext.gettext

logging.basicConfig()
l = logging.getLogger()
l.setLevel(logging.INFO)
cl = CumulativeLogger.CumulativeLogger()
l.info(_('Starting the program...'))
MainWindowApp.MainWindowApp(cl).run()