#!/usr/bin/env python
#Author: Vincent DELFT
#
#This program is free software; you can redistribute it and/or
#modify it under the terms of the GNU General Public License
#as published by the Free Software Foundation; either version 2
#of the License, or (at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

# $Id: dirssync.py,v 1.13 2003/11/13 21:16:48 vincent_delft Exp $

"""
WINDOWS ISSUES

Microsoft Windows XP and 2000 cause the following problems when files are
transferred to a non-NTFS file system:
    * the modification times are incremented by 1 second
    * older Windows versions mess up the capitalisation of the files

This confounds dirssync, which relies on both information to determine which
files to transfer. It is recommended that only NTFS file systems be used in
conjunction with Win XP and 2K.    
"""

import _psyco

from wxPython.wx import *
from wxPython.lib.filebrowsebutton import FileBrowseButton
import pickle
import os
import os.path
import string
import shutil
import gettext
wxInitAllImageHandlers()

# Install locale language file or english if there is no 
# translation file for local language
if gettext.find('dirssync')!=None:
    #looks for translation file in default path usually /usr/share/locale
    gettext.translation('dirssync').install()
    print "dirssync.py is using this lang file: ",gettext.find('dirssync')
elif gettext.find('dirssync',os.path.join(os.getcwd(),"locale"))!=None:
    #looks for translation file in dirsync path
    gettext.translation('dirssync',os.path.join(os.getcwd(),"locale")).install()
    print "dirssync.py is using this lang file: ",gettext.find('dirssync',os.path.join(os.getcwd(),"locale"))
else:
    #if no language file exists use internal messages
    print "dirssync.py uses internal messages: no language file found. Default, english, will be used"
    _=lambda msg: msg

REMOTE_LABEL = _("Remote")
LOCAL_LABEL = _("Local")

global listdirs,listfiles
listfiles = {}
listdirs={}

#define booleans, if necessary (pre-python 2.3)
try: True
except NameError: True, False = 1 , 0


class file_criteria:
    __ALL__=['mtime','size']
    default='mtime'
    class mtime:
        msg=_("comparison based on the modification time")
        def comp(self,file):
            return os.path.getmtime(file)
    class size:
        msg=_("comparison based on the file size (bigger is the winner)")
        def comp(self,file):
            return os.path.getsize(file)


