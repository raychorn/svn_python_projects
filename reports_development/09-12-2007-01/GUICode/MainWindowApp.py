import Tkinter
import logging
import ViewLog
import ThreadsConnector
import ActionWindow
import gettext
from Tkinter import *
import onMetadataFrom_mySQL
import onMetadataFrom_MSSQL
import ViewProjects
from vyperlogix import *
from win32api import *
_ = gettext.gettext

def isOSWinXP(winver):
	if (len(winver) < 5):
		return False
	return ( (winver[0] == 5) and (winver[1] == 1) and (winver[2] == 2600) and (winver[3] == 2) and (winver[4] == 'Service Pack 2') )

class App(Frame):
	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.pack()

class MainWindowApp:

	def __init__(self, log):
		self.log    = log
		self.logger = logging.getLogger(self.__class__.__name__)
		self._onMetadataFrom_mySQL = onMetadataFrom_mySQL
		self._onMetadataFrom_MSSQL = onMetadataFrom_MSSQL
		self.persist = shelveSupport.persistence()

	def run(self):
		self.app = app = App()
		self._mySQLDSN = Tkinter.StringVar(app)
		self._myMSSQLDSN = Tkinter.StringVar(app)
		self._myProjectName = Tkinter.StringVar(app)
		self._myStatus = Tkinter.StringVar(app)
		
		app.tkraise()
		app.master.title(_('SQLAlchemy 0.4.0beta4 Utility Version 0.1'));
		app.master.minsize(450, 200)
		app.master.maxsize(450, 200)
		Tkinter.Label(app, borderwidth = 0, font = "Garamond 14", text = "SQLAlchemy 0.4.0beta4 Utility v0.1").grid(row=0, column=1, padx=110, sticky=W)
	
		Tkinter.Button(app, text=_('Metadata from mySQL'), command=self.onMetadataFrom_mySQL, width=20).grid(row=1, column=1, padx=10, sticky=W)
		Tkinter.Button(app, text=_('Metadata from MSSQL'), command=self.onMetadataFrom_MSSQL, width=20).grid(row=1, column=1, padx=145, sticky=W)
		Tkinter.Button(app, text=_('View Log'), command=self.onViewLog, width=10).grid(row=1, column=1, padx=280, sticky=W)
		Tkinter.Button(app, text=_('Exit'), command=self.onExit, width=10).grid(row=1, column=1, padx=355, sticky=W)
	
		Tkinter.Label(app, text = "MySQL DSN:").grid(row=2, column=1, padx=10, pady=5, sticky=W)
		self._entry_1 = Tkinter.Entry(app, width = 58,textvariable = self._mySQLDSN).grid(row=2, column=1, padx=85, pady=5, sticky=W)
	
		Tkinter.Label(app, text = "MSSQL DSN:").grid(row=3, column=1, padx=10, pady=5, sticky=W)
		self._entry_1 = Tkinter.Entry(app, width = 58,textvariable = self._myMSSQLDSN).grid(row=3, column=1, padx=85, pady=5, sticky=W)
	
		Tkinter.Label(app, text = "Project Name:").grid(row=4, column=1, padx=10, pady=1, sticky=W)
		self._entry_1 = Tkinter.Entry(app, width = 50,textvariable = self._myProjectName)
		self._entry_1.grid(row=4, column=1, padx=85, pady=1, sticky=W)
		self._entry_1.configure(state=Tkinter.DISABLED)
		Tkinter.Button(app, text=_('...'), command=self.onViewProjects, width=3).grid(row=4, column=1, padx=395, sticky=W)
	
		Tkinter.Label(app, borderwidth = 0, font = "Garamond 10", text = "",textvariable = self._myStatus).grid(row=5, column=1, padx=5, pady=10, sticky=W)

		winVers = sys.getwindowsversion()
	
		_dsn = 'mysql://root:peekaboo@127.0.0.1/reports_development'
		if (isOSWinXP(winVers)):
			_dsn = 'mysql://root:foobarbaz@192.168.105.67/reports_development'
		dsn = self.persist.unShelveThis('_mySQLDSN')
		if (len(dsn) > 0):
			self._mySQLDSN.set(dsn)
		else:
			self._mySQLDSN.set(_dsn)
		
		_sqlInstanceName = '%s\SQLEXPRESS' % GetComputerName()
		_dsn = 'SERVER=%s;DATABASE=reports_development' % _sqlInstanceName
		dsn = self.persist.unShelveThis('_myMSSQLDSN')
		if ( (len(dsn) > 0) and (dsn.find(_sqlInstanceName) > -1) ):
			self._myMSSQLDSN.set(dsn)
		else:
			self._myMSSQLDSN.set(_dsn)
		
		self._myProjectName.set('')
		#self._myProjectName.set('place your project name here... ([%s],[%s],[%s],[%s],[%s])' % (winVers[0],winVers[1],winVers[2],winVers[3],winVers[4]))
		app.mainloop()
	
	def onExit(self):
		self.app.quit()

	def onViewLog(self):
		ViewLog.ViewLog(self.app, self.log)

	def onViewProjects(self):
		d = ViewProjects.ViewProjects(self.app,self._myProjectName.get())
		toks = d.curPath.split('/')
		toks.remove(toks[0])
		fpath = ''.join(["%s/" % s for s in toks])
		if (fpath.startswith('/')):
		  fpath = fpath[1:len(fpath)]
		if (fpath.endswith('/')):
		  fpath = fpath[0:len(fpath)-1]
		self._myProjectName.set(fpath)

	def logStatus(self,status):
		self._myStatus.set(status)
		self.logger.info(_(status))

	def getThreadsConnector(self,dsn,dbName):
		self.logger.info(_('Preparing and starting the process of creating metadata from %s.'), dbName)
		conn = ThreadsConnector.ThreadsConnector()
		wnd = ActionWindow.ActionWindow(self.app, _('Creating Metadata from %s' % dbName), _('Processing Metadata files...'))
		conn.data.append(dsn)
		if (len(self._myProjectName.get()) > 0):
			conn.data.append(self._myProjectName)
		else:
			self.logStatus('ERROR - Invalid ProjectName! Choose or Create a Project Name.')
			return([-1])
		return (conn,wnd)

	def onMetadataFrom_mySQL(self):
		self.persist.shelveThis('_mySQLDSN',self._mySQLDSN.get())
		handle = self.getThreadsConnector(self._mySQLDSN,'mySQL')
		try:
			if (len(handle) == 2):
				conn = handle[0]
				wnd = handle[1]
				conn.runInGui(wnd, conn, None, self._onMetadataFrom_mySQL.process, 'onMetadataFrom_mySQL')
			elif (len(handle) == 1):
				pass
			else:
				self.logStatus('ERROR - Cannot process the user request due to a programming problem !')
		finally:
			pass

	def onMetadataFrom_MSSQL(self):
		self.persist.shelveThis('_myMSSQLDSN',self._myMSSQLDSN.get())
		handle = self.getThreadsConnector(self._myMSSQLDSN,'MSSQL')
		try:
			if (len(handle) == 2):
				conn = handle[0]
				wnd = handle[1]
				conn.runInGui(wnd, conn, None, self._onMetadataFrom_MSSQL.process, 'onMetadataFrom_MSSQL')
			elif (len(handle) == 1):
				pass
			else:
				self.logStatus('ERROR - Cannot process the user request due to a programming problem !')
		finally:
			pass
