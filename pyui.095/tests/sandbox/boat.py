# PyUI
# Copyright (C) 2001-2002 Sean C. Riley
# 
# This library is free software; you can redistribute it and/or
# modify it under the terms of version 2.1 of the GNU Lesser General Public
# License as published by the Free Software Foundation.
# 
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

""" This module is for interacting with data sources using Twisted Enterprise -
a object-relational mapping interface for python that uses the Twisted
network/server framework.

Info on Twisted can be found at http://www.twistedmatrix.com. This code worked
with Twisted verion 0.99r4.

An example for using these Boat classes (Row Boat - get it?) can
be found in pyui/tests/boatTest.py
"""

import time
import pyui
import traceback

from twisted.enterprise import adbapi, row, sqlreflector, util
from twisted.enterprise.dbcred import *

class BoatChildrenFrame(pyui.widgets.Frame):
    """This is a frame that shows the children of a particular row for a relationship.
    It uses a BoatSheet internally
    """
    def __init__(self, x, y, reflector, parentRow, relationship, dataIn=None):
        self.reflector = reflector
        self.relationship = relationship
        self.parentRow = parentRow
        pyui.widgets.Frame.__init__(self, x, y, 400,180, "Rows from %s for %s" % (relationship.childRowClass.rowTableName, parentRow.getKeyTuple()) )
        self.setLayout(pyui.layouts.GridLayoutManager(1,1))
        where = self.reflector.buildWhereClause(relationship, parentRow)
        self.sheet = BoatSheet(self.reflector, relationship.childRowClass, dataIn, where)
        self.replacePanel(self.sheet)

class BoatFormFrame(pyui.widgets.Frame):
    """This is a frame that displays all of the data for a row in a form
    and allows the user to edit the data. Uses a BoatFormFrame internally.
    """
    def __init__(self, reflector,rowClass, rowNum, sheet):
        self.reflector = reflector
        self.rowClass = rowClass
        self.rowNum = rowNum
        self.sheet = sheet
        l = len(rowClass.rowColumns)
        pyui.widgets.Frame.__init__(self, 50,50,400,22*(l+2), "Row %s" % rowClass)
        
        self.setLayout(pyui.layouts.TableLayoutManager(2,l+1))
        self.form = BoatFormPanel(rowClass)
        self.updateButton = pyui.widgets.Button("Save", self.onButton)
        self.closeButton = pyui.widgets.Button("Cancel", self.onCloseButton)
        self.addChild(self.form, (0,0,2,l))
        self.addChild(self.updateButton, (1,l,1,1) )
        self.addChild(self.closeButton, (0,l,1,1) )        
        self.pack()

    def populate(self, row):
        self.form.populate(row)
        
    def onButton(self, but):
        self.form.process()
        self.reflector.updateRow(self.form.object).addCallback(self.onUpdate)

    def onUpdate(self, but):
        print "form row updated."
        self.sheet.updateRowAt(self.form.object, self.rowNum)
        self.destroy()

    def onCloseButton(self, but):
        self.destroy()    
        

class BoatFormPanel(pyui.widgets.FormPanel):
    """The actual form panel used by the BoatFormFrame.
    """
    def __init__(self, rowClass):
        self.rowClass = rowClass
        fieldList = []
        for name, ctype in rowClass.rowColumns:
            if util.dbTypeMap[ctype] == util.NOQUOTE:
                fieldType = "int"
            else:
                fieldType = "string"
            if (name,ctype) in rowClass.rowKeyColumns:
                fieldType = "label"
            fieldList.append( (fieldType, name, "%s:"%name, 1, 24) )
            
        pyui.widgets.FormPanel.__init__(self,  fieldList )


