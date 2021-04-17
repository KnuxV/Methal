#!/usr/bin/env bash
PTHORIG=../out/hofnarr_heidideldum_with_characters.xml
FNINDIV=bastian-01.xml
FNGRP=bastian-hofnarr-heidideldum.xml
PUBREPODIR=/home/ruizfabo/te/stra/re/theatre_alsacien/demos/heb_pfingstmontag/unistra-methal-sources
PTHINDIV=$PUBREPODIR/indiv/methal-sources/$FNINDIV
PTHGRP=$PUBREPODIR/group/methal-sources/$FNGRP

cp $PTHORIG $PTHINDIV
cp $PTHORIG $PTHGRP

sed -i -e 's/"..\/..\/..\/css\/tei-drama.css"/"work\/css\/tei-drama.css"/g' $PTHINDIV
sed -i -e 's/"..\/..\/..\/css\/tei-drama.css"/"work\/css\/tei-drama.css"/g' $PTHGRP