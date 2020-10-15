#Author: Vincent DELFT
#
# 09/2000 : first realase 0.1
# 10/2000 : menu "file->new","file->open","file->save" added
# 11/2001 : add new functionnalities proposed by Maharajan 
# 01/2003 : better error handling
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
#
#        

from wxPython.wx import *
from wxPython.lib.filebrowsebutton import FileBrowseButton
import pickle
import os
import os.path
import string
import shutil

global listdirs,listfiles
listfiles = {}
listdirs={}

class transfer:
	def __init__(self,log):
		self.log=log
		self.cdirdic={}
		self.rdirdic={}
		self.crootdir=""
		self.rrootdir=""
		
	def getlocaldir(self,arg,cdir,cnames):
		#print "local directory: ",cdir
		self.log.add("Exploring local "+cdir)
		relatifpath=string.replace(cdir,self.crootdir,"")
		for cname in cnames:
				self.cdirdic[os.path.join(relatifpath,cname)]=os.path.getmtime(os.path.join(cdir,cname))
			
	def getremotedir(self,arg,rdir,rnames):
		#print "remote directory: ",rdir
		self.log.add("Exploring remote "+rdir)
		relatifpath=string.replace(rdir,self.rrootdir,"")
		for rname in rnames:
				self.rdirdic[os.path.join(relatifpath,rname)]=os.path.getmtime(os.path.join(rdir,rname))
			
	
	def transfer(self,listdirs):
		res={}
		i=0
		items=listdirs.items()
		dirlist={}
		self.log.add(" ")
		self.log.add("Analysis is starting...")
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
			#print "local dir : ",self.crootdir
			#print "remote dir : ",self.rrootdir
				
			os.path.walk(testdir,self.getlocaldir,"")
			os.path.walk(destdir,self.getremotedir,"")
			
			#print self.cdirdic
			#print self.rdirdic
			
			self.log.add("Comparing "+testdir+"....with..."+destdir)
			#check local to update remote
			
			for elem in self.cdirdic.keys():
				if self.rdirdic.has_key(elem):
					if self.cdirdic[elem]>self.rdirdic[elem] and os.path.isfile(os.path.join(self.crootdir,elem)):
						#text="Copy to remote the file "+elem
						#res=raw_input(text)
						#if res=="y":
						res[i]="yes","copy to remote",os.path.join(self.crootdir,elem),os.path.join(self.rrootdir,elem)
						i=i+1
							
				else:
					if os.path.isdir(os.path.join(self.crootdir,elem)):
						#text="Create to remote the directory " + elem
						#res=raw_input(text)
						#if res=="y":
						res[i]="yes","mkdir on remote",os.path.join(self.rrootdir,elem),""
						i=i+1
					if os.path.isfile(os.path.join(self.crootdir,elem)):
						#text="Create to remote the file " + elem
						#res=raw_input(text)
						#if res=="y":
						res[i]="yes","copy to remote",os.path.join(self.crootdir,elem),os.path.join(self.rrootdir,elem)
						i=i+1
					
			#check remote to update local
			for elem in self.rdirdic.keys():
				#print "check",elem,cdirdic.has_key(elem)
				if self.cdirdic.has_key(elem):
					if self.rdirdic[elem]>self.cdirdic[elem] and os.path.isfile(os.path.join(self.crootdir,elem)):
						#text="Copy to local the file "+elem
						#res=raw_input(text)
						#if res=="y":
						res[i]="yes","copy to local",os.path.join(self.rrootdir,elem),os.path.join(self.crootdir,elem)
						i=i+1
							
				else:
					if os.path.isdir(os.path.join(self.rrootdir,elem)):
						#text="Create to local the directory " + elem
						#res=raw_input(text)
						#if res=="y":
						res[i]="yes","mkdir on local",os.path.join(self.crootdir,elem),""
						i=i+1
					if os.path.isfile(os.path.join(self.rrootdir,elem)):
						#text="Create to local the file " + elem
						#res=raw_input(text)
						#if res=="y":
						res[i]="yes","copy to local",os.path.join(self.rrootdir,elem),os.path.join(self.crootdir,elem)
						i=i+1
		self.log.add(" ")
		self.log.add("Analysis ended.")
		self.log.add(" ")
		
		return res
			
		

