import os
from shutil import copyfile
import shutil
import pymysql
import time
import subprocess
import sys
import hashlib
import requests


log = open("ffmpegToXibo.log", "a")
sys.stdout = log

dirname = os.path.dirname(__file__)
my_path = os.path.abspath(os.path.dirname(__file__))
absolute = os.path.abspath(os.getcwd())

videoFileToDBSQL = "142.93.129.123"
xiboSQL = "142.93.129.123"


connVideoFileToDBSQL = pymysql.connect(host=videoFileToDBSQL, port=8000, user='root', password='mihica.909', database='songsDB')
connXiboSQL = pymysql.connect(host=xiboSQL, port=5000, user='cms', password='mihica.909', database='cms')

cursorConnVideoFileToDBSQL = connVideoFileToDBSQL.cursor()
cursorConnXiboSQL = connXiboSQL.cursor()

morning = dirname + '/video/morning'
day = dirname + '/video/day'
commercials = dirname + '/video/commercials'


def convertFFmpeg():
    cursorConnVideoFileToDBSQL.execute("SELECT songName, attribute, fileLocation FROM songsDBFileLocation WHERE FFmpeg = 0 ") #LIMIT 10
    data = cursorConnVideoFileToDBSQL.fetchall()
    for x in data:
        song = x[0]
        attribute = x[1]
        fileLocation = (x[2])
        print(song + ", '" + attribute + "'" + ', ' + fileLocation)
        copyfile((fileLocation), ('/app' + fileLocation + '.tmp'))
        subprocess.call('./ffmpegContainer.sh')
        os.remove(('/app' + fileLocation + '.tmp'))
        cursorConnVideoFileToDBSQL.execute("""INSERT INTO songsDBFileLocation (songName, attribute, fileLocation, FFmpeg) VALUES (%s, %s, %s, %s)
                           ON DUPLICATE KEY UPDATE FFmpeg = '1'""",
                       (song, attribute, fileLocation, '1'))
        shutil.move(('/app' + fileLocation + '.mp4'), ('/xiboLibrary/' + 'SUBMARINE-'+ song + '.mp4'))
        print(song + ' converted and moved to ' + ('/xiboLibrary/' 'SUBMARINE-'+ song + '.mp4'))
        connVideoFileToDBSQL.commit()

        md5 = hashlib.md5(('/xiboLibrary/' 'SUBMARINE-'+ song + '.mp4').encode('utf-8')).hexdigest()
        cursorConnXiboSQL.execute(
            "SELECT mediaId, name, type, duration, originalFileName, storedAs, md5, fileSize, userId, retired, isEdited, editedMediaId, moduleSystemFile, valid, expires, released, apiRef, createdDt, modifiedDt  FROM media") ####ORDER BY mediaId DESC LIMIT 1 ")
        xiboData = cursorConnXiboSQL.fetchall()
        for y in xiboData:
            print(y)



        cursorConnXiboSQL("""INSERT INTO songsDB (songName, attribute, added, downloaded) VALUES (%s, %s, %s, %s)
                           ON DUPLICATE KEY UPDATE downloaded = '1'""",
                       (song, attribute, timestamp, '1'))
        connXiboSQL.commit()
        print(log)
    connVideoFileToDBSQL.close()
    connXiboSQL.close()


#convertFFmpeg()






