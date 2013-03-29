#!/bin/bash
function resizeall()
{
  DIR=$1$2
  mkdir -p "$DIR"
  mkdir -p "Übersicht"
  for i in *.JPG; do
    echo "- $i"
    convert "$i" -normalize -resize $1% -quality $2% "$DIR/$i"
    #identify "$i"
    #identify "$DIR/$i"
  done
  du -hS "$DIR"
  #montage -label %f -geometry 400x300+10+10 "$DIR/*.JPG" "Übersicht/$DIR.pdf"
  montage -auto-orient -shadow -page a4 -tile 4x "$DIR/*.JPG" "Übersicht/$DIR.pdf"
}

resizeall 30 90
#resizeall 10 80