class MyFrame(wxFrame):
	def __init__(self, parent, id, title):
		wxFrame.__init__(self, parent, -1, title,size=wxSize(700,600))
		#EVT_SIZE(self, self.OnSize)
		self.SetAutoLayout(true)

		self.nb = wxNotebook(self, -1) 
	 	lc = wxLayoutConstraints()
        	lc.top.SameAs(self, wxTop, 0)
	        lc.left.SameAs(self, wxLeft, 0)
	        lc.bottom.SameAs(self, wxBottom, 0)
	        lc.right.SameAs(self, wxRight, 0)
	        self.nb.SetConstraints(lc)
                
		self.panlog=panellog(self.nb)
		self.panlist=panellist(self.nb,self.panlog)
                self.paninputs=panelinputs(self.nb,self.panlist,self.panlog)
                self.nb.AddPage(self.paninputs, "Inputs")
                self.nb.AddPage(self.panlist, "Transfer list")
                self.nb.AddPage(self.panlog, "Log")
                menu_file = wxMenu()
                mnunewID=NewId()
                mnuopenID=NewId()
                mnusaveID=NewId()
                mnuexitID=NewId()
                menu_file.Append(mnunewID, "New")
                menu_file.Append(mnuopenID, "Open")
                menu_file.Append(mnusaveID,"Save")
                menu_file.AppendSeparator()
                menu_file.Append(mnuexitID, "Exit")
                menubar = wxMenuBar()
                menubar.Append(menu_file, "File")
		menu_help = wxMenu()
		mnuaboutID=NewId()
		menu_help.Append(mnuaboutID,"About")
		menubar.Append(menu_help,"Help")
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
                dlg = wxFileDialog(self, "Choose a file", ".", "", "*.*", wxOPEN)
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
                dlg = wxFileDialog(self, "Choose a file", ".", "", "*.*", wxSAVE | wxOVERWRITE_PROMPT )
                if dlg.ShowModal() == wxID_OK:
                        f=open(dlg.GetPath(),"w")
                        pickle.dump(listdirs,f)
                        f.close()
                dlg.Destroy()

                
        def OnMnuExit(self,event):
                self.Close()

        def OnMnuAbout(self,event):
		dlg = wxMessageDialog(self, 'Directories Synchronizer is a Python and wxPython application\nwritten by Vincent Delft under the GPL license!\n\nFeel free to propose your ideas to improve this application\nby visiting http://DirsSync.sourceforge.net\nor\nby sending a Email at vincent_delft@yahoo.com',
                          'About Directories Synchronizer', wxOK | wxICON_INFORMATION)
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
		tID=NewId()
		self.list = wxListCtrl(self, tID,size=wxDefaultSize, style=wxLC_REPORT|wxSUNKEN_BORDER)
	 	lc = wxLayoutConstraints()
        	lc.top.SameAs(self, wxTop, 10)
	        lc.left.SameAs(self, wxLeft, 10)
	        lc.bottom.SameAs(self, wxBottom, 50)
	        lc.right.SameAs(self, wxRight, 10)
	        self.list.SetConstraints(lc)
  		
		self.OKbutID=NewId()
		self.OKbut=wxButton(self,self.OKbutID,"SYNCHRONISE",wxPoint(200,410))
		EVT_BUTTON(self,self.OKbutID,self.OnCOPY)
	        lc = wxLayoutConstraints()
		lc.bottom.SameAs(self, wxBottom, 15)
		lc.centreX.SameAs(self, wxCentreX)
	        lc.height.AsIs()
	        lc.width.AsIs()
	        self.OKbut.SetConstraints(lc);

                self.list.InsertColumn(0, "Transfer")
                self.list.InsertColumn(1,"Action")
		self.list.InsertColumn(2, "From")
		self.list.InsertColumn(3, "To")
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
	def mkdir(self,pathname):
		#correction proposed by Maharajan to avoid crash when creating new directory tree
		if os.path.isdir(pathname):
			return 0
		dirname=os.path.dirname(pathname)
		if dirname!="" and dirname!=pathname:
			self.mkdir(dirname)
			try:
		    		os.mkdir(pathname)
			except:
				self.log.add("ERROR : Cannot create the directory %s" % pathname)
				return 1 
			else:
				return 0
		else:
			self.log.add("ERROR : Cannot create the directory called %s" % pathname)
			return 1

	def OnCOPY(self,event):
                #print "PrintOnCOPY", self.list.GetItemCount()
                #print "listfiles",listfiles
                #print "selected count",self.list.GetSelectedItemCount()
		self.parent.SetSelection(2)
		self.log.add(" ")
		self.log.add("Transfer is starting ....")
		self.log.add(" ")
                #firstly we create some directory
                for i in range(self.list.GetItemCount()):
                        #print "ItemText:",i,self.list.GetItemText(i),self.list.GetItemState(i,wxLIST_STATE_SELECTED )
                        Vtransfer,VactionT,Vfrom,Vto=listfiles[self.list.GetItemData(i)]
                        Vaction,brol,brol=string.split(VactionT)
                        if self.list.GetSelectedItemCount()<=1:
                                if ((Vtransfer=="yes") and (Vaction=="mkdir")):
						result=self.mkdir(Vfrom)
						if result==0:
							self.log.add("Create Dir "+Vfrom)
						else:
							self.log.add("Process abended")
						#print "1mkdir",result,Vfrom
						
                        elif self.list.GetItemState(i,wxLIST_STATE_SELECTED ): 
                                if ((Vtransfer=="yes") and (Vaction=="mkdir")):
                                                #print "transfer",Vtransfer,"action",Vaction,"from",Vfrom,"to",Vto
						result=self.mkdir(Vfrom)
						if result==0:
							self.log.add("Create Dir "+Vfrom)
						else:
							self.log.add("Process abended")
						#print "2mkdir",result,Vfrom
						
                                                
                #secondly we copy the files
                for i in range(self.list.GetItemCount()):
                        #print "ItemText:",i,self.list.GetItemText(i),self.list.GetItemState(i,wxLIST_STATE_SELECTED )
                        Vtransfer,VactionT,Vfrom,Vto=listfiles[self.list.GetItemData(i)]
                        Vaction,brol,brol=string.split(VactionT)
			#print "transfer",Vtransfer,"action",Vaction,"from",Vfrom,"to",Vto,"EEEE",os.path.dirname(Vto),os.path.isdir(os.path.dirname(Vto))
                        if self.list.GetSelectedItemCount()<=1:
                                if Vtransfer=="yes" and Vaction=="copy" and os.path.isdir(os.path.dirname(Vto)):
						try:
							shutil.copy2(Vfrom,Vto)
						except:
							self.log.add("ERROR : Cannot copy the file %s to %s" % (Vfrom,Vto))
						else:
							self.log.add("Copy file "+Vfrom+", "+Vto)
						#print "copy ",Vfrom,Vto
                        elif self.list.GetItemState(i,wxLIST_STATE_SELECTED ): 
                                if Vtransfer=="yes" and Vaction=="copy" and os.path.isdir(os.path.dirname(Vto)):
						try:
							shutil.copy2(Vfrom,Vto)
						except:
							self.log.add("ERROR : Cannot copy the file %s to %s" % (Vfrom,Vto))
						else:
							self.log.add("Copy file "+Vfrom+", "+Vto)
						#print "copy ",Vfrom,Vto
                                                
		self.parent.SetSelection(2)
		

	def UpdateList(self,listf):
		global listfiles
		listfiles=listf
		items = listfiles.items()
		for x in range(len(items)):
			data = listfiles[x]
			#self.list.InsertImageStringItem(x, data[0], idx1)
			self.list.InsertStringItem(x, data[0])
			self.list.SetStringItem(x,1, data[1])
			self.list.SetStringItem(x, 2, data[2])
			if data[3]: self.list.SetStringItem(x, 3, data[3])
			self.list.SetItemData(x, x)

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
		print("ColumnSorter: %d, %d\n" % (key1, key2))
		item1 = listfiles[key1][self.col]
		item2 = listfiles[key2][self.col]
		print(self.col,item1,item2)
		if item1 == item2:  return 0
                elif item1 < item2: return -1
                else:               return 1

	def OnColClick(self, event):
		print("OnColClick: %d\n" % event.m_col)
		print (event)
		self.col = event.m_col
		self.list.SortItems(self.ColumnSorter)


        def OnDoubleClick(self, event):
                #print("OnDoubleClick item %s\n" % self.localItem)
                if self.list.GetItemText(self.localItem)=="yes":
                        self.list.SetItemText(self.localItem,"no")
                        listfiles[self.localItem]="no",listfiles[self.localItem][1],listfiles[self.localItem][2],listfiles[self.localItem][3]
                else:
                        self.list.SetItemText(self.localItem,"yes")
                        listfiles[self.localItem]="yes",listfiles[self.localItem][1],listfiles[self.localItem][2],listfiles[self.localItem][3]                        
                #print "onDoubleClick listfiles",listfiles[self.localItem]


        def OnRightClick(self, event):
                #print("OnRightClick %s\n" % self.list.GetItemText(self.localItem))
                menu = wxMenu()
                tPopupIDSI= 0
                tPopupIDDA=2
                tPopupIDPR= 1
                menu.Append(tPopupIDSI, "DeleteSelectedItem")
                menu.Append(tPopupIDDA, "Delete All Items")
                menu.Append(tPopupIDPR, "Print All")
                
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
                                if self.list.GetItemText(i)=="yes":
                                        selectedfiles[i]= listfiles[self.list.GetItemData(i)]                
                        elif self.list.GetItemState(i,wxLIST_MASK_STATE ): 
                                if self.list.GetItemText(i)=="yes":
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


