# -*- mode: python ; coding: utf-8 -*-
from os import path
block_cipher = None

add_files = [
    ('assets\\sprites','assets\\sprites'),
    ('assets\\audio','assets\\audio')
]

script_dir = path.dirname(path.abspath(SPEC))
a = Analysis(['game.py'],
             binaries=[],
             datas=add_files,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=['tcl', 'lib2to3', 'ssl', 'bz2', 'lzma', 'curses'],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
excluded_binaries = ['libcrypto-1_1.dll']
a.binaries = TOC([x for x in a.binaries if x[0] not in excluded_binaries])
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='FlappyBird',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,
		  icon=os.path.join(script_dir, 'logo.ico'))
