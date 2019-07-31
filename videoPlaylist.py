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
    cursor.execute("SELECT songName, attribute, fileLocation FROM songsDBFileLocation WHERE attribute = 'day' ORDER BY RAND() LIMIT 10")
    data = cursor.fetchall()
    sftp.cwd('/media/videos/day')
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
        with open('playlist.pls', 'a', encoding='utf-8') as playlist:
            playlist.write('<track><location>' + absoluteFileName + '</location></track>' + '\n')
            localFilename = os.path.join(currentPath + fileLocation)
            localFilename = (localFilename[1:])
            localFilename = (os.path.basename(fileLocation))
            os.chdir(day)
            try:
                sftp.get(localFilename)
            except IOError:
                pass

def morningClock():
    cursor.execute("SELECT songName, attribute, fileLocation FROM songsDBFileLocation WHERE attribute = 'morning' ORDER BY RAND() LIMIT 12")
    data = cursor.fetchall()
    sftp.cwd('/media/videos/morning')
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
        with open('playlist.pls', 'a',  encoding='utf-8') as playlist:
            playlist.write('<track><location>' + absoluteFileName + '</location></track>' + '\n')
            localFilename = os.path.join(currentPath + fileLocation)
            localFilename = (localFilename[1:])
            localFilename = (os.path.basename(fileLocation))
            os.chdir(morning)
            try:
                sftp.get(localFilename)
            except IOError:
                pass


def commercialsClock():
    cursor.execute("SELECT songName, attribute, fileLocation FROM commercialsDBFileLocation WHERE attribute = 'commercial' ORDER BY RAND() LIMIT 2")
    data = cursor.fetchall()
    sftp.cwd('/media/videos/commercials')
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
        with open('commercials.pls', 'a', encoding='utf-8') as commercialsList:
            commercialsList.write('<track><location>' + absoluteFileName + '</location></track>' + '\n')
            localFilename = os.path.join(currentPath + fileLocation)
            localFilename = (localFilename[1:])
            localFilename = (os.path.basename(fileLocation))
            os.chdir(commercials)
            try:
                sftp.get(localFilename)
            except IOError:
                pass


def deletePlaylist():
    os.chdir(dirname)
    open('playlist.pls', 'w').close()
    open('commercials.pls', 'w').close()
    try:
        os.remove('playlistWithCommercials.xspf')
    except FileNotFoundError:
        pass

def insertCommercials():
    os.chdir(dirname)
    playlistList = [word.strip('\n').split(',') for word in open("playlist.pls", 'r').readlines()]
    commercialsList = [word.strip('\n').split(',') for word in open("commercials.pls", 'r').readlines()]
    playlistWithCommercials = [x for y in (playlistList[i:i + 6] + commercialsList * (i < len(playlistList) - 6) for i in range(0, len(playlistList), 6)) for x in y]
    print(playlistWithCommercials)
    with open('playlistWithCommercials.xspf', 'a', encoding='utf-8') as outfile:
        outfile.write('<playlist version="1" xmlns="http://xspf.org/ns/0/" xmlns:vlc="http://www.videolan.org/vlc/playlist/ns/0/"><title>Playlist</title><trackList>' + '\n')
        for s in playlistWithCommercials:
            for line in s:
                outfile.write(str(line) + '\n')
        outfile.write('</trackList></playlist>')


def killOBS():
    os.system('ps -C obs -o pid=|xargs kill -9')


def runOBS():
    subprocess.call('obs')

def playlist():
    killOBS()
    deletePlaylist()
    deleteVideoFiles(morning)
    deleteVideoFiles(day)
    deleteVideoFiles(commercials)
    #for _ in range(12):
    morningClock()
    #for _ in range(24):
    dayClock()
    commercialsClock()
    insertCommercials()
    time.sleep(3)
    runOBS()


playlist()