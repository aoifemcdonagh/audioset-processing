# NOT USED here for reference

#!/bin/bash

# Script for downloading audio clips (10s) from Youtube using AudioSet CSV datasets

SAMPLE_RATE=22050

# fetch_clip(videoID, startTime, endTime)
fetch_clip() {
  echo "Fetching $1 ($2 to $3)..."
  outname="$1_$2"
  if [ -f "${outname}.wav.gz" ]; then
    echo "Already have it."
    return
  fi

  if [ $? -eq 0 ]; then
    # i.e. if we haven't found this file
    ffmpeg -loglevel quiet -ss "$2" -t 10 \
        -i $(youtube-dl -f 'bestaudio' --get-url https://youtube.com/watch?v=$1) \
        -ar $SAMPLE_RATE \
        "./$outname.wav"
   else
    sleep 1
   fi
}

# iterate through the input piped into script
grep -E '^[^#]' | while read line
do
  fetch_clip $(echo "$line" | sed -E 's/,/ /g')
done