import os
import sys
import subprocess

def main():
    print("=== Building Surprize Application with PyInstaller ===")
    
    # Install PyInstaller if not already installed
    subprocess.call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # Build the executable
    subprocess.call([
        sys.executable, "-m", "PyInstaller",
        "--onefile",              # Create a single executable file
        "--windowed",             # Do not show console window
        "--clean",                # Clean PyInstaller cache
        "--noconfirm",            # Replace output directory without asking
        "--name", "Surprize",     # Name of the executable
        "src/main.py"             # Script to package
    ])
    
    print("\nBuild completed!")
    print(f"Executable can be found in: {os.path.abspath('dist/Surprize.exe')}")

if __name__ == "__main__":
    main()
