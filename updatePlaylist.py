import pymysql
import time
from shutil import *
import os
import datetime

###napraviti dugme na webu da pokrene ovu funkciju nakon izmjene playliste u phpmyadminu

ts = time.time()
timestamp = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y %H:%M:%S')
dst =  '/opt/project/video/playlistFiles/'

# for the_file in os.listdir(dst):
#     file_path = os.path.join(dst, the_file)
#     try:
#         if os.path.isfile(file_path):
#             os.unlink(file_path)
#     except Exception as e:
#         print(e)


conn = pymysql.connect(host='142.93.129.123', port=8000, user='root', password='mihica.909', database='songsDB')
cursor = conn.cursor()



def update():
    #ID = 1
    cursor.execute("SELECT ID, songName, attribute, added, fileLocation FROM submarinePlaylist ORDER BY ID")
    data = cursor.fetchall()
    for x in data:
        ID = x[0]
        song = x[1]
        attribute = x[2]
        fileLocation = (x[4])
        src = '/opt/project' + fileLocation + '.mp4'
        try:
            copy2(src, dst + str(ID) + '-' + song + '.mp4')
        except (FileNotFoundError, IOError) as e:
            continue
        #ID = ID + 1



update()

