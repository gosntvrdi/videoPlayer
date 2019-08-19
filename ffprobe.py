from ffprobe3 import FFProbe
import datetime
import time
from datetime import date, datetime, time, timedelta
import os
import pandas as pd
from sqlalchemy import create_engine
from pandas.io import sql


def formatResult(result):
    seconds = int(result)
    microseconds = (result * 1000000) % 1000000
    output = timedelta(0, seconds, microseconds)
    return output


videos = [line.rstrip('\n') for line in open('/opt/project/video/playlistWithCommercials.m3u')]
with open ('playlistDuration.txt', 'w') as f:
    secondsAdded = 0
    dt = datetime.combine(date.today(), time(4, 00))
    for video in videos:
        metadata=FFProbe(video)
        for stream in metadata.streams:
            if stream.is_video():
                seconds = stream.duration_seconds()
                secondsAdded = seconds + secondsAdded
                f.write('\n' + video + ';' + str(formatResult(seconds)) + ';' + str(formatResult(secondsAdded)) + '\n')


pd.DataFrame = [line.rstrip('\n') for line in open('/opt/project/playlistDuration.txt')]
df =  pd.read_csv('/opt/project/playlistDuration.txt', sep=';', engine='python')
df.columns = ['Song', 'Duration', 'Playtime at']


engine = create_engine('mysql://root:mihica.909@142.93.129.123:8000/songsDB')
with engine.connect() as conn, conn.begin():
    df.to_sql('submarinePlaylist', conn, if_exists='replace')