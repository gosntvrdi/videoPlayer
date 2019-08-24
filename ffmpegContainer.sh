#!/bin/sh

for f in submarine/video/morning/*.tmp;
do
   ffmpeg -i "${f}" -i logo/lower.mov -i logo/logo.png -filter_complex \
      "[0:v]scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:x=(1280-iw)/2:y=(720-ih)/2:color=black[bg0]; \
      [bg0][1:v]overlay=10:10,drawtext=fontfile=logo/Courier Prime.ttf:text=$(basename "${f}" | cut -f 1 -d '.'): \
	  fontcolor=white:fontsize=25:x=256:y=h-th-130:alpha=1:enable='between(t,2,15)'" \
      -c:v libx264 -crf 21 -preset fast "${f%.*}.mp4"
done

for f in submarine/video/day/*.tmp;
do
   ffmpeg -i "${f}" -i logo/lower.mov -i logo/logo.png -filter_complex \
      "[0:v]scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:x=(1280-iw)/2:y=(720-ih)/2:color=black[bg0]; \
      [bg0][1:v]overlay=10:10,drawtext=fontfile=logo/Courier Prime.ttf:text=$(basename "${f}" | cut -f 1 -d '.'): \
	  fontcolor=white:fontsize=25:x=256:y=h-th-130:alpha=1:enable='between(t,2,15)'" \
      -c:v libx264 -crf 21 -preset fast "${f%.*}.mp4"
done

for f in submarine/video/commercials/*.tmp;
do
   ffmpeg -i "${f}" -i logo/lower.mov -i logo/logo.png -filter_complex \
      "[0:v]scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:x=(1280-iw)/2:y=(720-ih)/2:color=black[bg0]; \
      [bg0][1:v]overlay=10:10,drawtext=fontfile=logo/Courier Prime.ttf:text=$(basename "${f}" | cut -f 1 -d '.'): \
	  fontcolor=white:fontsize=25:x=256:y=h-th-130:alpha=1:enable='between(t,2,15)'" \
      -c:v libx264 -crf 21 -preset fast "${f%.*}.mp4"
done
