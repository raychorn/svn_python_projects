# -*- mode: python -*-
a = Analysis([os.path.join(HOMEPATH,'support\\_mountzlib.py'), os.path.join(HOMEPATH,'support\\useUnicode.py'), 'J:\\@Vyper Logix Corp\\@Projects\\python\\windows-user-scripts\\windows-lock-if-not-correct-user.py'],
             pathex=['J:\\@Research\\@Python\\PyInstaller 1.5.1\\pyinstaller-1.5.1'])
pyz = PYZ(a.pure)
exe = EXE( pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name=os.path.join('dist', 'windows-lock-if-not-correct-user.exe'),
          debug=False,
          strip=False,
          upx=True,
          console=True )
