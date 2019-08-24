import os
import signal
import subprocess
import pysftp
import pymysql
import time


dirname = os.path.dirname(__file__)
my_path = os.path.abspath(os.path.dirname(__file__))
absolute = os.path.abspath(os.getcwd())

myHostname = "142.93.129.123"
myUsername = "root"
myPassword = "mihica.909"
cnopts = pysftp.CnOpts()
cnopts.hostkeys = None
sftp = pysftp.Connection(host=myHostname, username=myUsername, password=myPassword, cnopts=cnopts)

conn = pymysql.connect(host='142.93.129.123', port=8000, user='root', password='mihica.909', database='songsDB')
cursor = conn.cursor()


morning = absolute + '/video/morning'
day = absolute + '/video/day'
commercials = absolute + '/video/commercials'
playlistFolder = absolute + '/video/'


def dayClock():
    cursor.execute("SELECT songName, attribute, fileLocation FROM songsDBFileLocation WHERE attribute = 'day' ORDER BY RAND() LIMIT 10")
    data = cursor.fetchall()
    sftp.cwd('/media/videos/day')
    cwd = os.getcwd()
    currentPath = (os.path.relpath(cwd))
    os.chdir(day)
    for x in data:
        os.chdir(absolute)
        song = x[0]
        attribute = x[1]
        fileLocation = (x[2])
        print(song + ", '" + attribute + "'" + ', ' + fileLocation)
        absoluteFileName = os.path.join(absolute + fileLocation)
        with open('playlist.pls', 'a',  encoding='utf-8') as playlist:
            # playlist.write('<track><location>' + absolute + fileLocation + '.mp4' + '</location></track>' + '\n')
            playlist.write((r'C:\Users\Mirko\PycharmProjects\videoPlayer_old\video\day/') + song + '.mp4' + '\n')
            localFilename = os.path.join(currentPath + fileLocation)
            localFilename = (localFilename[1:])
            localFilename = (os.path.basename(fileLocation))
            os.chdir(day)
            try:
                if os.path.isfile(localFilename + '.mp4'):
                    print('Song already downloaded.')
                    continue
                else:
                    sftp.get(localFilename)
                    os.rename(localFilename, localFilename + '.tmp')
            except IOError:
                pass

def morningClock():
    cursor.execute("SELECT songName, attribute, fileLocation FROM songsDBFileLocation WHERE attribute = 'morning' ORDER BY RAND() LIMIT 10")
    data = cursor.fetchall()
    sftp.cwd('/media/videos/morning')
    cwd = os.getcwd()
    currentPath = (os.path.relpath(cwd))
    os.chdir(morning)
    for x in data:
        os.chdir(absolute)
        song = x[0]
        attribute = x[1]
        fileLocation = (x[2])
        print(song + ", '" + attribute + "'" + ', ' + fileLocation)
        absoluteFileName = os.path.join(absolute + fileLocation)
        with open('playlist.pls', 'a',  encoding='utf-8') as playlist:
            # playlist.write('<track><location>' + absolute + fileLocation + '.mp4' + '</location></track>' + '\n')
            playlist.write((r'C:\Users\Mirko\PycharmProjects\videoPlayer_old\video\morning/') + song + '.mp4' + '\n')
            localFilename = os.path.join(currentPath + fileLocation)
            localFilename = (localFilename[1:])
            localFilename = (os.path.basename(fileLocation))
            os.chdir(morning)
            try:
                if os.path.isfile(localFilename + '.mp4'):
                    print('Song already downloaded.')
                    continue
                else:
                    sftp.get(localFilename)
                    os.rename(localFilename, localFilename + '.tmp')
            except IOError:
                pass


def commercialsClock():
    cursor.execute("SELECT songName, attribute, fileLocation FROM commercialsDBFileLocation WHERE attribute = 'commercial' ORDER BY RAND() LIMIT 1")
    data = cursor.fetchall()
    sftp.cwd('/media/videos/morning') ###PROMIJENITI U COMMERCIALS FOLDER
    cwd = os.getcwd()
    currentPath = (os.path.relpath(cwd))
    os.chdir(commercials)
    for x in data:
        os.chdir(absolute)
        song = x[0]
        attribute = x[1]
        fileLocation = (x[2])
        print(song + ", '" + attribute + "'" + ', ' + fileLocation)
        absoluteFileName = os.path.join(absolute + fileLocation)
        with open('commercials.pls', 'a',  encoding='utf-8') as commercialsList:
            # commercialsList.write('<track><location>' + absolute + fileLocation + '.mp4' + '</location></track>' + '\n')
            commercialsList.write((r'C:\Users\Mirko\PycharmProjects\videoPlayer_old\video\commercials/') + song + '.mp4' + '\n')
            localFilename = os.path.join(currentPath + fileLocation)
            localFilename = (localFilename[1:])
            localFilename = (os.path.basename(fileLocation))
            os.chdir(commercials)
            try:
                if os.path.isfile(localFilename + '.mp4'):
                    print('Song already downloaded.')
                    continue
                else:
                    sftp.get(localFilename)
                    os.rename(localFilename, localFilename + '.tmp')
            except IOError:
                pass


def deletePlaylist():
    os.chdir(absolute)
    open('playlist.pls', 'w').close()
    open('commercials.pls', 'w').close()
    try:
        os.remove(playlistFolder + 'playlistWithCommercials.m3u')
    except FileNotFoundError:
        pass

def insertCommercials():
    os.chdir(absolute)
    playlistList = [word.strip('\n').split(',') for word in open("playlist.pls", 'r').readlines()]
    commercialsList = [word.strip('\n').split(',') for word in open("commercials.pls", 'r').readlines()]
    playlistWithCommercials = [x for y in (playlistList[i:i + 6] + commercialsList * (i < len(playlistList) - 6) for i in range(0, len(playlistList), 6)) for x in y]
    print(playlistWithCommercials)
    with open(playlistFolder + 'playlistWithCommercials.m3u', 'a', encoding='utf-8') as outfile:
        for s in playlistWithCommercials:
            for line in s:
                outfile.write(str(line) + '\n')


def ffmpegConvert():
    os.chdir(absolute)
    subprocess.call('./ffmpeg.sh')


def deleteVideoFiles(folder):
    for file in os.listdir(folder):
        filePath = os.path.join(folder, file)
        try:
            if os.path.isfile(filePath):
                os.unlink(filePath)
        except Exception as e:
            pass


def deleteTempFiles(folder):
    for file in os.listdir(folder):
        filePath = os.path.join(folder, file)
        try:
            if file.endswith('.tmp'):
                if os.path.isfile(filePath):
                    os.unlink(filePath)
        except Exception as e:
            pass


def playlist():
    deletePlaylist()
    #deleteVideoFiles(morning)
    #deleteVideoFiles(day)
    #deleteVideoFiles(commercials)
    for _ in range(100):
        morningClock()
    for _ in range(100):
        dayClock()
    commercialsClock()
    insertCommercials()
    ffmpegConvert()
    time.sleep(3)
    deleteTempFiles(morning)
    deleteTempFiles(day)
    deleteTempFiles(commercials)

playlist()

