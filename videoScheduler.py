from apscheduler.schedulers.blocking import BlockingScheduler
#from videoPlaylist import playlist
from player import mpvPlayer
from OBS import obsSceneVLC
from nowPlaying import nowPlaying



scheduler = BlockingScheduler()
#scheduler.add_job(playlist, trigger='cron', hour='22', minute='25')
scheduler.add_job(mpvPlayer, trigger='cron', hour='20', minute='46')
#scheduler.add_job(cecPowerOn, trigger='cron', hour='08', minute='00')
#scheduler.add_job(cecInputNuc, trigger='cron', hour='08', minute='01')


scheduler.start()
