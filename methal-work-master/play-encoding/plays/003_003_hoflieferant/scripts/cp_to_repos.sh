#!/usr/bin/env bash
PTHORIG=../hoflieferant_with_characters.xml
FNINDIV=stoskopf-02.xml
FNGRP=stoskopf-dr-hoflieferant.xml
PUBREPODIR=/home/ruizfabo/te/stra/re/theatre_alsacien/demos/heb_pfingstmontag/unistra-methal-sources
PTHINDIV=$PUBREPODIR/indiv/methal-sources/$FNINDIV
PTHGRP=$PUBREPODIR/group/methal-sources/$FNGRP

cp $PTHORIG $PTHINDIV
cp $PTHORIG $PTHGRP

