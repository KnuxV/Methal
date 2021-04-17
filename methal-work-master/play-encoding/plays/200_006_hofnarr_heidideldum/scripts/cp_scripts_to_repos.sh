#!/usr/bin/env bash

# copy relevant material to 'work' directory of public repos

DATA=../data
ORIG=../sources
TEI=../
#UTILS=../utils
CSS=../css
OUT=../out
LOGS=../logs

CREATE_TEIINITIAL=${TEI}/create_tei.py
CREATE_TEIFINAL=${TEI}/add_characters.py
CONFIG=${TEI}/config.py
OCONFIG=${TEI}/oconfig.py
#FRONT=${TEI}/add_to_front.py
VERSE=${TEI}/verse.py
PP=${TEI}/play_parsing.py
RUN=${TEI}/encode.sh
DRACORIZER=${TEI}/dracorizer.py

PTHINDIV=/home/ruizfabo/te/stra/re/theatre_alsacien/demos/heb_pfingstmontag/unistra-methal-sources/indiv/methal-sources
PTHGRP=/home/ruizfabo/te/stra/re/theatre_alsacien/demos/heb_pfingstmontag/unistra-methal-sources/group/methal-sources

SINDIV=$PTHINDIV/work/plays/bastian-01-hofnarr-heidideldum
SGRP=$PTHGRP/work/plays/bastian-hofnarr-heidideldum

SAVEIFS=$IFS
IFS=$(echo -en "\n\b")

for dname in $SINDIV $SGRP; do
    #echo $dname
    [[ ! -d $dname ]] && mkdir -p $dname
    #[[ ! -d $dname/${TEI} ]] && mkdir -p $dname/${TEI}
    mkdir $dname/out
    #mkdir $dname/utils
    mkdir $dname/data
    #cp -r $DATA $dname/.
    cp -r $LOGS $dname/.
    #cp -r $UTILS $dname/.
    cp -r $CSS $dname/.
    for xname in $(ls $OUT); do
      if [[ -z $(echo "$OUT/$xname" | grep -P "(bak|copy|test|dracor|corrections)") ]]; then
        cp "$OUT/$xname" "$dname/out/$xname"
      fi
    done
#    for xname in $(ls $UTILS); do
#      if [[ -z $(echo "$UTILS/$xname" | grep -P "__pycache") ]]; then
#        cp "$UTILS/$xname" "$dname/utils/$xname"
#      fi
#    done
    for xname in $(ls $DATA); do
      if [[ -z $(echo "$DATA/$xname" | grep -P "personnages") ]]; then
        cp "$DATA/$xname" "$dname/data/$xname"
      fi
    done
    for sdname in $ORIG ; do
      cp -r $sdname $dname/.
    done
    for fname in $CREATE_TEIINITIAL $CREATE_TEIFINAL $CONFIG $OCONFIG $VERSE $PP; do
        bfname=$(basename $fname)
      cp $fname $dname/$bfname
    done
done

IFS=$SAVEIFS

TEIBASIC=../out/hofnarr_heidideldum.xml
CREATE_TEIFINAL=../out/hofnarr_heidideldum_with_characters.xml
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
