#!/bin/bash

find . -name "*.jpg" -exec mv {} . \;
find . -name "*.png" -exec mv {} . \;
find . -type d -exec rmdir {} \; > /dev/null


for i in *.{jpg,jpeg,png}
do
  if [ -f "$i" ]; then
    width=$(identify -format "%w" "$i")
    height=$(identify -format "%h" "$i")
    wh=$(identify -format "%wx%h" "$i" | sed 's/[0-9]\{2\}x\([0-9]*\)[0-9]\{2\}$/00x\100/g')
    size=$(($width*$height/100000*100))
    dir=""
    echo -n "$i ($width $height)"
    if [ $width -gt $height ]; then
      echo "Breit"
      mkdir -p "breit/$dir"
      mv "$i" "breit/$dir"
    else
      echo "HOCH"
      mkdir -p "hoch/$dir"
      mv "$i" "hoch/$dir"
    fi
  fi
done
