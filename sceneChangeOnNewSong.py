from OBS import scene, scene2
import pyinotify
import time

def sceneChange(ev):
    scene2()
    time.sleep(6)
    scene()

wm = pyinotify.WatchManager()
wm.add_watch('nowPlaying.txt', pyinotify.IN_MODIFY, sceneChange)
notifier = pyinotify.Notifier(wm)
notifier.loop()
