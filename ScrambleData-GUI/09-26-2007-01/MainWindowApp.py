import Tkinter
import logging
import ViewLog
import ThreadsConnector
import ActionWindow
import gettext
from Tkinter import *
import ViewFiles
from win32api import *
import shelveSupport
_ = gettext.gettext

class App(Frame):
	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.pack()

class MainWindowApp:

	def __init__(self, log):
		self.log    = log
		self.logger = logging.getLogger(self.__class__.__name__)
		self.persist = shelveSupport.persistence()

	def run(self):
		self.app = app = App()
		self._myFileName = Tkinter.StringVar(app)
		
		app.tkraise()
		app.master.title(_('Scramble Data Version 1.0'));
		app.master.minsize(450, 200)
		app.master.maxsize(450, 200)
		Tkinter.Label(app, borderwidth = 0, font = "Garamond 14", text = "Scramble Data Version 1.0").grid(row=0, column=1, padx=110, sticky=W)
	
		Tkinter.Button(app, text=_('View Log'), command=self.onViewLog, width=10).grid(row=5, column=1, padx=280, sticky=W)
		Tkinter.Button(app, text=_('Exit'), command=self.onExit, width=10).grid(row=5, column=1, padx=355, sticky=W)
	
		self._label_1 = Tkinter.Label(app, text = "File Name:").grid(row=4, column=1, padx=10, pady=1, sticky=W)
		self._entry_1 = Tkinter.Entry(app, width = 50,textvariable = self._myFileName)
		self._entry_1.grid(row=4, column=1, padx=85, pady=1, sticky=W)
		self._entry_1.configure(state=Tkinter.DISABLED)
		Tkinter.Button(app, text=_('...'), command=self.onViewFiles, width=3).grid(row=4, column=1, padx=395, sticky=W)
	
		winVers = sys.getwindowsversion()
	
		app.mainloop()
	
	def onExit(self):
		self.app.quit()

	def onViewLog(self):
		ViewLog.ViewLog(self.app, self.log)
		
	def onViewFiles(self):
		d = ViewFiles.fileChooser(self.app, self._myFileName)
		toks = d.curPath.split('/')
		toks.remove(toks[0])
		fpath = ''.join(["%s/" % s for s in toks])
		if (fpath.startswith('/')):
			fpath = fpath[1:len(fpath)]
		if (fpath.endswith('/')):
			fpath = fpath[0:len(fpath)-1]
		self._myFileName.set(fpath)

	def logStatus(self,status):
		self._myStatus.set(status)
		self.logger.info(_(status))

	def getThreadsConnector(self,dsn,dbName):
		self.logger.info(_('Preparing and starting the process of Scrambling the data.'))
		conn = ThreadsConnector.ThreadsConnector()
		wnd = ActionWindow.ActionWindow(self.app, _('Scrambling the data'), _('Scrambling files...'))
		return (conn,wnd)
