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

"""This module uses Twisted Enterprise to interface to a relational database.
For more information see: http://www.twistedmatrix.com

WANRING: this is experimental code and may not work. Multithreaded python database access and PyUI
together are a dangerous combination so far.

"""

from twisted.enterprise import row
import pyui

from pyui.desktop import getDesktop, getTheme, getRenderer

class DBKeyCell(pyui.widgets.Label):
    """A cell in a data grid for an immutable key column
    """
    def draw(self, renderer):
        renderer.drawRect(pyui.colors.grey, self.windowRect)
        pyui.widgets.Label.draw(self, renderer)
        
class DBGridCell(pyui.widgets.Edit):
    """A cell in data grid for a non-key column (can be changed)
    """

    def __init__(self, reflector, rowObject, column):
        self.reflector = reflector
        self.rowObject = rowObject
        self.column = column
        text = "%s" % getattr(self.rowObject, column)
        
        pyui.widgets.Edit.__init__(self, text, 32, self.onEnter)
        
    def onEnter(self, cell):
        for column, typeid in self.rowObject.rowColumns:
            if column == self.column:
                if row.dbTypeMap[typeid] == row.NOQUOTE:
                    setattr(self.rowObject, self.column, int(self.text) )
                else:
                    setattr(self.rowObject, self.column, self.text)
            self.reflector.updateRow(self.rowObject)    
        self.setDirty(1)
        pyui.widgets.Edit.loseFocus(self)
        return 1

    def loseFocus(self):
        if self.text:
            self.onEnter(self)
        return pyui.widgets.Edit.loseFocus(self)

    def draw(self, renderer):
        if getDesktop().focusWidget == self:
            renderer.drawRect(pyui.colors.black, self.windowRect)
        pyui.widgets.Edit.draw(self, renderer)

class DBGridPanel(pyui.grid.GridPanel):
    """A Grid Panel to display the rows in a database table. Uses Twisted Enterprise
    Row objects to interface to the database. This panel loads the data from the database
    when the panel is created.
    """
    def __init__(self, rowClass, tableName, keyColumns, rows, reflector):
        pyui.grid.GridPanel.__init__(self, len(rowClass.rowColumns), rows, 1, 0)
        self.tableName = tableName
        self.rowClass = rowClass
        self.keyColumns = keyColumns
        self.reflector = reflector
        i = 0
        for column, ctype in self.rowClass.rowColumns:
            self.setColumnName(i, column)
            i = i + 1
        if rowClass.populated:
            self.populated(0)
        else:
            self.reflector.runInteraction(self.reflector._populateSchemaFor,
                                          rowClass).addCallback(self.populated)

    def populated(self, dummy):
        """Called when the rowClass is populated.
        """
        self.reflector.loadObjectsFrom(self.tableName).addCallback(self.gotData).arm()
        
    def gotData(self, rows):
        """called when the data for the table comes back.
        """
        self.rows = rows
        r = 0
        for row in rows:
            c = 0
            for column, ctype in self.rowClass.rowColumns:
                newCell = None
                dbKeyColumns = self.reflector.getTableInfo(row).rowKeyColumns
                for keyColumn, ctype in dbKeyColumns:
                    if keyColumn == column:
                        value = getattr(row, column)
                        newCell = DBKeyCell("%s" % value)
                if not newCell:
                    newCell = DBGridCell(self.reflector, row, column)
                self.putCellAt(newCell, c, r)
                c = c +1
            r = r + 1
            
    def refresh(self):
        self.clear()
        self.populated(0)
        
