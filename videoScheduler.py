from apscheduler.schedulers.blocking import BlockingScheduler
#from videoPlaylist import playlist
from videoPlaylist import playlist
from OBS import obsSceneVLC
from nowPlaying import nowPlaying



scheduler = BlockingScheduler()
#scheduler.add_job(playlist, trigger='cron', hour='22', minute='25')
scheduler.add_job(videoPlaylist, trigger='cron', hour='15', minute='47')
#scheduler.add_job(cecPowerOn, trigger='cron', hour='08', minute='00')
#scheduler.add_job(cecInputNuc, trigger='cron', hour='08', minute='01')


scheduler.start()
