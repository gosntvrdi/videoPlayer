import os
import pyinotify,subprocess




def nowPlaying(ev):
    with open('mpvLog.txt', 'r') as f:
        lines = f.read().splitlines()
        if 'Playing:' in lines[-3]:
            np = lines[-3]
        elif 'Playing:' in lines[-4]:
            np = lines[-4]
        elif 'Playing:' in lines[-9]:
            np = lines[-9]
        else:
            np = lines[-5]
        np = (np[9:])
        np = (os.path.basename(np).split('.')[0])
        print(np)
    with  open('nowPlaying.txt', 'w') as f:
        f.write(np)




wm = pyinotify.WatchManager()
wm.add_watch('mpvLog.txt', pyinotify.IN_MODIFY, nowPlaying)
notifier = pyinotify.Notifier(wm)
notifier.loop()