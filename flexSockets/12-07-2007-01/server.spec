a = Analysis([os.path.join(HOMEPATH,'support\\_mountzlib.py'), 'server.py'],
             pathex=['Z:\\python projects\\flexSockets'])
pyz = PYZ(a.pure)
exe = EXE( pyz,
          a.scripts,
          a.binaries,
          name='server.exe',
          debug=False,
          strip=False,
          upx=True,
          console=True )
