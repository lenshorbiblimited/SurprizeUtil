import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
    "packages": ["os", "tkinter", "psutil", "qrcode", "PIL"],
    "include_files": [],
    "excludes": ["unittest", "email", "html", "http", "xml", "pydoc_data"],
    "optimize": 2,
}

# GUI applications require a different base on Windows
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="Surprize",
    version="1.0",
    description="Многофункциональная утилита Surprize",
    options={"build_exe": build_exe_options},
    executables=[Executable("src/main.py", base=base, target_name="Surprize.exe", icon=None)]
)
