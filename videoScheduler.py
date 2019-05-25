from apscheduler.schedulers.blocking import BlockingScheduler
from videoPlaylist import playlist
from player import playerVLC
from OBS import obsSceneVLC




scheduler = BlockingScheduler()
scheduler.add_job(obsSceneVLC, trigger='cron', hour='20', minute='17')
scheduler.add_job(playlist, trigger='cron', hour='21', minute='12')
#scheduler.add_job(cecPowerOn, trigger='cron', hour='08', minute='00')
#scheduler.add_job(cecInputNuc, trigger='cron', hour='08', minute='01')
scheduler.add_job(playerVLC, trigger='cron', hour='21', minute='11')
scheduler.start()
