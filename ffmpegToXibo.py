import os
from shutil import copyfile
import shutil
import pymysql
import time
import datetime
import subprocess
import sys
import hashlib
import requests
from operator import itemgetter
from ffprobe3 import FFProbe


# log = open("ffmpegToXibo.log", "a")
# sys.stdout = log

dirname = os.path.dirname(__file__)
my_path = os.path.abspath(os.path.dirname(__file__))
absolute = os.path.abspath(os.getcwd())

videoFileToDBSQL = "172.18.0.6"
xiboSQL = "172.18.0.2"


connVideoFileToDBSQL = pymysql.connect(host=videoFileToDBSQL, port=3306, user='root', password='mihica.909', database='songsDB')
connXiboSQL = pymysql.connect(host=xiboSQL, port=3306, user='cms', password='ge%tvB7h@9UW', database='cms')

cursorConnVideoFileToDBSQL = connVideoFileToDBSQL.cursor()
cursorConnXiboSQL = connXiboSQL.cursor()

morning = dirname + '/video/morning'
day = dirname + '/video/day'
commercials = dirname + '/video/commercials'



def convertFFmpeg():
    cursorConnVideoFileToDBSQL.execute("SELECT songName, attribute, fileLocation FROM songsDBFileLocation WHERE submarine = 0 ") #LIMIT 10
    data = cursorConnVideoFileToDBSQL.fetchall()
    for x in data:
        song = x[0]
        attribute = x[1]
        if attribute == 'morning':
            tagId = 6
        else:
            tagId = 7
        fileLocation = (x[2])
        metadata = FFProbe(fileLocation)
        fileSize = os.stat(fileLocation).st_size
        for stream in metadata.streams:
            try:
                duration = stream.duration_seconds()
                duration = int(round(duration))
            except Exception:
                duration = 0
        print(song + ", '" + attribute + "'" + ', ' + fileLocation + ', Duration: ' + str(duration))
        copyfile((fileLocation), ('/app' + fileLocation + '.tmp'))
        subprocess.call('./ffmpegContainer.sh')
        os.remove(('/app' + fileLocation + '.tmp'))
        shutil.move(('/app' + fileLocation + '.mp4'), ('/xiboLibrary/' + 'SUBMARINE-'+ song + '.mp4'))
        cursorConnVideoFileToDBSQL.execute("""INSERT INTO songsDBFileLocation (songName, attribute, fileLocation, submarine) VALUES (%s, %s, %s, %s)
                           ON DUPLICATE KEY UPDATE submarine = '1'""",
                       (song, attribute, fileLocation, '1'))
        print(song + ' converted and moved to ' + ('/xiboLibrary/' 'SUBMARINE-'+ song + '.mp4'))
        connVideoFileToDBSQL.commit()


        cursorConnXiboSQL.execute("SELECT mediaId, name, type, duration, originalFileName, storedAs, md5, fileSize, "
                                  "userId, retired, isEdited, editedMediaId, moduleSystemFile, valid, expires, released, "
                                  "apiRef, createdDt, modifiedDt  FROM media")
        xiboData = cursorConnXiboSQL.fetchall()
        mediaId = [xiboData[-1]]
        mediaId = mediaId[0]
        mediaId = mediaId[0]
        mediaId = mediaId + 1
        songXibo = ('SUBMARINE-'+ song + '.mp4')
        md5 = hashlib.md5(('/xiboLibrary/' 'SUBMARINE-' + song + '.mp4').encode('utf-8')).hexdigest()
        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        cursorConnXiboSQL.execute("""INSERT INTO media (mediaID, name, type, duration, originalFileName, storedAs, md5, fileSize,
                                    userId, retired, isEdited, editedMediaId, moduleSystemFile, valid, expires, released,
                                    apiRef, createdDt, modifiedDt)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                           (mediaId, songXibo, 'video', duration, songXibo, songXibo, md5, fileSize, 1, 0, 0, 0, 0, 1, 0, 1, 'NULL', timestamp, timestamp))
        cursorConnXiboSQL.execute("SELECT lkTagMediaId, tagId, mediaId FROM lktagmedia")
        xiboLkTagMedia = cursorConnXiboSQL.fetchall()
        try:
            lkTagMediaId = max(xiboLkTagMedia, key=itemgetter(0))[0]
            lkTagMediaId = lkTagMediaId + 1
        except ValueError:
            lkTagMediaId = 1
        cursorConnXiboSQL.execute("""INSERT INTO lktagmedia (lkTagMediaId, tagId, mediaId)
                            VALUES (%s, %s, %s)""",
                           (lkTagMediaId, tagId, mediaId))
        connXiboSQL.commit()

        #print(log)
    connVideoFileToDBSQL.close()
    connXiboSQL.close()


convertFFmpeg()

















# import requests, json
# from pprint import pprint
#
# library = 'http://142.93.129.123:7000/api/library'
# clock = 'http://142.93.129.123:7000/api/clock'
# tokenUrl = 'http://142.93.129.123:7000/api/authorize/access_token'
# clientId = 'Jyat3oCKJC2XY8moaUknm2aGebO77qr1jdHoRJnL'
# clientSecret = '4e2mR6XthEtlWi0tZ4cloEy88500yuKVO5ZkRSHSssklh3vhSfOSzd8FZFj66AxNukYIoztTivRUx0wsAlcDLyJrxs89MabahB3TLrSMrBsadZHiuOlVTZbygCn44EfCj0d1jAAEJWSChieu68EYlum9V79bO9x3QHmuGqrk2jS328CYAzc5bDxmSSfNBTwhJCsOLlp248kDxIzVqTdJx36mdw6l3ZexbAi8gw1Usw5fT9sNSXxkZC8CYkvLyl'
# data = {'grant_type': 'client_credentials'}
# access_token_response = requests.post(tokenUrl, data=data, verify=False, allow_redirects=False, auth=(clientId, clientSecret))
# tokens = json.loads(access_token_response.text)
# headers = {
# 'Authorization': 'Bearer ' + tokens['access_token'],
# 'Cache-Control': 'no-cache',
# }
#
#
# mediaIdResponse = requests.get(library, headers=headers)
# mediaId = json.loads(mediaIdResponse.text)
# sortedMediaId = sorted(mediaId, key=itemgetter('mediaId'))
# sortedMediaIdJSON = (json.dumps(sortedMediaId, indent=4))
# print(sortedMediaIdJSON)
#print(mediaId[-1])
#Upload File
# payload = “------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=“files”; filename=“C:\test.JPG”\r\nContent-Type: image/jpeg\r\n\r\n\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=“name”\r\n\r\nCTV_Sendung\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=“oldMediaId”\r\n\r\n156\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=“updateInLayouts”\r\n\r\n1\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=“deleteOldRevisions”\r\n\r\n1\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW–”
#
# headers = {
# 'content-type': “multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW”,
# 'Cache-Control': “no-cache”,
# 'Content-Type': “application/json”,
# 'Postman-Token': “a7c524e4-dac6-442c-8387-f9c7605cd1a8”,
# }
#
# response = requests.request(“POST”, url1, data=payload, headers=headers)
#print(response.text)














# import requests, json
# from pprint import pprint
#
# library = 'http://142.93.129.123:7000/api/library'
# clock = 'http://142.93.129.123:7000/api/clock'
# tokenUrl = 'http://142.93.129.123:7000/api/authorize/access_token'
# clientId = 'Jyat3oCKJC2XY8moaUknm2aGebO77qr1jdHoRJnL'
# clientSecret = '4e2mR6XthEtlWi0tZ4cloEy88500yuKVO5ZkRSHSssklh3vhSfOSzd8FZFj66AxNukYIoztTivRUx0wsAlcDLyJrxs89MabahB3TLrSMrBsadZHiuOlVTZbygCn44EfCj0d1jAAEJWSChieu68EYlum9V79bO9x3QHmuGqrk2jS328CYAzc5bDxmSSfNBTwhJCsOLlp248kDxIzVqTdJx36mdw6l3ZexbAi8gw1Usw5fT9sNSXxkZC8CYkvLyl'
# data = {'grant_type': 'client_credentials'}
# access_token_response = requests.post(tokenUrl, data=data, verify=False, allow_redirects=False, auth=(clientId, clientSecret))
# tokens = json.loads(access_token_response.text)
# headers = {
# 'Authorization': 'Bearer ' + tokens['access_token'],
# 'Cache-Control': 'no-cache',
# }
#
#
# mediaIdResponse = requests.get(library, headers=headers)
# mediaId = json.loads(mediaIdResponse.text)
# sortedMediaId = sorted(mediaId, key=itemgetter('mediaId'))
# sortedMediaIdJSON = (json.dumps(sortedMediaId, indent=4))
# print(sortedMediaIdJSON)
#print(mediaId[-1])
#Upload File
# payload = “------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=“files”; filename=“C:\test.JPG”\r\nContent-Type: image/jpeg\r\n\r\n\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=“name”\r\n\r\nCTV_Sendung\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=“oldMediaId”\r\n\r\n156\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=“updateInLayouts”\r\n\r\n1\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=“deleteOldRevisions”\r\n\r\n1\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW–”
#
# headers = {
# 'content-type': “multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW”,
# 'Cache-Control': “no-cache”,
# 'Content-Type': “application/json”,
# 'Postman-Token': “a7c524e4-dac6-442c-8387-f9c7605cd1a8”,
# }
#
# response = requests.request(“POST”, url1, data=payload, headers=headers)
#print(response.text)




