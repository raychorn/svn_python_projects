import os, sys
import ConfigParser

from vyperlogix import misc
from vyperlogix.misc import _utils

from vyperlogix.hash.lists import HashedLists
from vyperlogix.classes.SmartObject import SmartFuzzyObject

from vyperlogix.win import shortcut_hook

__symbol__ = 'InternetShortcut'

def get_items_from_url_shortcut_file(fileName):
    try:
	data = _utils.readFileFrom(fileName)
	items = SmartFuzzyObject(args={})
	c = ConfigParser.ConfigParser()
	c.read(fileName)
	if (c.has_section(__symbol__)):
	    items = SmartFuzzyObject(args=dict(c.items(__symbol__)))
    except:
	items = SmartFuzzyObject(args={})
    return items

def get_items_from_url_shortcuts(fpath=None):
    items = HashedLists(fromDict={}, caseless=False)
    if (os.path.exists(fpath)):
	if (os.path.isdir(fpath)):
	    files = shortcut_hook.get_shortcut_paths(fpath)
	    for f in files:
		_items_ = get_items_from_url_shortcut_file(f)
		for k, v in _items_.asPythonDict().iteritems():
		    items[k] = v
	else:
	    items = get_items_from_url_shortcut_file(fpath)
    return items

