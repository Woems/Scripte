#!/bin/bash
DVDDIR="$HOME/dvd"
mkdir "$DVDDIR"
echo "**********************************"
echo "* Erstelle Backup                *"
echo "**********************************"
eject -t
if ! dvdbackup -M -i /dev/dvd -o "$DVDDIR" ; then
  echo BACKUP FEHLGESCHLAGEN
  exit
fi
eject
SUBDIR=$(find "$DVDDIR" -name "VIDEO_TS.IFO" | sed "s/.*\/\([^/]*\)\/VIDEO_TS\/[^/]*$/\1/" )
echo "**********************************"
echo "* Erstelle CD                    *"
echo "**********************************"
if ! mkisofs -dvd-video -udf -o "$DVDDIR/$SUBDIR.iso" "$DVDDIR/$SUBDIR" ; then
  echo ISO erstellen FEHLGESCHLAGEN
  exit
fi
rm -R "$DVDDIR/$SUBDIR"
