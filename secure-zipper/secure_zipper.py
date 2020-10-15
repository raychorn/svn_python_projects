import os, sys
from vyperlogix.zip import secure

s_passPhrase = [110,111,119,105,115,116,104,101,116,105,109,101,102,111,114,97,108,108,103,111,111,100,109,101,110,116,111,99,111,109,101,116,111,116,104,101,97,105,100,111,102,116,104,101,105,114,99,111,117,110,116,114,121]
_passPhrase = ''.join([chr(ch) for ch in s_passPhrase])

__top__ = r'J:\@Vyper Logix Corp\@Projects\python\svnHotBackups'

__archive__ = os.path.abspath('./archive.bak')

def main():
    #secure.zipper(__top__, __archive__, archive_type=secure.ZipType.zip, passPhrase=_passPhrase)
    pass

if (__name__ == '__main__'):
    import hotshot, hotshot.stats, test.pystone
    prof = hotshot.Profile("profiler.prof")
    benchtime, stones = prof.runcall(main)
    prof.close()
    stats = hotshot.stats.load("profiler.prof")
    stats.strip_dirs()
    stats.sort_stats('time', 'calls')
    stats.print_stats(20)

