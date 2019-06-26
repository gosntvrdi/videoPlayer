import mysql.connector as mariadb
import os
import pysftp


dirname = os.path.dirname(__file__)
my_path = os.path.abspath(os.path.dirname(__file__))
absolute = os.path.abspath(os.getcwd())

myHostname = "142.93.129.123"
myUsername = "root"
myPassword = "mihica.909"
cnopts = pysftp.CnOpts()
cnopts.hostkeys = None
sftp = pysftp.Connection(host=myHostname, username=myUsername, password=myPassword, cnopts=cnopts)

conn = mariadb.connect(host='142.93.129.123', port='8000', user='root', password='mihica.909', database='songsDB', auth_plugin='mysql_native_password', connection_timeout=3)
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
    cursor.execute("SELECT songName, attribute, fileLocation FROM songsDBFileLocation WHERE attribute = 'day' ORDER BY RAND() LIMIT 30")
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
        with open('playlist.pls', 'a') as playlist:
            playlist.write(absoluteFileName + '\n')
            localFilename = os.path.join(currentPath + fileLocation)
            localFilename = (localFilename[1:])
            localFilename = (os.path.basename(fileLocation))
            os.chdir(day)
            try:
                sftp.get(localFilename)
            except IOError:
                pass

def morningClock():
    cursor.execute("SELECT songName, attribute, fileLocation FROM songsDBFileLocation WHERE attribute = 'morning' ORDER BY RAND() LIMIT 50")
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
        with open('playlist.pls', 'a') as playlist:
            playlist.write(absoluteFileName + '\n')
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
        with open('commercials.pls', 'a') as commercialsList:
            commercialsList.write(absoluteFileName + '\n')
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
    open('playlistWithCommercials.pls', 'w').close()


def insertCommercials():
    os.chdir(dirname)
    playlistList = [word.strip('\n').split(',') for word in open("playlist.pls", 'r').readlines()]
    commercialsList = [word.strip('\n').split(',') for word in open("commercials.pls", 'r').readlines()]
    playlistWithCommercials = [x for y in (playlistList[i:i + 6] + commercialsList * (i < len(playlistList) - 6) for i in range(0, len(playlistList), 6)) for x in y]
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
    #for _ in range(12):
    morningClock()
    #for _ in range(24):
    dayClock()
    commercialsClock()
    insertCommercials()


playlist()