class BoatNewFormFrame(pyui.widgets.Frame):
    """Frame for Form for entering a new row
    """
    def __init__(self, reflector,rowClass, sheet):
        self.reflector = reflector
        self.rowClass = rowClass
        self.sheet = sheet
        l = len(rowClass.rowColumns)
        pyui.widgets.Frame.__init__(self, 50,50,400,22*(l+2), "Row %s" % rowClass)
        
        self.setLayout(pyui.layouts.TableLayoutManager(2,l+1))
        self.form = BoatNewFormPanel(rowClass)
        self.updateButton = pyui.widgets.Button("Create", self.onButton)
        self.closeButton = pyui.widgets.Button("Cancel", self.onCloseButton)
        self.addChild(self.form, (0,0,2,l))
        self.addChild(self.updateButton, (1,l,1,1) )
        self.addChild(self.closeButton, (0,l,1,1) )        
        self.pack()

    def populate(self, row):
        self.form.populate(row)
        
    def onButton(self, but):
        self.form.process()
        self.reflector.insertRow(self.form.object).addCallbacks(self.onInsert, self.onError)

    def onInsert(self, but):
        print "form row inserted.", but
        self.sheet.insertRowAt(self.form.object)
        self.destroy()

    def onError(self, err):
        print "Error on insert:", err
        
    def onCloseButton(self, but):
        self.destroy()    
        

class BoatNewFormPanel(pyui.widgets.FormPanel):
    """The actual form panel used by the BoatNewFormFrame.
    """
    def __init__(self, rowClass):
        self.rowClass = rowClass
        fieldList = []
        for name, ctype in rowClass.rowColumns:
            if util.dbTypeMap[ctype] == util.NOQUOTE:
                fieldType = "int"
            else:
                fieldType = "string"
            fieldList.append( (fieldType, name, "%s:"%name, 1, 24) )
            
        pyui.widgets.FormPanel.__init__(self,  fieldList )

        newRow = self.rowClass()
        self.populate(newRow)

    def process_string(self, formWidget, fieldName):
        """if this is a key column, use the special assignKeyAttr method.
        """
        found=0
        for name, ctype in self.rowClass.rowKeyColumns:
            if name == fieldName:
                if util.dbTypeMap[ctype] == util.NOQUOTE:                
                    self.object.assignKeyAttr(fieldName, formWidget.text)
                else:
                    self.object.assignKeyAttr(fieldName, formWidget.text)
                found=1
        if not found:
            pyui.widgets.FormPanel.process_string(self, formWidget, fieldName)
    
class BoatSheet(pyui.sheet.Sheet):
    """A panel that displays a set of rows for a particular rowClass/table.
    It has resizable columns and rows, and allows in-place editing of the
    data which will be updated immediately back into the reflector.

    Has a menu that allows other operationson the rows.
    """
    def __init__(self, reflector, rowClass, dataIn=None, whereIn=None):
        self.reflector = reflector
        self.rowClass = rowClass
        self.dataIn = dataIn
        pyui.sheet.Sheet.__init__(self, self.onChange)

        # setup column titles
        i=0
        for name, ctype in rowClass.rowColumns:
           self.setColumnTitle(i+1, name)
           i=i+1
           if (name, ctype) in rowClass.rowKeyColumns:
               self.setColumnReadOnly(i)

        # setup menu
        actionMenu = pyui.widgets.MenuPopup()
        item = actionMenu.addItem("Open...", self.onEdit)
        item = actionMenu.addItem("New...", self.onNew)
        item = actionMenu.addItem("Delete...", self.onDelete)        
        info = self.reflector.getTableInfo(rowClass)
        for relationship in info.relationships:
            item = actionMenu.addItem("Show Children for %s..." % relationship.childRowClass.rowTableName, self.onChildren)
            item.relationship = relationship
        item.sheet = self
        self.addPopup(actionMenu)

        # load objects
        self.reflector.loadObjectsFrom(self.rowClass.rowTableName, data=dataIn, whereClause=whereIn, forceChildren=0).addCallback(self.gotRows)

    def gotRows(self, rows):
        y=0
        for row in rows:
            x=0
            for colName, ctype in self.rowClass.rowColumns:
                self.setCellValue(x+1, y+1, getattr(row, colName))
                x=x+1
            y=y+1
        self.rows = rows            
            
    def onChange(self, x, y, value):
        print "changed:", x, y, value
        if x < 0 or y < 0 or x >= len(self.rowClass.rowColumns) or y >= len(self.rows):
            print "Changed cell not on an existing row."
            return
        
        row = self.rows[y-1]
        (name, ctype) = self.rowClass.rowColumns[x-1]
        
        try:
            if ctype == "int" or ctype == "int4" or ctype == "int2":
                setattr(row, name, int(value))
            elif ctype == "float8" or ctype == "float":
                setattr(row, name, float(value))
            else:
                setattr(row, name, value)
        except:
            print "Invalid value for cell", name, ctype, value
            traceback.print_exc()
            return

        self.reflector.updateRow(row).addCallback(self.onUpdate)
        return 1

    def onEdit(self, item):
        pos = (self.popup.posX - self.rect[0], self.popup.posY - self.rect[1])
        (x,y) = self.findCellAt(pos[0], pos[1])
        if y-1 >= len(self.rows):
            return         
        form = BoatFormFrame(self.reflector, self.rowClass, y-1, self)
        form.populate(self.rows[y-1])

    def onNew(self, item):
        ##TODO: create a new row object
        pos = (self.popup.posX - self.rect[0], self.popup.posY - self.rect[1])
        (x,y) = self.findCellAt(pos[0], pos[1])
        form = BoatNewFormFrame(self.reflector, self.rowClass, self)

    def onChildren(self, item):
        pos = (self.popup.posX - self.rect[0], self.popup.posY - self.rect[1])
        (x,y) = self.findCellAt(pos[0], pos[1])
        row = self.rows[y-1]
        f = BoatChildrenFrame(self.rect[0]+50, self.rect[1]+50, self.reflector, row, item.relationship, self.dataIn)

    def onUpdate(self, stuff):
        print "updated row."

    def updateRowAt(self, row, y):
        x=0
        for colName, ctype in self.rowClass.rowColumns:
            self.setCellValue(x+1, y+1, getattr(row, colName))
            x=x+1

    def insertRowAt(self, row):
        x=0
        y = self.highestRow
        for colName, ctype in self.rowClass.rowColumns:
            self.setCellValue(x+1, y+1, getattr(row, colName))
            x=x+1
        
    def onDelete(self, item):
        pos = (self.popup.posX - self.rect[0], self.popup.posY - self.rect[1])
        (x,y) = self.findCellAt(pos[0], pos[1])
        if y-1 >= len(self.rows):
            return 
        row = self.rows[y-1]
        self.reflector.deleteRow(row).addCallback(self.onDeleted, row)

    def onDeleted(self, null, row):
        print "Deleted row."
        self.rows.remove(row)
        self.clear()
        self.gotRows(self.rows)
        
