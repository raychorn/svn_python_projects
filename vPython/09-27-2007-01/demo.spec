a = Analysis([os.path.join(HOMEPATH,'support\\_mountzlib.py'), 'theBall.py'],
             pathex=['Z:\\python projects\\vPython'])
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=1,
          name='builddemo/demo.exe',
          debug=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT( exe,
               a.binaries,
               strip=False,
               upx=True,
               name='distdemo')
