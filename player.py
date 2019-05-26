import time
from OBS import obsSceneTransition, obsSceneVLC
from subprocess import call
import os


def mpvPlayer():
    call('mpv --quiet --gapless-audio --write-filename-in-watch-later-config  >> mpvLog.txt --playlist playlistWithCommercials.pls', shell=True)




mpvPlayer()