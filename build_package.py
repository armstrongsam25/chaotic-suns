"""Setup script for building Chaotic Suns with PyInstaller."""
import os
import sys
import shutil

# Clean previous builds
for d in ['build', 'dist', 'ChaoticSuns_*.zip']:
    if os.path.exists(d):
        if os.path.isdir(d):
            shutil.rmtree(d)
        else:
            os.remove(d)
    # Also handle glob
    import glob
    for f in glob.glob(d):
        if os.path.isfile(f):
            os.remove(f)

# Build the spec
spec_content = """# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('src/', 'src/'),
        ('requirements.txt', '.'),
    ],
    hiddenimports=['pygame', 'numpy', 'src.nbody', 'src.renderer', 'src.civilization',
                   'src.audio', 'src.menu', 'src.lore', 'src.save_system',
                   'src.progression', 'src.prediction', 'src.effects', 'src.starfield',
                   'src.events', 'src.fleet', 'src.tech_tree', 'src.achievements',
                   'src.scenario_select'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

# Default: console-friendly (shows print/logs but also supports NOFRAME for testing)
# For production: use Window=True to hide console
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='ChaoticSuns',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Set to False for Windows release builds
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
"""

with open('ChaoticSuns.spec', 'w') as f:
    f.write(spec_content)

print("Spec file written. Run: pyinstaller ChaoticSuns.spec")
print("\nAfter build, the dist/ChaoticSuns/ folder is the distributable.")