import requests
import json

tokenUrl = 'http://142.93.129.123:7000/api/authorize/access_token'
library = 'http://142.93.129.123:7000/api/library'
mainUrl = 'http://142.93.129.123:7000/api/user'
clientId = 'CLcHDq4WOoUfB9VtNWZeSz1TTV1zya3yu6eYcBqE'
clientSecret = '7eemAx8c9PPmFrwPyeAc91RjSc5HzsplpwURXyrNhPMseHcUNJj9d3M0iqOCMCNnWO3tfIgqbx4Ljt8gElJlT4UCYDax6SktryA1qFv6BvnmY34e5bBcAEa6zB1zIHzjaCA44O0vdIAofW73vr8KWlgwoQECotfYqXb1iZrAdAWihsuQqoYEgQgPC0oqhgjNWWc8LyONMjzq26k1FtPINnTwLnX9lPOzIZqYLHOGiMddDv6KTT4c8LRzHFJgWD'

data = {'grant_type':'client_credentials'}
access_token_response = requests.post(tokenUrl,data=data,verify=False,allow_redirects=False,auth=(clientId, clientSecret))
tokens = json.loads(access_token_response.text)
print ('Bearer ' + tokens['access_token'])

#querystring = {'media':'video'}
#headers = {'Authorization': "Bearer " + tokens['access_token'],'Cache-Control':'no-cache','content-type': 'multipart/form-data'}
#response = requests.request('GET',library,data=data,headers=headers)
#responseLibrary = json.loads(response.text)


#headers = {'Authorization': "Bearer " + tokens['access_token'],'Cache-Control':'no-cache','content-type': 'multipart/form-data'}


import requests

url = "http://142.93.129.123:7000/api/library"

payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"files\"; filename=\"C:/Users/lukab.SOONIK2/PycharmProjects/videoPlayer_old2/app/videos/morning/SUBMARINE-Aaron Neville featuring Robbie Robertson - Crazy Love.mp4\"\r\nContent-Type: video/mp4\r\n\r\n\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"name\"\r\n\r\nnesto\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"updateInLayouts\"\r\n\r\n1\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--"
headers = {
    'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
    'Authorization': "Bearer B6u3nmy2xCXnlS48kidGSfdsRueSVrRkvthCSsGe",
    'User-Agent': "PostmanRuntime/7.15.2",
    'Accept': "*/*",
    'Cache-Control': "no-cache",
    'Postman-Token': "498a27cb-3855-4bb9-a030-9892464c74a9,6527056c-ac52-4f54-a7ca-e8b92b5af5cc",
    'Host': "142.93.129.123:7000",
    'Cookie': "PHPSESSID=fv8b4h5470lohu7b7nb5kjkpps",
    'Accept-Encoding': "gzip, deflate",
    'Content-Type': "multipart/form-data; boundary=--------------------------319929371879600350995198",
    'Content-Length': "4454011",
    'Connection': "keep-alive",
    'cache-control': "no-cache"
    }

response = requests.request("POST", url, data=payload, headers=headers)

print(response.text)