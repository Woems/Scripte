INPUT="PSIS-02.wmv"
OUTPUT="$INPUT.2.avi"
rm frameno.avi
mencoder "$INPUT" -ovc lavc -lavcopts threads=4:vcodec=mpeg4:vpass=1 -oac copy -o "$OUTPUT"
mencoder "$INPUT" -ovc lavc -lavcopts threads=4:vcodec=mpeg4:vpass=2 -oac copy -o "$OUTPUT"
