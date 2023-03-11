# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['lyrical.py'],
    pathex=[],
    binaries=[('resources/en.json.gz', 'spellchecker/resources'),('resources/de.json.gz', 'spellchecker/resources'),('resources/es.json.gz', 'spellchecker/resources'),('resources/fr.json.gz', 'spellchecker/resources'),('resources/pt.json.gz', 'spellchecker/resources')],
    datas=[('literary_resources/beautiful_words.json', 'literary_resources/'),('literary_resources/colours.json', 'literary_resources/'),('literary_resources/descriptors.json', 'literary_resources/'),('literary_resources/smells.json', 'literary_resources/'),('literary_resources/sounds.json', 'literary_resources/'),('literary_resources/touch_words.json', 'literary_resources/')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
splash = Splash(
    'splash.png',
    binaries=a.binaries,
    datas=a.datas,
    text_pos=None,
    text_size=12,
    minify_script=True,
    always_on_top=True,
)

exe = EXE(
    pyz,
    a.scripts,
    splash,
    [],
    exclude_binaries=True,
    name='lyrical',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='Icon.ico'
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    splash.binaries,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='lyrical',
)
