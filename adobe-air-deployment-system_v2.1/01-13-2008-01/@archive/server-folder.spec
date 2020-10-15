a = Analysis([os.path.join(HOMEPATH,'support\\_mountzlib.py'), '../XMLSocketServer.py'],
             pathex=['Z:\\python projects\\adobe-air-deployment-system\\@archive'])
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=1,
          name='buildserver-folder/server-folder.exe',
          debug=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT( exe,
               a.binaries,
               strip=False,
               upx=True,
               name='distserver-folder')
