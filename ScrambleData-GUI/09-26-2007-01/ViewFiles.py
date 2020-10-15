import Tkinter
import tkSimpleDialog
import ScrolledText
from Tkinter import *
import os
import gettext
from stat import *
import re
import win32file
import isOSWinXP

_ = gettext.gettext

str_to_i = {'0':0, '1':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9}

class fileChooser(tkSimpleDialog.Dialog):

	def __init__(self, parent, _myFileName):
		self._myFileName = _myFileName
		self.curPath = self.basePath = os.getcwd()
		if (self.curPath.endswith('/')):
			self.curPath = self.curPath[0:len(self.curPath)-1]
		tkSimpleDialog.Dialog.__init__(self, parent, _('File Browser'))

	def plainPath(self,fpath):
		if (fpath.endswith('/')):
			fpath = fpath[0:len(fpath)-1]
		return fpath

	def getLogicalDrives(self):
		value = []
		drives = win32file.GetLogicalDrives()
		for drive in range(26):
			if drives & (1 << drive):
				letter = chr(65 + drive)
				if win32file.GetDriveType(letter + ":\\") == win32file.DRIVE_FIXED:
					value.append(letter)
		value.sort()
		return value
		
	def populateFiles(self):
		self._myPath.set(self.curPath)
		files = []
		for dirpath, dirnames, filenames in os.walk(self.curPath):
			for f in dirnames:
				if ( (f.startswith('.') == False) and (f.startswith('$') == False) ):
					files.append('[%s]' % f)
			for f in filenames:
				files.append(f)
			break
		self._listbox_1.delete(0, END)
		toks = self.curPath.split(os.sep)
		p = os.sep.join(toks[0:len(toks)-1])
		if (p.endswith(':')):
			for f in self.getLogicalDrives():
				ff = f + (isOSWinXP.isOSWinAny() and ':' or '') + os.sep
				if (ff != self.curPath):
					self._listbox_1.insert(END, '.. (%s:)' % f)
		else:
			self._listbox_1.insert(END, '.. (%s)' % p)
		for s in files:
			self._listbox_1.insert(END, s)

	def stripPathFrom(self,path):
		s = path
		reobj = re.compile(r"[(]+.*[)]")
		match = reobj.search(path)
		if match:
			s = match.group()
			s = s[1:len(s)-1]
		return s
		
	def issueCallback(self, fname):
		print 'issueCallback() :: self._myFileName.__class__=(%s)' % str(self._myFileName.__class__)
		try:
			self._myFileName.set(fname)
			self.ok()
		except Exception, details:
			print 'Error in issueCallback() due to (%s)' % str(details)
	
	def onSelectListBox(self, event):
		widget = event.widget
		s = ''
		i = widget.curselection()
		if (len(str(i)) > 0):
			try:
				s = self.stripPathFrom(widget.get(i))
			except Exception, details:
				s = ''
			if (len(s) > 0):
				_i = -1
				_f = s.find(os.sep)
				if (_f == -1) or (_f == len(s)):
					d = self.getLogicalDrives()
					try:
						_i = d.index(s[0])
					except Exception, details:
						_i = -1
				if (os.path.isdir(s)) or (_i > -1):
					if (_i > -1):
						s = d[_i] + ':' + os.sep
					self.curPath = s
					print '\n'
					self.populateFiles()
				else:
					self.issueCallback(s)

	
	def body(self, master):
		self._myPath = Tkinter.StringVar(self)
		self._labelPath = Tkinter.Label(self, borderwidth = 0, font = "Garamond 10", text = "",textvariable = self._myPath)
		self._labelPath.pack(fill=Tkinter.BOTH)
		self._scrollbar = Scrollbar(self, orient=VERTICAL)
		self._listbox_1 = Tkinter.Listbox(self,height = 40,width = 60, yscrollcommand=self._scrollbar.set)
		self._scrollbar.config(command=self._listbox_1.yview)
		self._scrollbar.pack(side=RIGHT, fill=Y)
		self._listbox_1.pack(side=LEFT, fill=BOTH, expand=1)
		self._listbox_1.see(Tkinter.END)
		#self._listbox_1.pack(fill=Tkinter.BOTH)
		self._listbox_1.bind("<Double-Button-1>", self.onSelectListBox)
		self.populateFiles()

	def onOpenItem(self):
		i = self._listbox_1.curselection()
		if (len(i) > 0):
			name = self._listbox_1.get(i[0])
			if (name == '..'):
				toks = self.curPath.split('/')
				toks.pop()
				fpath = ''.join(["%s/" % s for s in toks])
				if (fpath.endswith('/')):
					fpath = fpath[0:len(fpath)-1]
			else:
				fpath = self.curPath + '/' + name
			print 'fpath=%s' % fpath
			self.curPath = fpath
			self.populateFiles()

	def buttonbox(self):
		pass
		#self._myNewPath = Tkinter.StringVar(self)
		#w = Tkinter.Button(self, text=_('Close'), width=10, command=self.ok, default=Tkinter.ACTIVE).pack(side=Tkinter.BOTH)
		#self.bind("<Return>", self.ok)
		#self.bind("<Escape>", self.cancel)

if __name__ == '__main__':
	root = Tkinter.Tk()
	ViewProjects(root)