import os
import time
import sys
import time
import pyinotify


video = 'video'

class MyEventHandler(pyinotify.ProcessEvent):
    def process_IN_OPEN(selfself, event):
        np = (os.path.basename(event.pathname))
        if np == 'morning':
            pass
        elif np == 'day':
            pass
        elif np == 'commercials':
            pass
        else:
            with  open('nowPlaying.txt', 'w') as f:
                f.write(np)
                print(np)

def main():

    wm = pyinotify.WatchManager()
    wm.add_watch(video, pyinotify.IN_OPEN, rec=True)
    eh = MyEventHandler()
    notifier = pyinotify.Notifier(wm, eh)
    notifier.loop()

if __name__ == '__main__':
    main()