class transfer:
    def __init__(self,log,options):
        self.log=log
        self.cdirdic={}
        self.rdirdic={}
        self.crootdir=""
        self.rrootdir=""
        self.options=options


    def removeexcludedlist(self,dir,names):
        import glob
        try:
            fid=open(dir+".dirsync","r")
        except IOError:
            return names
        content=fid.read()
        fid.close()
        for excludedcriteria in content.split("\n"):
            excludedcriteria=excludedcriteria.strip()
            excludedfiles=glob.glob(os.path.join(dir,excludedcriteria))
            for elem in excludedfiles:
                excludedfile=os.path.basename(elem)
                if excludedfile in names:
                    names.pop(names.index(excludedfile))
                    #print "in %s will exclude %s" % (dir,excludedfile)
        return names

    def _getlocaldir(self,arg,cdir,cnames):
        #print "local directory: ",cdir
        self.log.add(_("Exploring local ") + cdir)
        relatifpath=string.replace(cdir,self.crootdir,"")
        cnames=self.removeexcludedlist(cdir,cnames)
        for cname in cnames:
            try:
                self.cdirdic[os.path.join(relatifpath,cname)]=self.options.comparison_selected(os.path.join(cdir,cname))
            except OSError:
                pass

    def _getremotedir(self,arg,rdir,rnames):
        #print "remote directory: ",rdir
        self.log.add(_("Exploring remote ")+rdir)
        relatifpath=string.replace(rdir,self.rrootdir,"")
        rnames=self.removeexcludedlist(rdir,rnames)
        for rname in rnames:
            try:
                self.rdirdic[os.path.join(relatifpath,rname)]=self.options.comparison_selected(os.path.join(rdir,rname))
            except OSError:
                pass

    def update(self, res, src, dest): #srcroot, srcdir, destroot, destdir, destlabel):
        'update res with required actions'

        (srcroot, srcdir, srclabel, srccopy) = src
        (destroot, destdir, destlabel, destcopy) = dest

        #don't do anything if a copy is not required
        if(not srccopy): return


        for elem in srcdir.keys():
            srcfile = os.path.join(srcroot, elem)
            destfile = os.path.join(destroot, elem)
            abssrcfile = os.path.join(srcroot, elem)
            absdestfile = os.path.join(destroot,elem)

            HasKey = destdir.has_key(elem)

            if(os.path.isfile(srcfile)):
                stale = True
                if(HasKey):
                    if(srcdir[elem] <= destdir[elem]): stale = False

                if(stale):  res.append((_("yes"), "copy " + _("to ") + destlabel, abssrcfile, absdestfile))

            else: #it is a directory
                if(not HasKey):
                    res.append((_("yes"), "mkdir " + _("on ") + destlabel, absdestfile, ""))


    def delete(self, res, src, dest):
        'Account for any deletions'

        (srcroot, srcdir, srclabel, srccopy) = src
        (destroot, destdir, destlabel, destcopy) = dest

        #don't do anything if deletion is not required
        deletionRequired = (srccopy == True and destcopy == False and
        self.options.delete() == True)
        if(not deletionRequired): return


        for elem in destdir.keys():
            srcfile = os.path.join(srcroot, elem)
            destfile = os.path.join(destroot, elem)
            abssrcfile = os.path.join(srcroot, elem)
            absdestfile = os.path.join(destroot,elem)

            HasKey = srcdir.has_key(elem)
            if(HasKey): continue #no deletion to this element is required

            if(os.path.isfile(destfile)):
                res.append((_("yes"), "rm " + _("on ") + destlabel, absdestfile, ""))
            else: #it is a directory
                res.append((_("yes"), "rmdir " + _("on ") + destlabel, absdestfile, ""))


    def transfer(self,listdirs):
        res=[]
        items=listdirs.items()
        dirlist={}
        self.log.add(" ")
        self.log.add(_("Analysis is starting..."))
        self.log.add(" ")
        for x in range(len(items)):
            key, data = items[x]
            dirlist[data[0]]=data[1]
        #print "dirlist",dirlist

        for testdir in dirlist.keys():
            self.cdirdic={}
            self.rdirdic={}
            destdir=dirlist[testdir]
            testdir=os.path.join(testdir,"")
            self.crootdir=testdir
            destdir=os.path.join(destdir,"")
            self.rrootdir=destdir
            #browse local directoy
            os.path.walk(testdir,self._getlocaldir,"")
            #browse remote directory
            os.path.walk(destdir,self._getremotedir,"")
            self.log.add(_("Comparing ")+testdir+_("....with...")+destdir)
            local = (testdir, self.cdirdic, LOCAL_LABEL, self.options.l2r())
            remote = (destdir, self.rdirdic, REMOTE_LABEL, self.options.r2l())
            self.update(res, local, remote)
            self.delete(res, local, remote)
            self.update(res, remote, local)
            self.delete(res, remote, local)

        self.log.add(" ")
        self.log.add(_("Analysis ended."))
        self.log.add(" ")
        return res



class wxFileSyncNotebook(wxNotebook):
    def __init__(self, parent, id):
        wxNotebook.__init__(self, parent, -1)
        #EVT_SIZE(self, self.OnSize)
        self.SetAutoLayout(true)
        self.nb = self
        lc = wxLayoutConstraints()
        lc.top.SameAs(parent, wxTop, 0)
        lc.left.SameAs(parent, wxLeft, 0)
        lc.bottom.SameAs(parent, wxBottom, 0)
        lc.right.SameAs(parent, wxRight, 0)
        self.nb.SetConstraints(lc)
        self.panlog=panellog(self.nb)
        self.panlist=panellist(self.nb,self.panlog)
        self.paninputs=panelinputs(self.nb,self.panlist,self.panlog)
        self.nb.AddPage(self.paninputs, _("Inputs"))
        self.nb.AddPage(self.panlist, _("Transfer list"))
        self.nb.AddPage(self.panlog, _("Log"))

