import os
import time

dirname = os.path.dirname(__file__)
morningDir = dirname + '/video/morning'
os.chdir(morningDir)


def np():
    i=1
    for file in os.listdir():
        src=file
        dst=file
        try:
            os.rename(src,dst)
        except:
            print(file + ' is being played in OBS')
            os.chdir(dirname)
            with  open('nowPlaying.txt', 'w') as f:
                f.write(file)
            os.chdir(morningDir)
        i+=1


start_time = time.time()
interval = 1
for i in range(20):
    time.sleep(start_time + i*interval - time.time())
    np()