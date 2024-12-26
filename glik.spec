# -*- mode: python ; coding: utf-8 -*-
import os

block_cipher = None

# Informazioni sulla versione del file
version_info = {
    'version': '1.0.0',
    'company_name': 'Emmanuele Pani',
    'file_description': 'Glik - A Nightscout desktop viewer',
    'internal_name': 'Glik',
    'legal_copyright': '© 2025 Emmanuele Pani. Under GNU AGPL v3.0',
    'original_filename': 'Glik.exe',
    'product_name': 'Glik',
    'product_version': '1.0.0'
}

# Ottieni il percorso assoluto della directory corrente
basedir = os.path.abspath(os.path.dirname('__file__'))

a = Analysis(['main.py'],
    pathex=[basedir],  # Usa il percorso base
    binaries=[],
    datas=[
        (os.path.join(basedir, 'src/assets/logo_glik.png'), 'src/assets'),
        (os.path.join(basedir, 'src/config.json'), 'src'),
    ],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Glik',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    onefile=True,
    version='file_version_info.txt',  # Riferimento al file di versione
    icon=os.path.join(basedir, 'src/assets/logo_glik.png')) 