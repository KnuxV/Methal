#!/usr/bin/env bash
PTHORIG=../out/oscar_with_characters.xml
FNINDIV=hart-01.xml
FNGRP=hart-dr-poetisch-oscar.xml
PUBREPODIR=/home/ruizfabo/te/stra/re/theatre_alsacien/demos/heb_pfingstmontag/unistra-methal-sources
PTHINDIV=$PUBREPODIR/indiv/methal-sources/$FNINDIV
PTHGRP=$PUBREPODIR/group/methal-sources/$FNGRP

cp $PTHORIG $PTHINDIV
cp $PTHORIG $PTHGRP