class MyFrame(wxFrame):
    def __init__(self, parent, id, title):
        wxFrame.__init__(self, parent, -1, title,size=wxSize(700,600))
        #EVT_SIZE(self, self.OnSize)
        self.SetAutoLayout(true)
        icon=wxIcon('dirssync.xpm',wxBITMAP_TYPE_XPM)
        self.SetIcon(icon)
        self.nb = wxNotebook(self, -1)
        lc = wxLayoutConstraints()
        lc.top.SameAs(self, wxTop, 0)
        lc.left.SameAs(self, wxLeft, 0)
        lc.bottom.SameAs(self, wxBottom, 0)
        lc.right.SameAs(self, wxRight, 0)
        self.nb.SetConstraints(lc)

        self.panoptions=panoptions(self.nb)
        self.panlog=panellog(self.nb)
        self.panlist=panellist(self.nb,self.panlog)
        self.paninputs=panelinputs(self.nb,self.panlist,self.panlog,self.panoptions)
        self.nb.AddPage(self.paninputs, _("Inputs"))
        self.nb.AddPage(self.panlist, _("Transfer list"))
        self.nb.AddPage(self.panlog, _("Log"))
        self.nb.AddPage(self.panoptions,_("Options"))
        menu_file = wxMenu()
        mnunewID=wxNewId()
        mnuopenID=wxNewId()
        mnusaveID=wxNewId()
        mnuexitID=wxNewId()
        menu_file.Append(mnunewID, _("&New\t")+"Ctrl-n")
        menu_file.Append(mnuopenID, _("&Open\t")+"Ctrl-o")
        menu_file.Append(mnusaveID,_("&Save\t")+"Ctrl-s")
        menu_file.AppendSeparator()
        menu_file.Append(mnuexitID, _("&Exit\t")+"Ctrl-x")
        menubar = wxMenuBar()
        menubar.Append(menu_file, _("&File"))
        menu_help = wxMenu()
        mnuaboutID=wxNewId()
        menu_help.Append(mnuaboutID,_("&About\t")+"Ctrl-h")
        menubar.Append(menu_help,_("&Help"))
        aTable = wxAcceleratorTable([    (wxACCEL_CTRL, ord('N'), mnunewID),
                        (wxACCEL_CTRL, ord('O'), mnuopenID),
                        (wxACCEL_CTRL, ord('S'), mnusaveID),
                        (wxACCEL_CTRL, ord('X'), mnuexitID),
                        (wxACCEL_CTRL, ord('H'), mnuaboutID)])
        self.SetAcceleratorTable(aTable)

        self.SetMenuBar(menubar)
        EVT_MENU(self, mnunewID, self.OnMnuNew)
        EVT_MENU(self, mnuopenID, self.OnMnuOpen)
        EVT_MENU(self, mnusaveID, self.OnMnuSave)
        EVT_MENU(self, mnuexitID, self.OnMnuExit)
        EVT_MENU(self, mnuaboutID, self.OnMnuAbout)

    def OnMnuNew(self,event):
        #panelinputs.listdir.Clear()
        self.paninputs.DeleteAllItems()
        self.panlist.DeleteAllItems()
        self.panlog.DeleteAllItems()

    def OnMnuOpen(self,event):
        global listdirs
        dlg = wxFileDialog(self, _("Choose a file"), ".", "", "*.sync", wxOPEN)
        if dlg.ShowModal() == wxID_OK:
            self.paninputs.DeleteAllItems()
            f=open(dlg.GetPath(),"r")
            listdirs=pickle.load(f)
            #print "OnMnuOpen listdirs",listdirs
            self.paninputs.RefreshListDir(listdirs)
            f.close()

        dlg.Destroy()

    def OnMnuSave(self,event):
        global listdirs
        #print "OnMnuSave listdirs",listdirs
        dlg = wxFileDialog(self, _("Choose a file"), ".", "", "*.sync", wxSAVE | wxOVERWRITE_PROMPT )
        if dlg.ShowModal() == wxID_OK:
            f=open(dlg.GetPath(),"w")
            pickle.dump(listdirs,f)
            f.close()
        dlg.Destroy()


    def OnMnuExit(self,event):
        self.Close()

    def OnMnuAbout(self,event):
        dlg = wxMessageDialog(self, _("Directories Synchronizer is a Python and wxPython application\nwritten by Vincent Delft under the GPL license!\n\nFeel free to propose your ideas to improve this application\nby visiting http://DirsSync.sourceforge.net\nor\nby sending a Email at vincent_delft@yahoo.com"),
              _("About Directories Synchronizer"), wxOK | wxICON_INFORMATION)
              #wxYES_NO | wxNO_DEFAULT | wxCANCEL | wxICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()

    def OnCloseWindow(self, event):
        self.Destroy()


    def OnSize(self, event):
        w,h = self.GetClientSizeTuple()
        #self.nb.SetDimensions(0, 0, w, h)


