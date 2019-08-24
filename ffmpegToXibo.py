import os
from shutil import copyfile
import pymysql
import time
import subprocess


dirname = os.path.dirname(__file__)
my_path = os.path.abspath(os.path.dirname(__file__))
absolute = os.path.abspath(os.getcwd())

videoFileToDBSQL = "172.17.0.3"
#xiboSQL = "142.93.129.123"

connVideoFileToDBSQL = pymysql.connect(host=videoFileToDBSQL, port=3306, user='root', password='mihica.909', database='songsDB')
#connXiboSQL = pymysql.connect(host=xiboSQL, port=5000, user='root', password='mihica.909', database='songsDB')

cursorConnVideoFileToDBSQL = connVideoFileToDBSQL.cursor()
#cursorConnXiboSQL = connXiboSQL.cursor()

morning = dirname + '/video/morning'
day = dirname + '/video/day'
commercials = dirname + '/video/commercials'


def convertFFmpeg():
    cursorConnVideoFileToDBSQL.execute("SELECT songName, attribute, fileLocation FROM songsDBFileLocation WHERE FFmpeg = 1 ") #LIMIT 10
    data = cursorConnVideoFileToDBSQL.fetchall()
    for x in data:
        song = x[0]
        attribute = x[1]
        fileLocation = (x[2])
        print(song + ", '" + attribute + "'" + ', ' + fileLocation)
        copyfile((fileLocation), (dirname + fileLocation + '.tmp'))
        subprocess.call('./ffmpegContainer.sh')
        os.remove((convertedFileLocation + fileLocation + '.tmp'))

convertFFmpeg()