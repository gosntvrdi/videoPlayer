
import vlc
import time
import subprocess

def playerVLC():
    proces = subprocess.Popen(['obs'])
    proces
    time.sleep(5)
    from OBS import obsSceneTransition, obsSceneVLC
    playlist = '/home/luka/PycharmProjects/videoPlayer_old/playlistWithCommercials.pls'
    with open(playlist, 'r') as f:
        playlist=[i for line in f for i in line.split(',')]
        playlist = map(lambda s: s.strip(), playlist)
    instance = vlc.Instance(
            "--quiet " +
            "--no-xlib " +
            "--vout=opengl " +
            "--avcodec-threads=0")
    player = instance.media_player_new()
    playing = set([1,2,3,4])
    for i in playlist:
        obsSceneVLC()
        player.set_mrl(i)
        player.play()
        play=True
        while play == True:
            time.sleep(1)
            play_state = player.get_state()
            if play_state in playing:
                continue
            else:
                obsSceneTransition()
                play = False

playerVLC()




