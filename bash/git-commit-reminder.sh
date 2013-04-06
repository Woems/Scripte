#!/bin/bash

GitArchive="$HOME/.mozilla/firefox/azua9l03.default/gm_scripts"
if [ ! -d "$GitArchive" ]; then GitArchive="$HOME/.mozilla/firefox/vkuuxfit.default/gm_scripts"; fi
if [ ! -d "$GitArchive" ]; then echo "gm_scripts nicht gefunden"; exit; fi
ScriptRun="./cleanup.sh"
Ignor="config"

while true
do
  cd "$GitArchive"
  pwd
  AnzMod=$(git status | grep "modified" | grep -v "$Ignor" | wc -l)
  echo "$(date) - Mod: $AnzMod"
  if [ $AnzMod -ge 1 ]; then
    echo "MODIFIED"
    $(sleep 1 && wmctrl -a Frage -b add,above)&
    RET=$(zenity --question --text "$AnzMod Dateien wurden modifiziert. Commiten?")
    if [ $? -eq 0 ]; then
      if git status | grep "modified:.*config.xml" > /dev/null; then
        xmlstarlet ed -L -d "/UserScriptConfig/Script/@installTime" -d "/UserScriptConfig/Script/@lastUpdateCheck" -d "/UserScriptConfig/Script/@modified" -d "/UserScriptConfig/Script/@uuid" config.xml
        git add config.xml ; git commit -m "config"
      fi
      echo "## git gui"
      git gui
      echo "--RET: $?"
      AnzMod=$(git status | grep "modified" | grep -v "$Ignor" | wc -l)
      echo "$AnzMod"
      if [ $AnzMod -eq 0 ]; then
        echo "## git pull"
        git pull
        echo "--RET: $?"
        echo "## git mergetool -y"
        git mergetool -y
        echo "--RET: $?"
        echo "## git commit -m 'Merge'"
        git commit -m "Merge"
        echo "--RET: $?"
        echo "## git push -u origin master"
        git push -u origin master
        echo "--RET: $?"
      fi
    fi
  fi
  echo "Wait for 10 min... (STRG+C zum abbrechen)"
  sleep 600
  #read -n 1 -p "Beliebige Taste zum fortfahren" -t 600
  # sec => 1h=60*60=3600
  #echo ""
done
