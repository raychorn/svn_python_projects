import Tkinter
import tkSimpleDialog
from Tkinter import *

class test1(tkSimpleDialog.Dialog):
	def __init__(self, master):
		scrollbar = Scrollbar(master, orient=VERTICAL)
		self.b1 = Listbox(master, yscrollcommand=scrollbar.set)
		self.b2 = Listbox(master, yscrollcommand=scrollbar.set)
		scrollbar.config(command=self.yview)
		scrollbar.pack(side=RIGHT, fill=Y)
		self.b1.pack(side=LEFT, fill=BOTH, expand=1)
		self.b2.pack(side=LEFT, fill=BOTH, expand=1)
	
	def yview(self, *args):
		apply(self.b1.yview, args)
		apply(self.b2.yview, args)

if __name__ == '__main__':
	root = Tkinter.Tk()
	test1(root)