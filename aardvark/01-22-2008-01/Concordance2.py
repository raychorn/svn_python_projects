import psyco
import pprint
import ConcordanceProcessor

_packages_filename = '#packages.txt'

def main():
	print '(main) :: BEGIN:'
	c = ConcordanceProcessor.Concordance(_packages_filename)
	
	print 'BEGIN: _dataBase'
	pp = pprint.PrettyPrinter(indent=4)
	pp.pprint(c.dataBase)
	print 'END! _dataBase'
	print

	print 'BEGIN: _synonyms'
	pp = pprint.PrettyPrinter(indent=4)
	pp.pprint(c.synonyms)
	print 'END! _synonyms'
	print

	print 'BEGIN: _concordance'
	pp = pprint.PrettyPrinter(indent=4)
	pp.pprint(c.concordance)
	print 'END! _concordance'
	print

	print '(main) :: END !'

if (__name__ == '__main__'):
	psyco.bind(main)
	main()
	