# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller spec for compare_pdfs.exe (Windows one-folder distribution)."""

from PyInstaller.utils.hooks import collect_data_files, collect_dynamic_libs

block_cipher = None

# Collect hidden imports and data files for dependencies
pypdfium2_datas = collect_data_files("pypdfium2")
pypdfium2_bins = collect_dynamic_libs("pypdfium2")
openpyxl_datas = collect_data_files("openpyxl")
pdfminer_datas = collect_data_files("pdfminer")

a = Analysis(
    ["compare_pdfs.py"],
    pathex=[],
    binaries=pypdfium2_bins,
    datas=pypdfium2_datas + openpyxl_datas + pdfminer_datas + [("config.yaml", ".")],
    hiddenimports=[
        "pypdfium2",
        "pypdfium2._helpers",
        "pypdfium2.raw",
        "pdfminer",
        "pdfminer.high_level",
        "pdfminer.layout",
        "numpy",
        "cv2",
        "yaml",
        "openpyxl",
    ],
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
    name="compare_pdfs",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    version="version_info.txt",
    icon="compare_pdfs.ico",
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="compare_pdfs",
)