class panellist(wxPanel):
    def __init__(self,parent,log):
        wxPanel.__init__(self, parent, -1)
        self.log=log
        self.parent=parent
        #First Panel : List
        self.SetAutoLayout(true)
        tID=wxNewId()
        self.list = wxListCtrl(self, tID,size=wxDefaultSize,
        style=wxLC_REPORT|wxSUNKEN_BORDER)
        lc = wxLayoutConstraints()
        lc.top.SameAs(self, wxTop, 10)
        lc.left.SameAs(self, wxLeft, 10)
        lc.bottom.SameAs(self, wxBottom, 50)
        lc.right.SameAs(self, wxRight, 10)
        self.list.SetConstraints(lc)

        self.OKbutID=wxNewId()
        self.OKbut=wxButton(self,self.OKbutID,_("SYNCHRONISE"),wxPoint(200,410))
        EVT_BUTTON(self,self.OKbutID,self.OnSync)
        lc = wxLayoutConstraints()
        lc.bottom.SameAs(self, wxBottom, 15)
        lc.centreX.SameAs(self, wxCentreX)
        lc.height.AsIs()
        lc.width.AsIs()
        self.OKbut.SetConstraints(lc);

        self.list.InsertColumn(0, _("Transfer"))
        self.list.InsertColumn(1,_("Action"))
        self.list.InsertColumn(2, _("From"))
        self.list.InsertColumn(3, _("To"))
        #print "panellist__init__,listfiles",listfiles
        self.localItem = 0
        EVT_LIST_ITEM_SELECTED(self, tID, self.OnItemSelected)
        #EVT_LIST_DELETE_ITEM(self, tID, self.OnItemDelete)
        EVT_LIST_COL_CLICK(self, tID, self.OnColClick)
        EVT_LEFT_DCLICK(self.list, self.OnDoubleClick)
        EVT_RIGHT_DOWN(self.list, self.OnRightDown)

        # for wxMSW
        EVT_COMMAND_RIGHT_CLICK(self.list, tID, self.OnRightClick)

        # for wxGTK
        EVT_RIGHT_UP(self.list, self.OnRightClick)

    def mkdir(self,pathname, dummy):
        if(not os.path.exists(pathname)):
            os.makedirs(pathname)

    def echo(self, src, dest):
        'simple function to test SyncAction'
        str = 'echo %s %s' % (src, dest)
        self.log.add(str)

    def copy(self, src, dest):
        'copy regular source file to dest directory'
        if os.path.isdir(os.path.dirname(dest)): shutil.copy2(src,dest)

    def rmregfile(self, src, dummy):
        'remove a regular file (i.e. not a directory)'
        os.remove(src)
        
    def rmdir(self, pathname, dummy):
        'remove directory pathname'
        os.rmdir(pathname)
        
    def SyncAction(self, rng, actionString, actionFunc):
        for i in rng:
            Vtransfer,VactionT,Vfrom,Vto=listfiles[self.list.GetItemData(i)]
            Vaction=VactionT.split()[0]
            if(Vtransfer!=_("yes") or actionString != Vaction):
                continue #just go to the next one

            self.log.add( Vaction + " " + Vfrom)
            try: actionFunc(Vfrom, Vto)
            except: self.log.add(_("... failed"))

    def OnSync(self,event):
        self.parent.SetSelection(2)
        self.log.add(" ")
        self.log.add(_("Transfer is starting ...."))
        self.log.add(" ")

        rng = range(self.list.GetItemCount())
        self.SyncAction(rng, "mkdir", self.mkdir) #make the directories
        self.SyncAction(rng, "copy", self.copy) #copy over directories

        #remove unneeded directories in reverse order, so that deeper
        #directories as removed before shallower directories
        #rng.reverse()
        self.SyncAction(rng, "rm", self.rmregfile)
        self.SyncAction(rng, "rmdir", self.rmdir)

        #finish off
        self.log.add(" ")
        self.log.add(_("Transfer ended!"))
        self.log.add(" ")
        self.parent.SetSelection(2)


    def UpdateList(self,listf):
        global listfiles
        listfiles=listf
        #items = listfiles.items()
        i=0
        for x in listf:
            (transfer, action, fromm, to) = x
            #data = listfiles[x]
            #self.list.InsertImageStringItem(x, data[0], idx1)
            self.list.InsertStringItem(i, transfer)
            self.list.SetStringItem(i,1, action)
            self.list.SetStringItem(i, 2, fromm)
            if to: self.list.SetStringItem(i, 3, to)
            self.list.SetItemData(i, i)
            i += 1

        self.list.SetColumnWidth(0, wxLIST_AUTOSIZE_USEHEADER)
        self.list.SetColumnWidth(1, wxLIST_AUTOSIZE_USEHEADER)
        self.list.SetColumnWidth(2, wxLIST_AUTOSIZE)
        self.list.SetColumnWidth(3, wxLIST_AUTOSIZE)

        self.list.SetItemState(5, wxLIST_STATE_SELECTED, wxLIST_STATE_SELECTED)
    

        
    def OnItemSelected(self,event):
        self.localItem = event.m_itemIndex
        #print("OnItemSelected: %s\n" % self.list.GetItemText(self.localItem))

    def OnRightDown(self, event):
        self.x = event.GetX()
        self.y = event.GetY()
        #print("x, y = %s\n" % str((self.x, self.y)))
        event.Skip()

    def OnItemDelete(self, event):
        #print("OnItemDelete\n")
        pass

    def ColumnSorter(self, key1, key2):
        #print("ColumnSorter: %d, %d\n" % (key1, key2))
        item1 = listfiles[key1][self.col]
        item2 = listfiles[key2][self.col]
        #print(self.col,item1,item2)
        if item1 == item2:  return 0
        elif item1 < item2: return -1
        else:           return 1

    def OnColClick(self, event):
        #print("OnColClick: %d\n" % event.m_col)
        print (event)
        self.col = event.m_col
        self.list.SortItems(self.ColumnSorter)


    def OnDoubleClick(self, event):
        #print("OnDoubleClick item %s\n" % self.localItem)
        if self.list.GetItemText(self.localItem)==_("yes"):
            self.list.SetItemText(self.localItem,_("no"))
            listfiles[self.localItem]=_("no"),listfiles[self.localItem][1],listfiles[self.localItem][2],listfiles[self.localItem][3]
        else:
            self.list.SetItemText(self.localItem,_("yes"))
            listfiles[self.localItem]=_("yes"),listfiles[self.localItem][1],listfiles[self.localItem][2],listfiles[self.localItem][3]            
        #print "onDoubleClick listfiles",listfiles[self.localItem]


    def OnRightClick(self, event):
        #print("OnRightClick %s\n" % self.list.GetItemText(self.localItem))
        menu = wxMenu()
        tPopupIDSI= 0
        tPopupIDDA=2
        tPopupIDPR= 1
        menu.Append(tPopupIDSI, _("DeleteSelectedItem"))
        menu.Append(tPopupIDDA, _("Delete All Items"))
        menu.Append(tPopupIDPR, _("Print All"))

        EVT_MENU(self, tPopupIDSI, self.OnPopupDeleteItem)
        EVT_MENU(self, tPopupIDDA, self.OnPopupDeleteAllItems)
        EVT_MENU(self, tPopupIDPR, self.OnPopupPrintAll)
        self.PopupMenu(menu, wxPoint(self.x, self.y))
        menu.Destroy()

    def OnPopupPrintAll(self,event):
        global listfiles
        #print "PrintAll", self.list.GetItemCount()
        #print "listfiles",listfiles
        selectedfiles={}
        #print "selected count",self.list.GetSelectedItemCount()
        for i in range(self.list.GetItemCount()):
            #print "ItemText:",self.list.GetItemText(i)
            if self.list.GetSelectedItemCount()<=1:
                if self.list.GetItemText(i)==_("yes"):
                    selectedfiles[i]= listfiles[self.list.GetItemData(i)]
            elif self.list.GetItemState(i,wxLIST_MASK_STATE ):
                if self.list.GetItemText(i)==_("yes"):
                    selectedfiles[i]= listfiles[self.list.GetItemData(i)]

        #print selectedfiles.sort()

    def OnPopupDeleteItem(self, event):
        self.list.DeleteItem(self.localItem)

    def OnPopupDeleteAllItems(self, event):
        self.DeleteAllItems()

    def DeleteAllItems(self):
        global listfiles
        self.list.DeleteAllItems()
        listfiles={}


