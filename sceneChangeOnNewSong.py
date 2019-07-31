from OBS import scene, scene2
import pyinotify
import time

def sceneChange(ev):
    scene2()



wm = pyinotify.WatchManager()
wm.add_watch('nowPlaying.txt', pyinotify.IN_CLOSE_WRITE, sceneChange)
notifier = pyinotify.Notifier(wm)
notifier.loop()
