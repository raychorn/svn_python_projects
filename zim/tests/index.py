# -*- coding: utf-8 -*-

# Copyright 2009 Jaap Karssenberg <jaap.karssenberg@gmail.com>

import tests

import gtk
import pango

from zim.fs import Dir
from zim.notebook import Notebook, Path, Link, init_notebook
from zim.index import *
from zim.gui.pageindex import *
from zim.formats import ParseTree

# TODO test n_list_* functions


def get_files_notebook(key):
	# We fill the notebook using the store interface, as this test comes before
	# the notebook test, but after the store test.
	dir = Dir(tests.create_tmp_dir('index_'+key))
	init_notebook(dir)
	notebook = Notebook(dir=dir)
	store = notebook.get_store(':')
	manifest = []
	for name, text in tests.get_test_data('wiki'):
		manifest.append(name)
		page = store.get_page(Path(name))
		page.parse('wiki', text)
		store.store_page(page)
	notebook.testdata_manifest = tests.expand_manifest(manifest)
	return notebook


class TestIndex(tests.TestCase):

	def setUp(self):
		# Note that in this test our index is not the default index
		# for the notebook. So any assumption from the notebook about
		# the index will be wrong.
		self.index = Index(dbfile=':memory:')
		self.notebook = tests.get_test_notebook()
		self.index.set_notebook(self.notebook)

	def runTest(self):
		'''Test indexing'''
		# This is one big test instead of seperate sub tests because in the
		# subclass we generate a file based notebook in setUp, and we do not
		# want to do that many times

		#~ print self.__class__.__name__
		self.index.update()

		#~ print '\n==== DB ===='
		#~ cursor = self.index.db.cursor()
		#~ cursor.execute('select * from pages')
		#~ for row in cursor:
			#~ print row
		#~ cursor.execute('select * from links')
		#~ for row in cursor:
			#~ print row

		# paths / ids
		path = self.index.lookup_path(Path('Test:foo:bar'))
		self.assertTrue(isinstance(path, IndexPath))
		path = self.index.lookup_id(path.id)
		self.assertTrue(isinstance(path, IndexPath))
		self.assertEqual(path.name, 'Test:foo:bar')

		# pages
		pagelist = list(self.index.list_pages(None))
		self.assertTrue(len(pagelist) > 0)
		pagelist = list(self.index.list_pages(Path('Test')))
		self.assertTrue(len(pagelist) > 0)
		for page in pagelist:
			self.assertTrue(page.name.startswith('Test:'))
			self.assertTrue(page.name.count(':') == 1)
		pagelist = list(self.index.list_pages(Path('Linking')))
		self.assertTrue(Path('Linking:Dus') in pagelist)
		pagelist = list(self.index.list_pages(Path('Some:Non:Existing:Path')))
		self.assertTrue(len(pagelist) == 0)

		# links
		forwlist = list(self.index.list_links(Path('Test:foo:bar')))
		backlist = list(self.index.list_links(Path('Test:foo:bar'), LINK_DIR_BACKWARD))
		bothlist = list(self.index.list_links(Path('Test:foo:bar'), LINK_DIR_BOTH))
		for l in forwlist, backlist, bothlist:
			self.assertTrue(len(l) > 0)
			for link in l:
				self.assertTrue(isinstance(link, Link))
				self.assertTrue(isinstance(link.source, IndexPath))
				self.assertTrue(isinstance(link.href, IndexPath))
		self.assertTrue(len(forwlist) + len(backlist) == len(bothlist))

		n = self.index.n_list_links(Path('Test:foo:bar'), LINK_DIR_BACKWARD)
		self.assertEqual(n, len(backlist))

		# tags
		taglist = list(self.index.list_tags(Path('Test:tags')))
		self.assertTrue(len(taglist) == 11)
		for tag in taglist:
			self.assertTrue(isinstance(tag, IndexTag))
		tagnames = [t.name for t in taglist]
		aretags = ['tags', 'beginning', 'end', 'tabs', 'verbatim',
				   'enumerations', 'encoding', 's', 'num6ers', 'wit', 'cr']
		nottags = ['places', 'links', 'captions', 'Headings', 'word']
		for t in aretags:
			self.assertTrue(t in tagnames)
		for t in nottags:
			self.assertTrue(not t in tagnames)

		# cursor.row_count is not reliable - see docs
		def count_pages(db):
			c = db.cursor()
			c.execute('select id from pages')
			r = c.fetchall()
			return len(r)

		def dump_db(db):
			c = db.cursor()
			c.execute('select * from pages')
			text = ''
			for row in c:
				# HACK iterating of sqlite3.Row objects only supported for python 2.6
				myrow = []
				for i in range(len(row)):
					myrow.append(row[i])
				text += ', '.join(map(str, myrow)) + '\n'
			return text

		# repeat update() to check if update is stable
		manifest = len(self.notebook.testdata_manifest)
		self.assertTrue(count_pages(self.index.db) >= manifest)
		origdb = dump_db(self.index.db)
		self.index.update(checkcontents=False)
		self.assertEqualDiff(dump_db(self.index.db), origdb)

		# indexkey
		for path in (Path('Test'), Path('Test:foo')):
			indexpath = self.index.lookup_path(path)
			self.assertEqual(indexpath.contentkey, self.notebook.get_page_indexkey(path))
			self.assertEqual(indexpath.childrenkey, self.notebook.get_pagelist_indexkey(path))

		# other functions
		path = self.index.get_unique_path(Path('non-existing-path'))
		self.assertEqual(path, Path('non-existing-path'))
		path = self.index.get_unique_path(Path('Test:foo'))
		self.assertEqual(path, Path('Test:foo_1'))

		# get_previous / get_next
		page = list(self.index.list_pages(None))[0]
		seen = 0
		while page:
			seen = max(seen, page.name.count(':'))
			page = self.index.get_next(page)
		self.assertTrue(seen >= 2)

		page = list(self.index.list_pages(None))[-1]
		seen = 0
		while page:
			seen = max(seen, page.name.count(':'))
			page = self.index.get_previous(page)
		self.assertTrue(seen >= 2)

		# now go through the flush loop
		self.index.flush()
		self.assertEqual(count_pages(self.index.db), 1)
		self.index.update()
		self.assertEqualDiff(dump_db(self.index.db), origdb)

		# now index only part of the tree - and repeat
		self.index.flush()
		self.assertEqual(count_pages(self.index.db), 1)
		self.index.update(Path('Test'))
		self.assertTrue(count_pages(self.index.db) > 2)
		partdb = dump_db(self.index.db)
		self.index.update(Path('Test'))
		self.assertEqualDiff(dump_db(self.index.db), partdb)

		# Index whole tree again
		self.index.update()

		# Check cleanup
		path = Path('New:Nested:Path')
		self.index.touch(path)
		parent = self.index.lookup_path(path.parent)
		self.assertTrue(parent and parent.haschildren)
		self.index.delete(path)
		parent = self.index.lookup_path(path.parent)
		self.assertTrue(parent is None)

		#~ # Check cleanup for links
		links = [link.href for link in self.index.list_links(Path('roundtrip'))]
		for p in ('foo:bar', 'Bar'):
			self.assertTrue(Path(p) in links)
			path = self.index.lookup_path(Path('foo:bar'))
			self.assertTrue(path)

		# Check for tag indexing
		tags = [tag.name for tag in self.index.list_tags(Path('roundtrip'))]
		for t in ('foo', 'bar'):
			self.assertTrue(t in tags)
			tagged = list(self.index.list_tagged_pages(t))
			self.assertTrue(Path('roundtrip') in tagged)

		tree = ParseTree().fromstring('<zim-tree><link href=":foo:bar">:foo:bar</link></zim-tree>')
		page = self.notebook.get_page(Path('roundtrip'))
		page.set_parsetree(tree)
		self.notebook.store_page(page)
		path = self.index.lookup_path(Path('Bar'))
		self.assertTrue(path is None)
		path = self.index.lookup_path(Path('foo:bar'))
		self.assertTrue(path)

		self.notebook.delete_page(Path('roundtrip'))
		path = self.index.lookup_path(Path('foo:bar'))
		self.assertTrue(path is None)