class panellog(wxPanel):
    def __init__(self,parent):
        wxPanel.__init__(self, parent, -1)
        self.isEnabled = true
        self.SetAutoLayout(true)
        self.log = wxTextCtrl(self, -1, size=wxDefaultSize,
                              style=wxTE_MULTILINE|wxTE_RICH|wxTE_READONLY)
        lc = wxLayoutConstraints()
        lc.top.SameAs(self, wxTop, 10)
        lc.left.SameAs(self, wxLeft, 10)
        lc.bottom.SameAs(self, wxBottom, 50)
        lc.right.SameAs(self, wxRight, 10)
        self.log.SetConstraints(lc)

        butID=wxNewId()
        but=wxButton(self,butID,_("Clear"))
        EVT_BUTTON(self,butID,self.OnClear)
        lc = wxLayoutConstraints()
        lc.bottom.SameAs(self, wxBottom, 15)
        lc.left.SameAs(self, wxLeft, 15)
        lc.height.AsIs()
        lc.width.AsIs()
        but.SetConstraints(lc);


    def add(self,txt):
        if self.isEnabled:
            self.log.AppendText(txt+ '\n')
            self.log.Update()

    def OnClear(self,event):
        self.DeleteAllItems()


    def DeleteAllItems(self):
        self.log.Clear()
        self.log.SetFocus()

