import time
from OBS import obsSceneTransition, obsSceneVLC
from subprocess import call
import os


def mpvPlayer():
    call('mpv --quiet --cursor-autohide=1 --cache=yes --demuxer-readahead-secs=20 --gapless-audio --force-window-position --geometry=0%:100% --write-filename-in-watch-later-config  >> mpvLog.txt --playlist playlistWithCommercials.pls', shell=True)




mpvPlayer()