class BoatReflectorFrame(pyui.widgets.Frame):
    """A Frame that contains a list of the registered RowClasses/Tables and
    a tabbed dialog that can have a tab for each table/rowClass.
    """
    def __init__(self, reflector, x=0, y=0, width=620, height=400, dataIn=None):
        self.reflector = reflector
        self.dataIn = dataIn
        pyui.widgets.Frame.__init__(self, x, y, width, height, "Reflector Access")

        self.splitter = pyui.widgets.SplitterPanel(ratio=20)
        self.replacePanel(self.splitter)

        self.tableList = pyui.widgets.ListBox(self.onSelectTable)
        self.tabs = pyui.widgets.TabbedPanel()
        self.tablePanels = {}
        
        self.splitter.getFirstPanel().setLayout(pyui.layouts.TableLayoutManager(1,20))
        self.splitter.getSecondPanel().setLayout(pyui.layouts.GridLayoutManager(1,1))

        self.splitter.getFirstPanel().addChild(pyui.widgets.Button("Reflected Tables", None), (0,0,1,1) )
        self.splitter.getFirstPanel().addChild(self.tableList, (0,1,1,19))
        self.splitter.getSecondPanel().addChild(self.tabs)

        self.pack()

        self.populate()
        
    def populate(self):
        self.tableList.clear()
        for info in self.reflector.schema.values():
            self.tableList.addItem(info.rowTableName, info)
        self.tableList.sortByName()
            
    def onSelectTable(self, item):
        if item:
            self.switchToTable(item.data.rowTableName)
            self.setDirty(1)

    def switchToTable(self, tableName):
        panel = self.tablePanels.get(tableName)
        if panel:
            self.tabs.activatePanel(panel)
        else:
            panel = BoatSheet(self.reflector, self.reflector.schema[tableName].rowClass, dataIn=self.dataIn)
            self.tabs.addPanel(tableName, panel)
            self.tablePanels[tableName]=panel
            self.tabs.activatePanel(panel)

