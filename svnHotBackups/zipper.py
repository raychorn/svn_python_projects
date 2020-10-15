if (__name__ == '__main__'):
    from vyperlogix.zip import secure
    from vyperlogix.misc import _utils
    def main():
	import os, sys
	from vyperlogix.crypto import XTEAEncryption
	from vyperlogix.crypto import blowfish

	cname = _utils.getComputerName()
	_iv = XTEAEncryption.iv(_utils.getProgramName())
	_passPhrase = blowfish.seedPassword('nowisthetimeforallgoodmentocometotheaidoftheircountry')
	if (cname == 'UNDEFINED3'):
	    _top = 'C:\\@1b\\neon-0.28.3'
	    _dest = 'C:\\@3\\%s.zip' % (os.path.basename(_top))
	elif (cname.lower() == 'misha-lap.ad.magma-da.com'):
	    _top = 'C:\\@1a\\neon-0.28.3\\neon-0.28.3'
	    _dest = 'C:\\@1d\\%s.zip' % (os.path.basename(_top))
	if (len(sys.argv) > 1) and (sys.argv[1] == 'zip'):
	    secure.zipper(_top,_dest,archive_type=secure.ZipType.ezip,_iv=_iv)
	elif (len(sys.argv) > 1) and (sys.argv[1] == 'xzip'):
	    secure.zipper(_top,_dest,archive_type=secure.ZipType.xzip,_iv=_iv)
	elif (len(sys.argv) > 1) and (sys.argv[1] == 'bzip'):
	    secure.zipper(_top,_dest,archive_type=secure.ZipType.bzip,passPhrase=_passPhrase)
	if (cname == 'UNDEFINED3'):
	    _dest = 'C:\\@3\\%s.ezip' % (os.path.basename(_top))
	    _top = 'C:\\@3a'
	elif (cname.lower() == 'misha-lap.ad.magma-da.com'):
	    _dest = 'C:\\@1d\\%s.ezip' % (os.path.basename(_top))
	    _top = 'C:\\@1'
	if (len(sys.argv) > 1) and (sys.argv[1] == 'unzip'):
	    secure.unzipper(_dest,_top,archive_type=secure.ZipType.ezip,_iv=_iv)
	elif (len(sys.argv) > 1) and (sys.argv[1] == 'unxzip'):
	    secure.unzipper(_dest,_top,archive_type=secure.ZipType.xzip,_iv=_iv)
	elif (len(sys.argv) > 1) and (sys.argv[1] == 'unbzip'):
	    secure.unzipper(_dest,_top,archive_type=secure.ZipType.bzip,passPhrase=_passPhrase)

    from vyperlogix.misc import _psyco
    _psyco.importPsycoIfPossible(func=main)
    main()
