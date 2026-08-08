# -*- mode: python ; coding: utf-8 -*-

from pathlib import Path

from PyInstaller.utils.hooks import collect_submodules

ROOT = Path.cwd()


block_cipher = None


a = Analysis(
    ["tools/packaged_backend.py"],
    pathex=[str(ROOT)],
    binaries=[],
    datas=[
        (str(ROOT / "apps"), "apps"),
        (str(ROOT / "config"), "config"),
        (str(ROOT / "templates"), "templates"),
        (str(ROOT / "static"), "static"),
        (str(ROOT / "requirements.txt"), "."),
    ],
    hiddenimports=[
        "apps.catalogo",
        "apps.catalogo.apps",
        "apps.catalogo.views",
        "apps.clientes",
        "apps.clientes.apps",
        "apps.financeiro",
        "apps.financeiro.apps",
        "apps.legacy_migration",
        "apps.legacy_migration.apps",
        "apps.pedidos",
        "apps.pedidos.apps",
        "psycopg",
        "psycopg_binary",
        "PIL",
        "decouple",
    ]
    + collect_submodules("cryptography")
    + collect_submodules("openpyxl")
    + collect_submodules("reportlab"),
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

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="mheibos-backend",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="mheibos-backend",
)
