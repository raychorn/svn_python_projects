#!/usr/bin/python
# -*- coding: iso-8859-1 -*

"""
convert_drkeys.py
Convert key codes of DrPython Shortcuts
Antonio Barbosa 29 Dec 2006

I must be run twice:
In first run, creates a file with «old» keycodes
In the second run, creates another file with «new» keycodes.
And then prompts for conversion of each shortcuts file of DrPython.

It should be wise to make backups of those files :)

"""


import os
import wxversion
import re
fname1="keys_2.6.txt"
fname2="keys_2.8.txt"
Dict1={}
Dict2={}

drFiles=["shortcuts.dat","stcshortcuts.dat","drscript.shortcuts.dat"]
userpreferencesdirectory = os.environ["APPDATA"].replace("\\", "/") +'/drpython/'


def convert(filename):
	print 'Converting: ',filename
	text='#version=%s\n' %wx.VERSION_STRING
	f = open(userpreferencesdirectory +filename, 'rb')
	line = f.readline()
	if line.find("version")>0:
		print '------> allready converted!'
		f.close()
		return
	while len(line) > 0:
		p0 = line.find("<keycode>")
		p1 = line.find("</keycode>")
		if p0>=0 and p1>p0:
			s0=line[:p0+len("<keycode>")]
			s1=line[p1:]
			key=line[p0+len("<keycode>"):p1]
			if len(key):
				#a=int(key)
				if Dict1.has_key(key):
					a=Dict1[key]
					key=Dict2[a]
			text+=s0+key+s1
		else:
			text+=line
		line = f.readline()
	f.close()
	f = open(userpreferencesdirectory +filename, 'w')
	f.write(text)
	f.close()
	print 'ok'
	
	
def save_key_codes(fname):
	print 'saving ',fname
	fragment = "WXK_"
	f=open (fname,'w')
	for elem in dir(wx):
		if elem.isupper() and fragment in elem:
			#print elem,eval('wx.'+elem)
			f.write( '%s\t%s\n' %(elem,eval('wx.'+elem)))
	f.close()



#---------------------------------

if os.path.exists(fname1)==False: #first run
	wxversion.select("2.6")
	import wx
	save_key_codes(fname1)
	print "please run this script again..."
else:                              #second run
	wxversion.select("2.8")
	import wx
	save_key_codes(fname2)
	#Creating dicts:
	f1 = open(fname1, 'r')
	for line in f1:
		s=line.strip().split('\t')
		Dict1[s[1]]=s[0] #Value:Name
	f1.close()
	f2 = open(fname2, 'r')
	for line in f2:
		s=line.strip().split('\t')
		Dict2[s[0]]=s[1] #Name:Value
	f2.close()
	#And finally, converting shortcuts files
	for file in drFiles:
		print "Process %s? (y/n)" %file,
		s=raw_input()
		if s=='y':
			convert(file)
