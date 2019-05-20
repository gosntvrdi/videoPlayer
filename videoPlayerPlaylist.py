import mysql.connector as mariadb
import ftplib
import os


dirname = os.path.dirname(__file__)
my_path = os.path.abspath(os.path.dirname(__file__))

conn = mariadb.connect(host='192.168.150.251', user='videostream', password='mirko', database='songsDB')
cursor = conn.cursor(buffered=True)

morning = 'video/morning'
day = 'video/day'


def deleteVideoFiles(folder):
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            pass


def dayClock():
    cursor.execute("SELECT songName, attribute, fileLocation FROM songsDBFileLocation WHERE attribute = 'day' ORDER BY RAND() LIMIT 240")
    data = cursor.fetchall()
    ftp = ftplib.FTP('192.168.150.251', 'videostream', 'yammatFM102.5')
    ftp.cwd('/04-PUBLIC/LUKA/videoplayer/video/day')
    cwd = os.getcwd()
    print(cwd)
    currentPath = (os.path.relpath(cwd))
    os.chdir(day)
    for x in data:
        os.chdir(dirname)
        song = x[0]
        attribute = x[1]
        fileLocation = x[2]
        print(song + ", '" + attribute + "'" + ', ' + fileLocation)
        with open('playlist.pls', 'a') as playlist:
            playlist.write(fileLocation + '\n')
            localFilename = os.path.join(currentPath + fileLocation)
            localFilename = (localFilename[1:])
            localFilename = (os.path.basename(fileLocation))
            os.chdir(day)
            try:
                with open(localFilename, "wb") as file: ftp.retrbinary("RETR " + localFilename, file.write)
            except ftplib.error_perm:
                pass

def morningClock():
    cursor.execute("SELECT songName, attribute, fileLocation FROM songsDBFileLocation WHERE attribute = 'morning' ORDER BY RAND() LIMIT 120")
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
        fileLocation = x[2]
        print(song + ", '" + attribute + "'" + ', ' + fileLocation)
        with open('playlist.pls', 'a') as playlist:
            playlist.write(fileLocation + '\n')
            localFilename = os.path.join(currentPath + fileLocation)
            localFilename = (localFilename[1:])
            localFilename = (os.path.basename(fileLocation))
            os.chdir(morning)
            try:
                with open(localFilename, "wb") as file: ftp.retrbinary("RETR " + localFilename, file.write)
            except ftplib.error_perm:
                pass

def deletePlaylist():
    os.chdir(dirname)
    open('playlist.pls', 'w').close()


def playlistPrepareForVLC():
    os.chdir(dirname)
    with open('playlist.pls') as fp:
        lines = fp.read().splitlines()
    with open('playlist.pls', "w") as fp:
        for line in lines:
            print(dirname + line, file=fp)


def playlist():
    deletePlaylist()
    deleteVideoFiles(morning)
    deleteVideoFiles(day)
    morningClock()
    for _ in range(50):
        dayClock()
    playlistPrepareForVLC()


