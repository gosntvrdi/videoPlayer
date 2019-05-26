from apscheduler.schedulers.blocking import BlockingScheduler
from videoPlaylist import playlist
from player import playerVLC
from OBS import obsSceneVLC




scheduler = BlockingScheduler()
scheduler.add_job(playlist, trigger='cron', hour='22', minute='25')
scheduler.add_job(mpvPlayer, trigger='cron', hour='00', minute='50')
#scheduler.add_job(cecPowerOn, trigger='cron', hour='08', minute='00')
#scheduler.add_job(cecInputNuc, trigger='cron', hour='08', minute='01')
#scheduler.add_job(obsSceneVLC, trigger='cron', hour='20', minute='17')
scheduler.start()
