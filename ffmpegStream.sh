#!/bin/sh


for f in /media/video/playlistFiles/*.mp4;
do
	ffmpeg -re -i "${f}" -c copy -f flv "rtmp://127.0.0.1/live"
done

