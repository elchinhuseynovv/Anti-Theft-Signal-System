import PyInstaller.__main__
import os

# Get the absolute path of the script
script_path = os.path.abspath("main.py")

PyInstaller.__main__.run([
    script_path,
    '--name=Anti-Theft-System',
    '--onefile',
    '--windowed',
    '--icon=icon.ico',  # Optional: Add if you have an icon
    '--add-data=alerts.csv;.',  # Include the CSV file
    '--hidden-import=matplotlib',
    '--hidden-import=tkinter',
    '--hidden-import=csv',
    '--clean'
])