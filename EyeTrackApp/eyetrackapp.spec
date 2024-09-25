# -*- mode: python ; coding: utf-8 -*-

import sys ; sys.setrecursionlimit(sys.getrecursionlimit() * 5)
import os

block_cipher = None

# Get the directory where the spec file is located
#spec_dir = os.path.dirname(os.path.abspath(__file__))

# Build the path to the user_data folder
#user_data_source = os.path.abspath(os.path.join(spec_dir, '../user_data'))



user_data_toc = Tree('../user_data', prefix='user_data', excludes=['tmp', '*.pyc'], typecode='DATA')
added_files = [
#( 'src/README.txt', '.' ),
( '/../user_data', 'user_data'),
#( '/mygame/sfx/*.mp3', 'sfx' )
]

resources=[("Audio/*", "Audio"), ("Images/*", "Images/"), ("pye3d/refraction_models/*", "pye3d/refraction_models/"), ("Models/*", "Models/"),("Tools/*", "Tools/"), 
#("../user_data/*", "user_data/"),  # Include the user_data folder
#Tree(user_data_source, dest="user_data"),  # Include the user_data folder
#Tree('../user_data', prefix='user_data', excludes=['tmp', '*.pyc'], typecode='DATA'), # user_data_toc = 
]



a = Analysis(
['eyetrackapp.py'],
pathex=[],
binaries=[],
datas=resources,
hiddenimports=['cv2', 'numpy', 'PySimpleGui', 'pkg_resources.extern'],
hookspath=[],
hooksconfig={},
runtime_hooks=[],
excludes=[],
win_no_prefer_redirects=False,
win_private_assemblies=False,
cipher=block_cipher,
noarchive=False
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='eyetrackapp',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon="Images/logo.ico", 
)