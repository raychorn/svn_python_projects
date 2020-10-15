from PyLucene import StandardAnalyzer, RAMDirectory, Document, Field, IndexWriter, IndexReader

analyzer = StandardAnalyzer()

directory = RAMDirectory()

iwriter = IndexWriter(directory,analyzer,True)
ts = ["this bernhard is the text to be index text",
      "this claudia is the text to be index"]
for t in ts:
    doc = Document()
    doc.add(Field("fieldname",t,
                  Field.Store.YES, Field.Index.TOKENIZED,
                  Field.TermVector.WITH_POSITIONS_OFFSETS))
    iwriter.addDocument(doc)
iwriter.optimize()
iwriter.close()


ireader = IndexReader.open(directory)
tfv = ireader.getTermFreqVector(0,'fieldname').toTermPositionVector()
for (t,f,i) in zip(tfv.getTerms(),tfv.getTermFrequencies(),xrange(100000)):
    print 'term %s' % t
    print '  freq: %i' % f
    try:
        print '  pos: ' + str([p for p in tfv.getTermPositions(i)])
    except:
        print '  no pos'
    try:
        print '  off: ' + \
              str(["%i-%i" % (o.getStartOffset(), o.getEndOffset())
                   for o in tfv.getOffsets(i)])
    except:
        print '  no offsets'
