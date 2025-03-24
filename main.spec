# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_data_files

# Coleta dados extras (arquivos e pastas necessários)
datas = collect_data_files('interface_utilisateur', includes=['*.txt'])
datas += collect_data_files('interface_utilisateur/contrats', includes=['*.txt'])
datas += collect_data_files('base_donnees')
datas += collect_data_files('constantes')
datas += collect_data_files('requetes_sql')
datas += collect_data_files('fonctions_gestion')
datas += collect_data_files('utils')

a = Analysis(
    ['main.py'],
    pathex=['.'],
    binaries=[],
    datas=[
        ('interface_utilisateur/contrats', 'interface_utilisateur/contrats'),
    ],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    noarchive=False
)


pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='GNLocation',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None
)