class TestIndexFiles(TestIndex):
	# Like the test above, but now using a files backend

	slowTest = True

	def setUp(self):
		self.notebook = get_files_notebook('TestIndexFiles')
		self.index = self.notebook.index

	def runTest(self):
		'''Test indexing files'''
		TestIndex.runTest(self)


def color_to_string(color):
	# helper method for comparing gtk.gdk.Color objects
	return '%i,%i,%i' % (color.red, color.green, color.blue)


class TestPageTreeStore(tests.TestCase):

	def setUp(self):
		self.index = Index(dbfile=':memory:')
		self.notebook = tests.get_test_notebook()
		self.index.set_notebook(self.notebook)
		self.notebook.index.update()

	def runTest(self):
		'''Test PageTreeStore index interface'''
		# This is one big test instead of seperate sub tests because in the
		# subclass we generate a file based notebook in setUp, and we do not
		# want to do that many times.
		# Hooking up the treeview as well just to see if we get any errors
		# From the order the signals are generated.

		ui = MockUI()
		ui.notebook = self.notebook
		ui.page = Path('Test:foo')
		self.assertTrue(self.notebook.get_page(ui.page).exists())

		treeview = PageTreeView(ui)
		treestore = PageTreeStore(self.index)
		self.assertEqual(treestore.get_flags(), 0)
		self.assertEqual(treestore.get_n_columns(), 5)
		treeview.set_model(treestore)

		def process_events(*a):
			while gtk.events_pending():
				gtk.main_iteration(block=False)
			return True # continue

		self.index.update(callback=process_events)
		process_events()

		treeview = PageTreeView(ui) # just run hidden to check errors
		treeview.set_model(treestore)

		n = treestore.on_iter_n_children(None)
		self.assertTrue(n > 0)
		n = treestore.iter_n_children(None)
		self.assertTrue(n > 0)

		for i in range(treestore.get_n_columns()):
			self.assertTrue(not treestore.get_column_type(i) is None)

		# Quick check for basic methods
		iter = treestore.on_get_iter((0,))
		self.assertTrue(isinstance(iter, PageTreeIter))
		self.assertFalse(iter.indexpath.isroot)
		basename = treestore.on_get_value(iter, 0)
		self.assertTrue(len(basename) > 0)
		self.assertEqual(iter.treepath, (0,))
		self.assertEqual(treestore.on_get_path(iter), (0,))
		self.assertEqual(treestore.get_treepath(iter.indexpath), (0,))
		self.assertEqual(treestore.get_treepath(Path(iter.indexpath.name)), (0,))

		iter2 = treestore.on_iter_children(None)
		self.assertEqual(iter2.indexpath, iter.indexpath)

		self.assertTrue(treestore.on_get_iter((20,20,20,20,20)) is None)
		self.assertTrue(treestore.get_treepath(Path('nonexisting')) is None)
		self.assertRaises(ValueError, treestore.get_treepath, Path(':'))

		# Now walk through the whole notebook testing the API
		# with nested pages and stuff
		npages = 0
		path = []
		for page in self.notebook.walk():
			#~ print '>>', page
			npages += 1
			names = page.name.split(':')
			if len(names) > len(path):
				path.append(0) # always increment by one
			elif len(names) < len(path):
				while len(names) < len(path):
					path.pop()
				path[-1] += 1
			else:
				path[-1] += 1
			#~ print '>>', page, path
			iter = treestore.get_iter(tuple(path))
			indexpath = treestore.get_indexpath(iter)
			#~ print '>>>', indexpath
			self.assertEqual(indexpath, page)
			self.assertEqual(treestore.get_value(iter, NAME_COL), page.basename)
			self.assertEqual(treestore.get_value(iter, PATH_COL), page)
			if page.hascontent or page.haschildren:
				self.assertEqual(treestore.get_value(iter, EMPTY_COL), False)
				self.assertEqual(treestore.get_value(iter, STYLE_COL), pango.STYLE_NORMAL)
				self.assertEqual(
					color_to_string( treestore.get_value(iter, FGCOLOR_COL) ),
					color_to_string( treestore.NORMAL_COLOR) )
			else:
				self.assertEqual(treestore.get_value(iter, EMPTY_COL), True)
				self.assertEqual(treestore.get_value(iter, STYLE_COL), pango.STYLE_ITALIC)
				self.assertEqual(
					color_to_string( treestore.get_value(iter, FGCOLOR_COL) ),
					color_to_string( treestore.EMPTY_COLOR) )
			self.assertEqual(treestore.get_path(iter), tuple(path))
			if indexpath.haschildren:
				self.assertTrue(treestore.iter_has_child(iter))
				child = treestore.iter_children(iter)
				self.assertTrue(not child is None)
				child = treestore.iter_nth_child(iter, 0)
				self.assertTrue(not child is None)
				parent = treestore.iter_parent(child)
				self.assertEqual(
					treestore.get_indexpath(parent), page)
				childpath = treestore.get_path(child)
				self.assertEqual(
					childpath, tuple(path) + (0,))
				n = treestore.iter_n_children(iter)
				for i in range(1, n):
					child = treestore.iter_next(child)
					childpath = treestore.get_path(child)
					self.assertEqual(
						childpath, tuple(path) + (i,))
				child = treestore.iter_next(child)
				self.assertTrue(child is None)

			else:
				self.assertTrue(not treestore.iter_has_child(iter))
				child = treestore.iter_children(iter)
				self.assertTrue(child is None)
				child = treestore.iter_nth_child(iter, 0)
				self.assertTrue(child is None)

		self.assertTrue(npages > 10) # double check sanity of walk() method

		# Check if all the signals go OK
		treestore.disconnect_index()
		del treestore
		self.index.flush()
		treestore = PageTreeStore(self.index)
		treeview = PageTreeView(ui, treestore)
		self.index.update(callback=process_events)

		# Try some TreeView methods
		path = Path('Test:foo')
		self.assertTrue(treeview.select_page(path))
		self.assertEqual(treeview.get_selected_path(), path)
		treepath = treeview.get_model().get_treepath(path)
		self.assertTrue(not treepath is None)
		col = treeview.get_column(0)
		treeview.row_activated(treepath, col)

		#~ treeview.emit('popup-menu')
		treeview.emit('insert-link', path)
		treeview.emit('copy')

		# Check if all the signals go OK in delete
		for page in reversed(list(self.notebook.walk())): # delete bottom up
			self.notebook.delete_page(page)
			process_events()


class TestPageTreeStoreFiles(TestPageTreeStore):

	slowTest = True

	def setUp(self):
		self.notebook = get_files_notebook('TestPageTreeStoreFiles')
		self.index = self.notebook.index

	def runTest(self):
		'''Test PageTreeStore index interface with files index'''
		TestPageTreeStore.runTest(self)


class MockUI(tests.MockObject):

	page = None
	notebook = None
