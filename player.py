import time
from OBS import obsSceneTransition, obsSceneVLC
from subprocess import call

def mpvPlayer():
    call('mpv --quiet --gapless-audio --playlist playlistWithCommercials.pls', shell=True)

mpvPlayer()