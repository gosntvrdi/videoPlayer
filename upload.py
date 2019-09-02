import json
import pymysql
import requests


tokenUrl = 'http://142.93.129.123:7000/api/authorize/access_token'
clientId = 'CLcHDq4WOoUfB9VtNWZeSz1TTV1zya3yu6eYcBqE'
clientSecret = '7eemAx8c9PPmFrwPyeAc91RjSc5HzsplpwURXyrNhPMseHcUNJj9d3M0iqOCMCNnWO3tfIgqbx4Ljt8gElJlT4UCYDax6SktryA1qFv6BvnmY34e5bBcAEa6zB1zIHzjaCA44O0vdIAofW73vr8KWlgwoQECotfYqXb1iZrAdAWihsuQqoYEgQgPC0oqhgjNWWc8LyONMjzq26k1FtPINnTwLnX9lPOzIZqYLHOGiMddDv6KTT4c8LRzHFJgWD'
data = {'grant_type': 'client_credentials'}
access_token_response = requests.post(tokenUrl, data=data, verify=False, allow_redirects=False,
                                      auth=(clientId, clientSecret))
tokens = json.loads(access_token_response.text)

xiboSQL = "172.18.0.2"
connXiboSQL = pymysql.connect(host=xiboSQL, port=3306, user='cms', password='ge%tvB7h@9UW', database='cms')
cursorConnXiboSQL = connXiboSQL.cursor()


def updateLayouts():
    cursorConnXiboSQL.execute("SELECT layoutId, layout FROM layout")
    xiboData = cursorConnXiboSQL.fetchall()
    submarineMorningLayout = [xiboData[-1]]
    submarineMorningLayout = submarineMorningLayout[0]
    submarineMorningLayout = submarineMorningLayout[0]

    # url = "http://142.93.129.123:7000/api/layout/publish/" + submarineMorningLayout
    # payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"layoutId\"\r\n\r\n24\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"downloadRequired\"\r\n\r\ntrue\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"changeMode\"\r\n\r\nqueue\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--"
    # headers = {
    #     'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
    #     'Authorization': "Bearer 99TzhK4iS000CCiotqGcAxq7ZWBS86tyZqQfeK74",
    #     'User-Agent': "PostmanRuntime/7.15.2",
    #     'Accept': "*/*",
    #     'Cache-Control': "no-cache",
    #     'Postman-Token': "c243698b-2485-46b3-aa70-41a183292742,5ee6002d-0bf9-4987-98ee-beece84d0cbd",
    #     'Host': "142.93.129.123:7000",
    #     'Cookie': "PHPSESSID=fv8b4h5470lohu7b7nb5kjkpps",
    #     'Accept-Encoding': "gzip, deflate",
    #     'Content-Type': "multipart/form-data; boundary=--------------------------043169685718713921615634",
    #     'Content-Length': "398",
    #     'Connection': "keep-alive",
    #     'cache-control': "no-cache"
    #     }
    # response = requests.request("PUT", url, data=payload, headers=headers)
    # print(response.text)
    # submarineMorningLayout = submarineMorningLayout + 1
    # url = "http://142.93.129.123:7000/api/layout/checkout/" + submarineMorningLayout
    # payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"layoutId\"\r\n\r\n24\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"downloadRequired\"\r\n\r\ntrue\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"changeMode\"\r\n\r\nqueue\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--"
    # headers = {
    #     'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
    #     'Authorization': "Bearer 99TzhK4iS000CCiotqGcAxq7ZWBS86tyZqQfeK74",
    #     'User-Agent': "PostmanRuntime/7.15.2",
    #     'Accept': "*/*",
    #     'Cache-Control': "no-cache",
    #     'Postman-Token': "c243698b-2485-46b3-aa70-41a183292742,306dc17b-54d0-4a69-b812-739f6996b065",
    #     'Host': "142.93.129.123:7000",
    #     'Cookie': "PHPSESSID=fv8b4h5470lohu7b7nb5kjkpps",
    #     'Accept-Encoding': "gzip, deflate",
    #     'Content-Type': "multipart/form-data; boundary=--------------------------043169685718713921615634",
    #     'Content-Length': "398",
    #     'Connection': "keep-alive",
    #     'cache-control': "no-cache"
    #     }
    # response = requests.request("PUT", url, data=payload, headers=headers)
    # print(response.text)
    # connXiboSQL.close()

