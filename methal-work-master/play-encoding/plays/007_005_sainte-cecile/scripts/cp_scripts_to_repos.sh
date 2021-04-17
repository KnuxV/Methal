#!/usr/bin/env bash

# copy relevant material to 'work' directory of public repos

DATA=../data
ORIG=../sources
TEI=../
OUT=../out
LOGS=../logs

CREATE_TEIINITIAL=${TEI}/create_tei.py
CREATE_TEIFINAL=${TEI}/add_characters.py
CONFIG=${TEI}/config.py
RUN=${TEI}/encode.sh
DRACORIZER=${TEI}/dracorizer.py

PTHINDIV=/home/ruizfabo/te/stra/re/theatre_alsacien/demos/heb_pfingstmontag/unistra-methal-sources/indiv/methal-sources
PTHGRP=/home/ruizfabo/te/stra/re/theatre_alsacien/demos/heb_pfingstmontag/unistra-methal-sources/group/methal-sources

SINDIV=$PTHINDIV/work/plays/greber-01-sainte-cecile
SGRP=$PTHGRP/work/plays/greber-sainte-cecile

SAVEIFS=$IFS
IFS=$(echo -en "\n\b")

for dname in $SINDIV $SGRP; do
    #echo $dname
    [[ ! -d $dname ]] && mkdir -p $dname
    #[[ ! -d $dname/${TEI} ]] && mkdir -p $dname/${TEI}
    [[ ! -d $dname/out ]] && mkdir -p $dname/out
    [[ ! -d $dname/logs ]] && mkdir -p $dname/logs
    cp -r $DATA $dname/.
    for xname in $(ls $LOGS); do
      if [[ -z $(echo "$LOGS/$xname" | grep -P "(diff_stage)") ]]; then
        cp "$LOGS/$xname" "$dname/logs/$xname"
      fi
    done
    for xname in $(ls $OUT); do
      if [[ -z $(echo "$OUT/$xname" | grep -P "(bak|copy|test)") ]]; then
        cp "$OUT/$xname" "$dname/out/$xname"
      fi
    done
    for sdname in $ORIG ; do
      cp -r $sdname $dname/.
    done
    for fname in $CREATE_TEIINITIAL $CREATE_TEIFINAL $CONFIG; do
        bfname=$(basename $fname)
      cp $fname $dname/$bfname
    done
done

IFS=$SAVEIFS

TEIBASIC=../out/sainte-cecile.xml
CREATE_TEIFINAL=../out/sainte-cecile_with_characters.xml
#TEIDRACOR=../hoflieferant_with_characters_dracor.xml

for fname in $TEIBASIC $CREATE_TEIFINAL; do
    for dname in $SINDIV $SGRP; do
        bfname=$(basename $fname)
        cp $fname ${dname}/out/${bfname}
    done
done

cp ../README.md $SINDIV
cp ../README.md $SGRP
#cp ../README-work.md $(dirname ${SINDIV})/README.md
#cp ../README-work.md $(dirname ${SGRP})/README.md
