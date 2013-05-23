#!/bin/bash

# screen -dmS gcr /home/woems/Scripte/bash/git-commit-reminder.sh

function git_gui()
{
  echo "## git gui"
  echo "tooltip: GCR: gui" >&3
  git gui
  echo "--RET: $?"
}

function git_push_pull()
{
  echo "## git pull"
  echo "tooltip: GCR: pull" >&3
  git pull
  echo "--RET: $?"
  echo "## git mergetool -y"
  echo "tooltip: GCR: mergetool" >&3
  git mergetool -y
  echo "--RET: $?"
  echo "## git commit -m 'Merge'"
  echo "tooltip: GCR: commit merge" >&3
  git commit -m "Merge"
  echo "--RET: $?"
  echo "## git push -u origin master"
  echo "tooltip: GCR: push" >&3
  git push -u origin master
  echo "--RET: $?"
}

function add_config_xml()
{
  echo "tooltip: GCR: config.xml" >&3
  if git status | grep "modified:.*config.xml" > /dev/null; then
    xmlstarlet ed -L -d "/UserScriptConfig/Script/@installTime" -d "/UserScriptConfig/Script/@lastUpdateCheck" -d "/UserScriptConfig/Script/@modified" -d "/UserScriptConfig/Script/@uuid" config.xml
    git add config.xml ; git commit -m "config"
  fi
}

function show_modified()
{
   git status | grep "\(modified\|Untracked\)" | grep -v "$Ignor" | wc -l
}


exec 3> >(zenity --notification --listen)

GitArchive="$HOME/.mozilla/firefox/azua9l03.default/gm_scripts"
if [ ! -d "$GitArchive" ]; then GitArchive="$HOME/.mozilla/firefox/vkuuxfit.default/gm_scripts"; fi
if [ ! -d "$GitArchive" ]; then echo "gm_scripts nicht gefunden"; exit; fi
ScriptRun="./cleanup.sh"
Ignor="config"

cd "$GitArchive"

git_push_pull

while true
do
  pwd
  AnzMod=$(show_modified)
  echo "$(date) - Mod: $AnzMod"
  echo "tooltip: GCR: mod: $AnzMod" >&3
  if [ $AnzMod -ge 1 ]; then
    echo "MODIFIED"
    $(sleep 1 && wmctrl -a Frage -b add,above)&
    RET=$(zenity --question --text "$AnzMod Dateien wurden modifiziert. Commiten?")
    if [ $? -eq 0 ]; then
      add_config_xml
      git_gui
      AnzMod=$(show_modified)
      echo "$AnzMod"
      if [ $AnzMod -eq 0 ]; then
        git_push_pull
      fi
    fi
  fi
  echo "tooltip: GCR: 10 min warten..." >&3
  echo "Wait for 10 min... (STRG+C zum abbrechen)"
  sleep 600
  #read -n 1 -p "Beliebige Taste zum fortfahren" -t 600
  # sec => 1h=60*60=3600
  #echo ""
done

exec 3>&-
