import pymysql
import time
from shutil import *
import os
import datetime
from updatePlaylist import update


ts = time.time()
timestamp = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y %H:%M:%S')
dst =  '/opt/project/video/playlistFiles/'

for the_file in os.listdir(dst):
    file_path = os.path.join(dst, the_file)
    try:
        if os.path.isfile(file_path):
            os.unlink(file_path)
    except Exception as e:
        print(e)


conn = pymysql.connect(host='142.93.129.123', port=8000, user='root', password='mihica.909', database='songsDB')
cursor = conn.cursor()



def morningClock():
    ID = 100
    cursor.execute("""DELETE from submarinePlaylist""")
    while ID < 250:
        cursor.execute("SELECT songName, attribute, fileLocation FROM songsDBFileLocation WHERE attribute = 'morning' ORDER BY RAND() LIMIT 4")
        data = cursor.fetchall()
        for x in data:
            song = x[0]
            attribute = x[1]
            fileLocation = (x[2])
            cursor.execute("""INSERT INTO submarinePlaylist (ID, songName, attribute, added, fileLocation) VALUES (%s, %s, %s, %s, %s)""", (ID, song, attribute, timestamp, fileLocation))
            ID = ID + 1
            # src = '/opt/project' + fileLocation + '.mp4'
            # try:
            #     copy2(src, dst +  str(ID) + '-' + song + '.mp4')
            # except (FileNotFoundError, IOError) as e:
            #     continue



        cursor.execute("SELECT songName, attribute, fileLocation FROM commercialsDBFileLocation WHERE attribute = 'commercial' ORDER BY RAND() LIMIT 4")
        data = cursor.fetchall()
        for x in data:
            song = x[0]
            attribute = x[1]
            fileLocation = (x[2])
            cursor.execute("""INSERT INTO submarinePlaylist (ID, songName, attribute, added, fileLocation) VALUES (%s, %s, %s, %s, %s)""", (ID, song, attribute, timestamp, fileLocation))
            ID = ID + 1
            conn.commit()
            # src = '/opt/project' + fileLocation + '.mp4'
            # try:
            #     copy2(src, dst +  str(ID) + '-' + song + '.mp4')
            # except (FileNotFoundError, IOError) as e:
            #     continue
            conn.commit()
    update()

morningClock()