class panelinputs(wxPanel):
    def __init__(self,parent,panlist,panlog,panoptions):
        wxPanel.__init__(self, parent, -1)
        self.SetAutoLayout(true)

        self.panlog=panlog
        self.panlist=panlist
        self.parent=parent
        self.panoptions=panoptions
        self.curstatictxt=wxStaticText(self, -1, LOCAL_LABEL, wxPoint(20, 40))
        self.remstatictxt=wxStaticText(self, -1, REMOTE_LABEL,wxPoint(20, 70))
        self.curtxt= wxTextCtrl(self, -1, "", wxPoint(120, 40),
        wxSize(200,-1),style=wxTE_LEFT )
        self.remtxt= wxTextCtrl(self, -1, "", wxPoint(120, 70),
        wxSize(200,-1),style=wxTE_LEFT )
        self.curbutID=wxNewId()
        self.curbut = wxButton(self, self.curbutID,_("Browse"),wxPoint(350,40))
        self.rembutID=wxNewId()
        self.rembut = wxButton(self, self.rembutID,_("Browse"),wxPoint(350,70))
        EVT_BUTTON(self, self.curbutID, self.selectDir)
        EVT_BUTTON(self, self.rembutID, self.selectDir)
        self.butaddID=wxNewId()
        self.butadd = wxButton(self,self.butaddID,_("Add Job"),wxPoint(100,100))
        EVT_BUTTON(self,self.butaddID,self.AddDirToList)

        self.listdirID=wxNewId()
        self.listdir = wxListCtrl(self, self.listdirID,
        wxPoint(10,130), wxDefaultSize,wxLC_REPORT|wxSUNKEN_BORDER)
        lc = wxLayoutConstraints()
        lc.top.SameAs(self, wxTop, 130)
        lc.left.SameAs(self, wxLeft, 10)
        lc.bottom.SameAs(self, wxBottom, 10)
        lc.right.SameAs(self, wxRight, 10)
        self.listdir.SetConstraints(lc)

        self.listdir.InsertColumn(0, LOCAL_LABEL)
        self.listdir.InsertColumn(1, REMOTE_LABEL)
        self.listdir.SetColumnWidth(0, wxLIST_AUTOSIZE_USEHEADER)
        self.listdir.SetColumnWidth(1, wxLIST_AUTOSIZE_USEHEADER)

        self.chkbutID=wxNewId()
        self.chkbut=wxButton(self,self.chkbutID,_("Next>>"),wxPoint(450,50),wxSize(-1,60))

        logo=wxImage('DirsSync.png',wxBITMAP_TYPE_PNG).ConvertToBitmap()
        wxStaticBitmap(self,-1,logo,wxPoint(550,20))

        EVT_BUTTON(self, self.chkbutID, self.OnCheck)
        EVT_LIST_ITEM_SELECTED(self, self.listdirID, self.OnItemSelected)
        #EVT_LIST_DELETE_ITEM(self, self.listdirID, self.OnItemDelete)
        EVT_LIST_COL_CLICK(self, self.listdirID, self.OnColClick)
        EVT_RIGHT_DOWN(self.listdir, self.OnRightDown)
        # for wxMSW
        EVT_COMMAND_RIGHT_CLICK(self.listdir, self.listdirID, self.OnRightClick)

        # for wxGTK
        EVT_RIGHT_UP(self.listdir, self.OnRightClick)

    def DirFilterCallback(self,list):       # virtual
        #print list
        return list


    def OnCheck(self,event):
        if self.listdir.GetItemCount() == 0:
            self.AddDirToList(event)
            if self.listdir.GetItemCount() == 0:
                return
        #print "OnCheckButton: listdirs",listdirs
        #print "GetSelection",self.parent.GetSelection()
        self.parent.SetSelection(2)
        t=transfer(self.panlog,self.panoptions)
        res=t.transfer(listdirs)
        if self.DirFilterCallback <> None:
            res = self.DirFilterCallback(res)
        #print "res",res
        self.panlist.DeleteAllItems()
        self.panlist.UpdateList(res)
        self.parent.SetSelection(1)

    def AddDirToList(self,event):
        x=self.listdir.GetItemCount()
        #print "x",x,self.curtxt.GetValue(),self.remtxt.GetValue()
        if self.curtxt.GetValue()=="" or self.remtxt.GetValue()=="":
            dlg = wxMessageDialog(self, _("You must specify the local and remote directory."),_("Input Error"), wxOK | wxICON_EXCLAMATION )
            #wxYES_NO | wxNO_DEFAULT | wxCANCEL | wxICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()
        else:
            self.listdir.InsertStringItem(x,self.curtxt.GetValue() )
            self.listdir.SetStringItem(x,1, self.remtxt.GetValue() )
            self.listdir.SetItemData(x, x)
            listdirs[x]=(self.curtxt.GetValue(),self.remtxt.GetValue())
            self.listdir.SetColumnWidth(0, wxLIST_AUTOSIZE_USEHEADER)
            self.listdir.SetColumnWidth(1, wxLIST_AUTOSIZE_USEHEADER)
            self.curtxt.Clear()
            self.remtxt.Clear()

    def RefreshListDir(self,listdirs):
        items = listdirs.items()
        #print "RefrshListDir items",items
        for x in range(len(items)):
            data = listdirs[x]
            #print "x",x,data[0],data[1]
            self.listdir.InsertStringItem(x,  data[0])
            self.listdir.SetStringItem(x, 1, data[1])
            self.listdir.SetItemData(x, x)

        self.listdir.SetColumnWidth(0, wxLIST_AUTOSIZE_USEHEADER)
        self.listdir.SetColumnWidth(1, wxLIST_AUTOSIZE_USEHEADER)



    def selectDir(self,event):
        dlg = wxDirDialog(self)
        if dlg.ShowModal() == wxID_OK:
            #print('You selected: %s\n' % dlg.GetPath())
            if event.GetId()==self.curbutID:
                self.curtxt.SetValue(dlg.GetPath())
            #Avoid stupid input from users.
            if event.GetId()==self.rembutID:
                if self.curtxt.GetValue() == dlg.GetPath():
                    dlgW = wxMessageDialog(self,_("The local and remote directories are the same"),_("Input mismatch"),wxOK | wxICON_EXCLAMATION)
                    dlgW.ShowModal()
                    dlgW.Destroy()
                else:
                    self.remtxt.SetValue(dlg.GetPath())
        dlg.Destroy()

    def OnItemSelected(self,event):
        self.localItem = event.m_itemIndex

    def OnRightDown(self, event):
        self.x = event.GetX()+10
        self.y = event.GetY()+130
        #print("x, y = %s\n" % str((self.x, self.y)))
        event.Skip()

    def OnItemDelete(self, event):
        #print("OnItemDelete\n")
        pass

    def ColumnSorter(self, key1, key2):
        #print("ColumnSorter: %d, %d\n" % (key1, key2))
        item1 = listdirs[key1][self.col]
        item2 = listdirs[key2][self.col]
        if item1 == item2:  return 0
        elif item1 < item2: return -1
        else:           return 1

    def OnColClick(self, event):
        #print("OnColClick: %d\n" % event.m_col)
        self.col = event.m_col
        self.listdir.SortItems(self.ColumnSorter)


    def OnRightClick(self, event):
        #print("OnRightClick",self.localItem, self.listdir.GetItemText(self.localItem)),listdirs[self.localItem]
        menu = wxMenu()
        tPopupIDSI= 0
        menu.Append(tPopupIDSI, _("DeleteSelectedItem"))
        EVT_MENU(self, tPopupIDSI, self.OnPopupDeleteItem)
        self.PopupMenu(menu, wxPoint(self.x, self.y))
        menu.Destroy()

    def OnPopupDeleteItem(self, event):
        global listdirs
        max=self.listdir.GetItemCount()-1
        for x in range(self.localItem,max):
            listdirs[x]=listdirs[x+1]
        self.listdir.DeleteItem(self.localItem)
        ll=listdirs.keys()
        ll.sort()
        ll.reverse()
        max=ll[0]
        del listdirs[max]
        #print "listdirs",listdirs

    def DeleteAllItems(self):
        global listdirs
        listdirs={}
        self.listdir.DeleteAllItems()



