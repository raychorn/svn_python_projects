import Tkinter
import tkSimpleDialog
import ScrolledText
from Tkinter import *
import os
import gettext
from stat import *

_ = gettext.gettext

class ViewProjects(tkSimpleDialog.Dialog):

  def __init__(self, parent, folder):
    self.basePath = 'meta'
    self.curPath = self.basePath + '/' + folder
    if (self.curPath.endswith('/')):
      self.curPath = self.curPath[0:len(self.curPath)-1]
    tkSimpleDialog.Dialog.__init__(self, parent, _('Projects Browser'))

  def plainPath(self,fpath):
    if (fpath.endswith('/')):
      fpath = fpath[0:len(fpath)-1]
    return fpath

  def populateFiles(self):
    isFound = False
    while (isFound == False):
      try:
        files = os.listdir(self.curPath)
        isFound = True
      except Exception:
        os.mkdir(self.curPath)
    self._listbox_1.delete(0, END)
    if (self.curPath != self.plainPath(self.basePath)):
      self._listbox_1.insert(END, '..')
    for s in files:
      self._listbox_1.insert(END, s)

  def onSelectListBox(self, event):
    widget = event.widget
    i = widget.curselection()
    if (len(i) > 0):
      self.onOpenItem()
  
  def body(self, master):
    master.pack_configure(fill=Tkinter.BOTH, expand=1)
    self._listbox_1 = Tkinter.Listbox(self,height = 20,width = 60)
    self._listbox_1.see(Tkinter.END)
    self._listbox_1.pack(fill=Tkinter.BOTH)
    self._listbox_1.bind("<Double-Button-1>", self.onSelectListBox)
    self.populateFiles()

  def onNewPath(self):
    try:
      os.mkdir(self.curPath + '/' + self._myNewPath.get())
    except Exception:
      pass
    finally:
      self.populateFiles()

  def onDelItem(self):
    i = self._listbox_1.curselection()
    if (len(i) > 0):
      name = self._listbox_1.get(i[0])
      fpath = self.curPath + '/' + name
      try:
        os.rmdir(fpath)
      except Exception, details:
        pass
      finally:
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
    self._myNewPath = Tkinter.StringVar(self)
    self._entry_1 = Tkinter.Entry(self, width = 30,textvariable = self._myNewPath).pack(side=Tkinter.LEFT)
    self.btnNewPath = Tkinter.Button(self, text=_('(+)'), command=self.onNewPath, width=5).pack(side=Tkinter.LEFT)
    self.btnNewPath = Tkinter.Button(self, text=_('(-)'), command=self.onDelItem, width=5).pack(side=Tkinter.LEFT)
    self.btnNewPath = Tkinter.Button(self, text=_('(*)'), command=self.onOpenItem, width=5).pack(side=Tkinter.LEFT)
    w = Tkinter.Button(self, text=_('Close'), width=10, command=self.ok, default=Tkinter.ACTIVE).pack(side=Tkinter.RIGHT)
    self.bind("<Return>", self.ok)
    self.bind("<Escape>", self.cancel)

if __name__ == '__main__':
  #
  # Create GUI
  #
  root = Tkinter.Tk()
  ViewProjects(root)
