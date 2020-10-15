#!/usr/bin/env python

import sys, os, PyLucene, threading, time
from datetime import datetime

"""
This class is loosely based on the Lucene (java implementation) demo class 
org.apache.lucene.demo.IndexFiles.  It will take a directory as an argument
and will index all of the files in that directory and downward recursively.
It will index on the file path, the file name and the file contents.  The
resulting Lucene index will be placed in the current directory and called
'index'.
"""

class Ticker(object):

    def __init__(self):
        self.tick = True

    def run(self):
        while self.tick:
            sys.stdout.write('.')
            sys.stdout.flush()
            time.sleep(1.0)

class IndexFiles(object):
    """Usage: python IndexFiles.py <doc_directory> <file_pattern> <index_name>"""

    def __init__(self, root, storeDir, analyzer, pattern):

        if not os.path.exists(storeDir):
            os.mkdir(storeDir)
        store = PyLucene.FSDirectory.getDirectory(storeDir, True)
        writer = PyLucene.IndexWriter(store, analyzer, True)
        writer.setMaxFieldLength(1048576)
        self.indexDocs(root, writer, pattern)
        ticker = Ticker()
        print 'optimizing index',
        threading.Thread(target=ticker.run).start()
        writer.optimize()
        writer.close()
        ticker.tick = False
        print 'done'

    def indexDocs(self, root, writer, pattern):
        pattern = '.txt' if (not isinstance(pattern,str)) else pattern
        for root, dirnames, filenames in os.walk(root):
            for filename in filenames:
                if not filename.endswith(pattern):
                    continue
                print "adding", filename
                try:
                    path = os.path.join(root, filename)
                    file = open(path)
                    contents = unicode(file.read(), 'iso-8859-1')
                    file.close()
                    doc = PyLucene.Document()
                    doc.add(PyLucene.Field("name", filename,
                                           PyLucene.Field.Store.YES,
                                           PyLucene.Field.Index.UN_TOKENIZED))
                    doc.add(PyLucene.Field("path", path,
                                           PyLucene.Field.Store.YES,
                                           PyLucene.Field.Index.UN_TOKENIZED))
                    if len(contents) > 0:
                        doc.add(PyLucene.Field("contents", contents,
                                               PyLucene.Field.Store.YES,
                                               PyLucene.Field.Index.TOKENIZED))
                    else:
                        print "warning: no content in %s" % filename
                    writer.addDocument(doc)
                except Exception, e:
                    print "Failed in indexDocs:", e

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print IndexFiles.__doc__
        sys.exit(1)
    print 'PyLucene', PyLucene.VERSION, 'Lucene', PyLucene.LUCENE_VERSION
    start = datetime.now()
    try:
        progName, pathName, pattern, indexName = sys.argv[:4]
        print 'progName=(%s)' % (progName)
        print 'pathName=(%s)' % (pathName)
        print 'pattern=(%s)' % (pattern)
        print 'indexName=(%s)' % (indexName)
        IndexFiles(pathName, indexName, PyLucene.StandardAnalyzer(), pattern)
        end = datetime.now()
        print end - start
    except Exception, e:
        print "Failed: ", e
        print IndexFiles.__doc__
