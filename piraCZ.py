import subprocess


subprocess.Popen(['C:\Program Files (x86)\Pira CZ Silence Detector\\piraside.exe'], shell = True)


import os
import shutil

dir = 'video/morning'
files = os.listdir(dir)

for file in files:
    try:
        os.rename(file, file)
    except:
        print(file + ' is being played in OBS')