class panoptions(wxPanel):
    def __init__(self,parent):
        wxPanel.__init__(self, parent, -1)
        self.SetAutoLayout(true)
        self.comparison=file_criteria()
        self.comp_dict={}
        text_to_display=[]

        #file comparison method
        for elem in self.comparison.__ALL__:
            method=eval('self.comparison.%s()' % elem)
            txt=method.msg
            self.comp_dict[txt]=eval('method.comp')
            text_to_display.append(txt)
        wxStaticText(self, -1, _("File Comparison method :"),wxPoint(20, 10))
        cID = wxNewId()
        cb1 = wxChoice(self, cID,   wxPoint(40, 30), wxDefaultSize,text_to_display)
        cb1.SetSelection(0)
        EVT_CHOICE(self,cID, self.ComparisonSelect)
        self.comparison_selected=eval('self.comparison.%s().comp' % self.comparison.default)

        #LOCAL to REMOTE checkbox
        str = _("Local to Remote")
        basex = 20
        basey = 60
        self.cb2 = wxCheckBox(self, cID+1, str, wxPoint(basex, basey),
        wxSize(200, 20), wxNO_BORDER)
        self.cb2.SetValue(True)

        #REMOTE to LOCAL checkbox
        str = _("Remote to Local")
        self.cb3 = wxCheckBox(self, cID+2, str, wxPoint(basex, basey + 20),
        wxSize(200, 20), wxNO_BORDER)
        self.cb3.SetValue(True)

        #Allow deletion
        str = _("Delete (one-way)")
        self.cb4 = wxCheckBox(self, cID+3, str, wxPoint(basex, basey + 40),
        wxSize(200, 20), wxNO_BORDER)
        self.cb4.SetValue(False)

    def ComparisonSelect(self,event):
        "store the selected comparison method"
        self.comparison_selected=self.comp_dict[event.GetString()]
        #print "COMPARISON",self.comparison_selected

    def l2r(self):
        'Copy from local to remote?'
        return self.cb2.GetValue()

    def r2l(self):
        'Copy from remote to local?'
        return self.cb3.GetValue()

    def delete(self):
        'Allow deletion?'
        return self.cb4.GetValue()





if __name__ == "__main__":
    _psyco.importPsycoIfPossible()
    class MyApp(wxApp):
        def OnInit(self):
            frame=MyFrame(None,-1,_("Directories Synchronizer"))
            frame.Show(true)
            self.SetTopWindow(frame)
            return true

    app=MyApp(0)
    app.MainLoop()


# vim:ts=4:expandtab:softtabstop=4:shiftwidth=4:foldmethod=indent
