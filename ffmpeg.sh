#!/bin/sh

for f in /home/videostream/PycharmProjects/videoPlayer_old/video/morning/*.tmp;
do
   ffmpeg -i "$f" -i /home/videostream/PycharmProjects/videoPlayer_old/logo/lower.avi -i /home/videostream/PycharmProjects/videoPlayer_old/logo/logo.png -filter_complex \
      "[0:v]scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:x=(1280-iw)/2:y=(720-ih)/2:color=black[bg0]; \
      [bg0][1:v]overlay=10:10[bg1]; \
      [bg1][2:v]overlay=10:10,drawtext=fontfile=/logo/BebasNeue-Regular.otf:text=$(basename "$f" | cut -f 1 -d '.'):fontcolor=white:fontsize=14::x=120:y=H-th-83:enable='between(t,0,5)" \
      -c:v libx264 -preset ultrafast "${f%.*}.mp4"
done

for f in /home/videostream/PycharmProjects/videoPlayer_old/video/day/*.tmp;
do
   ffmpeg -i "$f" -i /home/videostream/PycharmProjects/videoPlayer_old/logo/lower.avi -i /home/videostream/PycharmProjects/videoPlayer_old/logo/logo.png -filter_complex \
      "[0:v]scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:x=(1280-iw)/2:y=(720-ih)/2:color=black[bg0]; \
      [bg0][1:v]overlay=10:10[bg1]; \
      [bg1][2:v]overlay=10:10,drawtext=fontfile=/logo/BebasNeue-Regular.otf:text=$(basename "$f" | cut -f 1 -d '.'):fontcolor=white:fontsize=14::x=120:y=H-th-83:enable='between(t,0,5)" \
      -c:v libx264 -preset ultrafast "${f%.*}.mp4"
done

for f in /home/videostream/PycharmProjects/videoPlayer_old/video/commercials/*.tmp;
do
   ffmpeg -i "$f" -i /home/videostream/PycharmProjects/videoPlayer_old/logo/lower.avi -i /home/videostream/PycharmProjects/videoPlayer_old/logo/logo.png -filter_complex \
      "[0:v]scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:x=(1280-iw)/2:y=(720-ih)/2:color=black[bg0]; \
      [bg0][1:v]overlay=10:10[bg1]; \
      [bg1][2:v]overlay=10:10,drawtext=fontfile=/logo/BebasNeue-Regular.otf:text=$(basename "$f" | cut -f 1 -d '.'):fontcolor=white:fontsize=14::x=120:y=H-th-83:enable='between(t,0,5)" \
      -c:v libx264 -preset ultrafast "${f%.*}.mp4"
done