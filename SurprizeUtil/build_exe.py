import os
import sys
import subprocess

def build_with_pyinstaller():
    print("Building with PyInstaller...")
    subprocess.call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    subprocess.call([sys.executable, "-m", "PyInstaller", "--onefile", "--windowed", "src/main.py", "--name", "Surprize"])
    print("PyInstaller build completed!")

def build_with_cx_freeze():
    print("Building with cx_Freeze...")
    subprocess.call([sys.executable, "-m", "pip", "install", "cx_Freeze"])
    subprocess.call([sys.executable, "setup.py", "build"])
    print("cx_Freeze build completed!")

def build_with_nuitka():
    print("Building with Nuitka...")
    subprocess.call([sys.executable, "-m", "pip", "install", "nuitka"])
    subprocess.call([sys.executable, "-m", "nuitka", "--follow-imports", "--windows-disable-console", "--standalone", "src/main.py"])
    print("Nuitka build completed!")

def main():
    print("=== Surprize Application Builder ===")
    print("1. Build with PyInstaller (recommended)")
    print("2. Build with cx_Freeze")
    print("3. Build with Nuitka")
    
    choice = input("Select build method (1-3): ")
    
    if choice == "1":
        build_with_pyinstaller()
    elif choice == "2":
        build_with_cx_freeze()
    elif choice == "3":
        build_with_nuitka()
    else:
        print("Invalid choice. Exiting.")

if __name__ == "__main__":
    main()
