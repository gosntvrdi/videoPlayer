import mysql.connector as mariadb
import ftplib
import os
#from apscheduler.schedulers.blocking import BlockingScheduler
#from OBS import obsSceneVLC
import sys

#reload(sys)
#sys.setdefaultencoding('utf-8')

dirname = os.path.dirname(__file__)
my_path = os.path.abspath(os.path.dirname(__file__))
absolute = os.path.abspath(os.getcwd())


conn = mariadb.connect(host='192.168.150.251', user='videostream', password='mirko', database='songsDB')
cursor = conn.cursor(buffered=True)

morning = dirname + '/video/morning'
day = dirname + '/video/day'
commercials = dirname + '/video/commercials'

def deleteVideoFiles(folder):
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            pass


def dayClock():
    cursor.execute("SELECT songName, attribute, fileLocation FROM songsDBFileLocation WHERE attribute = 'day' ORDER BY RAND() LIMIT 12")
    data = cursor.fetchall()
    ftp = ftplib.FTP('192.168.150.251', 'videostream', 'yammatFM102.5')
    ftp.cwd('/04-PUBLIC/LUKA/videoplayer/video/day')
    cwd = os.getcwd()
    currentPath = (os.path.relpath(cwd))
    os.chdir(day)
    for x in data:
        os.chdir(dirname)
        song = x[0]
        attribute = x[1]
        fileLocation = (x[2])
        print(song + ", '" + attribute + "'" + ', ' + fileLocation)
        absoluteFileName = os.path.join(absolute + fileLocation)
        with open('playlist.pls', 'a') as playlist:
            playlist.write(absoluteFileName + '\n')
            localFilename = os.path.join(currentPath + fileLocation)
            localFilename = (localFilename[1:])
            localFilename = (os.path.basename(fileLocation))
            os.chdir(day)
            try:
                with open(localFilename, "wb") as file: ftp.retrbinary("RETR " + localFilename, file.write)
            except ftplib.error_perm:
                pass

def morningClock():
    cursor.execute("SELECT songName, attribute, fileLocation FROM songsDBFileLocation WHERE attribute = 'morning' ORDER BY RAND() LIMIT 12")
    data = cursor.fetchall()
    ftp = ftplib.FTP('192.168.150.251', 'videostream', 'yammatFM102.5')
    ftp.cwd('/04-PUBLIC/LUKA/videoplayer/video/morning')
    cwd = os.getcwd()
    currentPath = (os.path.relpath(cwd))
    os.chdir(morning)
    for x in data:
        os.chdir(dirname)
        song = x[0]
        attribute = x[1]
        fileLocation = (x[2])
        print(song + ", '" + attribute + "'" + ', ' + fileLocation)
        absoluteFileName = os.path.join(absolute + fileLocation) 
        with open('playlist.pls', 'a') as playlist:
            playlist.write(absoluteFileName + '\n')
            localFilename = os.path.join(currentPath + fileLocation)
            localFilename = (localFilename[1:])
            localFilename = (os.path.basename(fileLocation))
            os.chdir(morning)
            try:
                with open(localFilename, "wb") as file: ftp.retrbinary("RETR " + localFilename, file.write)
            except ftplib.error_perm:
                pass


def commercialsClock():
    cursor.execute("SELECT songName, attribute, fileLocation FROM commercialsDBFileLocation WHERE attribute = 'commercial' ORDER BY RAND() LIMIT 3")
    data = cursor.fetchall()
    ftp = ftplib.FTP('192.168.150.251', 'videostream', 'yammatFM102.5')
    ftp.cwd('/04-PUBLIC/LUKA/videoplayer/video/commercials')
    cwd = os.getcwd()
    currentPath = (os.path.relpath(cwd))
    os.chdir(commercials)
    for x in data:
        os.chdir(dirname)
        song = x[0]
        attribute = x[1]
        fileLocation = (x[2])
        print(song + ", '" + attribute + "'" + ', ' + fileLocation)
        absoluteFileName = os.path.join(absolute + fileLocation)
        with open('commercials.pls', 'a') as commercialsList:
            commercialsList.write(absoluteFileName + '\n')
            localFilename = os.path.join(currentPath + fileLocation)
            localFilename = (localFilename[1:])
            localFilename = (os.path.basename(fileLocation))
            os.chdir(commercials)
            try:
                with open(localFilename, "wb") as file: ftp.retrbinary("RETR " + localFilename, file.write)
            except ftplib.error_perm:
                pass


def deletePlaylist():
    os.chdir(dirname)
    open('playlist.pls', 'w').close()
    open('commercials.pls', 'w').close()
    open('playlistWithCommercials.pls', 'w').close()


def insertCommercials():
    os.chdir(dirname)
    playlistList = [word.strip('\n').split(',') for word in open("playlist.pls", 'r').readlines()]
    commercialsList = [word.strip('\n').split(',') for word in open("commercials.pls", 'r').readlines()]
    playlistWithCommercials = [x for y in (playlistList[i:i + 6] + commercialsList * (i < len(playlistList) - 2) for i in range(0, len(playlistList), 3)) for x in y]
    print(playlistWithCommercials)
    with open('playlistWithCommercials.pls', mode="w") as outfile:
        for s in playlistWithCommercials:
            for line in s:
                outfile.write(str(line) + '\n')




def playlist():
    deletePlaylist()
    deleteVideoFiles(morning)
    deleteVideoFiles(day)
    deleteVideoFiles(commercials)
    for _ in range(1):
        morningClock()
    for _ in range(1):
        dayClock()
    commercialsClock()
    insertCommercials()



# scheduler = BlockingScheduler()
# scheduler.add_job(obsSceneVLC, trigger='cron', hour='03', minute='00')
# scheduler.add_job(playlist, trigger='cron', hour='11', minute='25')
# scheduler.start()

