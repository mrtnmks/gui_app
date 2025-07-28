# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=[],
    datas=[('requirements.txt', '.')],
    hiddenimports=[
        'tkinter', 
        'tkinter.ttk', 
        'tkinter.filedialog', 
        'tkinter.messagebox',
        'tkinter.constants',
        'tkinter.dialog',
        'tkinter.font',
        'tkinter.simpledialog',
        '_tkinter',
        'matplotlib.backends.backend_tkagg',
        'sklearn.utils._cython_blas',
        'sklearn.neighbors.typedefs',
        'sklearn.neighbors.quad_tree',
        'sklearn.tree._utils',
        'sklearn.utils._typedefs',
        'pandas._libs.window.aggregations',
        'pandas._libs.reduction',
        'pandas._libs.tslibs.base',
        'openpyxl',
        'seaborn'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='ClusterAnalysis',
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
)