class panelinputs(wxPanel):
        def __init__(self,parent,panlist,log):
                wxPanel.__init__(self, parent, -1)
		self.SetAutoLayout(true)
		
		self.log=log
                self.panlist=panlist
		self.parent=parent
		self.curstatictxt=wxStaticText(self, -1, "Local directory :",wxPoint(20, 40))
		self.remstatictxt=wxStaticText(self, -1, "Remote directory",wxPoint(20, 70))
		self.curtxt= wxTextCtrl(self, -1, "", wxPoint(120, 40), wxSize(200,-1),style=wxTE_READONLY)
		self.remtxt= wxTextCtrl(self, -1, "", wxPoint(120, 70), wxSize(200,-1),style=wxTE_READONLY)
		self.curbutID=NewId()
		self.curbut = wxButton(self, self.curbutID,"Browse",wxPoint(350,40))
		self.rembutID=NewId()
		self.rembut = wxButton(self, self.rembutID,"Browse",wxPoint(350,70))
		EVT_BUTTON(self, self.curbutID, self.selectDir)
		EVT_BUTTON(self, self.rembutID, self.selectDir)
		self.butaddID=NewId()
		self.butadd = wxButton(self,self.butaddID,"Add",wxPoint(100,100))
		EVT_BUTTON(self,self.butaddID,self.AddDirToList)
		
		self.listdirID=NewId()
		self.listdir = wxListCtrl(self, self.listdirID, wxPoint(10,130), wxDefaultSize,wxLC_REPORT|wxSUNKEN_BORDER)
	 	lc = wxLayoutConstraints()
        	lc.top.SameAs(self, wxTop, 130)
	        lc.left.SameAs(self, wxLeft, 10)
	        lc.bottom.SameAs(self, wxBottom, 10)
	        lc.right.SameAs(self, wxRight, 10)
	        self.listdir.SetConstraints(lc)
        
       		self.listdir.InsertColumn(0, "Local")
		self.listdir.InsertColumn(1, "Remote")
		self.listdir.SetColumnWidth(0, wxLIST_AUTOSIZE_USEHEADER)
		self.listdir.SetColumnWidth(1, wxLIST_AUTOSIZE_USEHEADER)
		
		self.chkbutID=NewId()
		self.chkbut=wxButton(self,self.chkbutID,"Check Folder",wxPoint(450,50),wxSize(-1,60))

		EVT_BUTTON(self, self.chkbutID, self.OnCheck)
		EVT_LIST_ITEM_SELECTED(self, self.listdirID, self.OnItemSelected)
		#EVT_LIST_DELETE_ITEM(self, self.listdirID, self.OnItemDelete)
		EVT_LIST_COL_CLICK(self, self.listdirID, self.OnColClick)
		EVT_RIGHT_DOWN(self.listdir, self.OnRightDown)
		# for wxMSW
		EVT_COMMAND_RIGHT_CLICK(self.listdir, self.listdirID, self.OnRightClick)

		# for wxGTK
		EVT_RIGHT_UP(self.listdir, self.OnRightClick)


	def OnCheck(self,event):
		#print "OnCheckButton: listdirs",listdirs
		#print "GetSelection",self.parent.GetSelection()
		self.parent.SetSelection(2)
		t=transfer(self.log)
		res=t.transfer(listdirs)
		#print "res",res
		self.panlist.DeleteAllItems()
		self.panlist.UpdateList(res)
		self.parent.SetSelection(1)

	def AddDirToList(self,event):
		x=self.listdir.GetItemCount()
		#print "x",x,self.curtxt.GetValue(),self.remtxt.GetValue()
		if self.curtxt.GetValue()=="" or self.remtxt.GetValue()=="":
			dlg = wxMessageDialog(self, "You must specify the local and remote directory","Input Error", wxOK | wxICON_EXCLAMATION )
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
					dlgW = wxMessageDialog(self,"The local and remote directories are the same","Input mismatch",wxOK | wxICON_EXCLAMATION)
					dlgW.ShowModal()
					dlgW.Destroy()
				else:
					self.remtxt.SetValue(dlg.GetPath())
                dlg.Destroy()

	def OnItemSelected(self,event):
		self.localItem = event.m_itemIndex
		#print("OnItemSelected: %s\n" % self.listdir.GetItemText(self.localItem))

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
                else:               return 1

	def OnColClick(self, event):
		#print("OnColClick: %d\n" % event.m_col)
		self.col = event.m_col
		self.listdir.SortItems(self.ColumnSorter)


        def OnRightClick(self, event):
                #print("OnRightClick",self.localItem, self.listdir.GetItemText(self.localItem)),listdirs[self.localItem]
                menu = wxMenu()
                tPopupIDSI= 0
                menu.Append(tPopupIDSI, "DeleteSelectedItem")
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
                           
