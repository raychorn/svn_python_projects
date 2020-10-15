# -*- mode: python -*-
a = Analysis([os.path.join(HOMEPATH,'support\\_mountzlib.py'), os.path.join(HOMEPATH,'support\\useUnicode.py'), 'J:\\@Vyper Logix Corp\\@Projects\\python\\sqlautocode_cleanup\\sqlautocode_cleanup.py'],
             pathex=['J:\\@Vyper Logix Corp\\@Projects\\python\\sqlautocode_cleanup'])
pyz = PYZ(a.pure)
exe = EXE( pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name=os.path.join('dist', 'sqlautocode_cleanup.exe'),
          debug=False,
          strip=False,
          upx=True,
          console=True )
