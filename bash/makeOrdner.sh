function Move()
{
  echo "Verschiebe '$1' nach '$2' ..."
  mkdir -p "$2"
  mv -v "$1" "$2/"
}

for FILENAME in *; do
  if [ "$FILENAME" = "makeOrdner.sh" ]; then continue; fi
  if [ -d "$FILENAME" ]; then continue; fi
  DIRNAME=$( echo "$FILENAME"  | sed -e "s/ vom [0-9]\+\. [A-Za-z]\+ [0-9]\+, [0-9-]\+ (.*)//;s/\.[A-Za-z]\+//" )
  echo "Quelle: $FILENAME"
  echo "Ziel: $DIRNAME"
  read -p "Verschieben(jnq)? " jn
  echo ""
  case "$jn" in
    j) Move "$FILENAME" "$DIRNAME";;
    n) ;;
    '') ;;
    q) exit ;;
    *) 
       DIRNAME="$jn"
       if [ -d "$DIRNAME" ]; then 
         Move "$FILENAME" "$DIRNAME";
       else
         read -n 1 -p "Verzeichniss '$DIRNAME' erstellen?" jn
         if [ "$jn" = "j" ]; then Move "$FILENAME" "$DIRNAME"; fi
       fi
       ;;
  esac
  echo ""
done