class panellog(wxPanel):
        def __init__(self,parent):
                wxPanel.__init__(self, parent, -1)
		self.SetAutoLayout(true)
		self.log= wxListCtrl(self, -1, size=wxDefaultSize,style=wxLC_REPORT)
                self.log.InsertColumn(0,"items")
	 	lc = wxLayoutConstraints()
        	lc.top.SameAs(self, wxTop, 10)
	        lc.left.SameAs(self, wxLeft, 10)
	        lc.bottom.SameAs(self, wxBottom, 50)
	        lc.right.SameAs(self, wxRight, 10)
	        self.log.SetConstraints(lc)
		
		butID=NewId()
		but=wxButton(self,butID,"Clear")
		EVT_BUTTON(self,butID,self.OnClear)
	        lc = wxLayoutConstraints()
		lc.bottom.SameAs(self, wxBottom, 15)
		lc.left.SameAs(self, wxLeft, 15)
	        lc.height.AsIs()
	        lc.width.AsIs()
	        but.SetConstraints(lc);


	def add(self,txt):
		pos=self.log.GetItemCount()
		self.log.InsertStringItem(pos,txt)
		self.log.SetColumnWidth(0, wxLIST_AUTOSIZE)
		self.log.EnsureVisible(pos)
	def OnClear(self,event):
		#ClearAll will not allow subsequent operations
		#proposition by Maharajan
		#self.log.ClearAll()
		self.log.DeleteAllItems()
        def DeleteAllItems(self):
                self.log.DeleteAllItems()
                        

class MyApp(wxApp):
	def OnInit(self):
		frame=MyFrame(None,-1,"Directories Synchronizer")
		frame.Show(true)
		self.SetTopWindow(frame)
		return true
		
app=MyApp(0)
app.MainLoop()
