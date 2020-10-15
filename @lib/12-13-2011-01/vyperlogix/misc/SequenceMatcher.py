from difflib import SequenceMatcher

def reportRatios(s,pat1,pat2):
	print 's.ratio("%s", "%s")=(%s)' % (pat1, pat2,s.ratio())
	print 's.quick_ratio("%s", "%s")=(%s)' % (pat1, pat2,s.quick_ratio())
	print 's.real_quick_ratio("%s", "%s")=(%s)' % (pat1, pat2,s.real_quick_ratio())

def computeAllRatios(pat1,pat2):
	seq = SequenceMatcher(None, pat1, pat2)
	return (seq.ratio(),seq.quick_ratio(),seq.real_quick_ratio())

def computeQuickRatio(pat1,pat2):
	seq = SequenceMatcher(None, pat1, pat2)
	return seq.real_quick_ratio()

def computeRatio(pat1,pat2):
	seq = SequenceMatcher(None, pat1, pat2)
	return seq.ratio()

def computeRatios(pat1,pat2):
	return SequenceMatcher(None, pat1, pat2)

if __name__ == '__main__':
	a = "qabxcd"
	b = "abycdf"
	s = SequenceMatcher(None, a, b)
	for tag, i1, i2, j1, j2 in s.get_opcodes():
		print ("%7s a[%d:%d] (%s) b[%d:%d] (%s)" % (tag, i1, i2, a[i1:i2], j1, j2, b[j1:j2]))

	s = computeRatios("abcd", "bcde")
	reportRatios(s, "abcd", "bcde")
	
	s = computeRatios("qabxcd", "abycdf")
	reportRatios(s, "qabxcd", "abycdf")

