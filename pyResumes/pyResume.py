
if (__name__ == '__main__'):
    from vyperlogix.misc import _psyco
    _psyco.importPsycoIfPossible(func=main)

    from vyperlogix.misc import Args

    args = {'--help':'show some help.',
            '--verbose':'output more stuff.',
            '--delete':'delete the specified keypath.',
            '--input=?':'the name of the file being read.',
            }
    _argsObj = Args.Args(args)

    _progName = _argsObj.programName

    if (_argsObj.isVerbose):
        print '_argsObj=(%s)' % str(_argsObj)

    if (_argsObj.isHelp):
        Args.ppArgs()
    else:
        main()
