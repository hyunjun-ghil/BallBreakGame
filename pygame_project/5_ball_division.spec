# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['5_ball_division.py'],
             pathex=['C:\\Users\\10190544\\Documents\\GitHub\\desktop-tutorial\\pygame_project'],
             binaries=[],
             datas=[('./images', './images')],
             hiddenimports=['pygame','os'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='5_ball_division',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False )
