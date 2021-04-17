#!/usr/bin/env bash

# copy relevant material to 'work' directory of public repos

DATA=../data
ORIG=../sources
TEI=..
LOGS=../logs

TEIINITIAL=${TEI}/create_tei.py
TEIFINAL=${TEI}/add_characters_to_tei.py
RUN=${TEI}/encode.sh
DRACORIZER=${TEI}/dracorizer.py

PTHINDIV=/home/ruizfabo/te/stra/re/theatre_alsacien/demos/heb_pfingstmontag/unistra-methal-sources/indiv/methal-sources
PTHGRP=/home/ruizfabo/te/stra/re/theatre_alsacien/demos/heb_pfingstmontag/unistra-methal-sources/group/methal-sources

SINDIV=$PTHINDIV/work/stoskopf-02-dr-hoflieferant
SGRP=$PTHGRP/work/stoskopf-dr-hoflieferant

for dname in $SINDIV $SGRP; do
    #echo $dname
    [[ ! -d $dname ]] && mkdir -p $dname
    #[[ ! -d $dname/${TEI} ]] && mkdir -p $dname/${TEI}
    cp -r $DATA $dname/.
    cp -r $LOGS $dname/.
    for sdname in $ORIG ; do
      cp -r $sdname $dname/.
    done
    for fname in $TEIINITIAL $TEIFINAL $RUN $DRACORIZER; do
        bfname=$(basename $fname)
      cp $fname $dname/$bfname
    done
done

TEIBASIC=../hoflieferant.xml
TEIFINAL=../hoflieferant_with_characters.xml
TEIDRACOR=../hoflieferant_with_characters_dracor.xml

for fname in $TEIBASIC $TEIFINAL $TEIDRACOR; do
    for dname in $SINDIV $SGRP; do
        bfname=$(basename $fname)
        cp $fname ${dname}/${bfname}
    done
done

cp ../README.md $SINDIV
cp ../README.md $SGRP
#cp ../README-work.md $(dirname ${SINDIV})/README.md
#cp ../README-work.md $(dirname ${SGRP})/README.md
