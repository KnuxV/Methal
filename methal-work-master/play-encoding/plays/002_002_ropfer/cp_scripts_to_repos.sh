DATA=data
ORIG=RopferStoskopf
HTML=${ORIG}_hOCR
TEI=${ORIG}TEI

XSLT=ropfer_hocr2tei.xsl
TEIFINAL=ropfer_tei_final.py
MANUAL=manual_corrections.py

PTHINDIV=/home/ruizfabo/te/stra/re/theatre_alsacien/demos/heb_pfingstmontag/unistra-methal-sources/indiv/methal-sources
PTHGRP=/home/ruizfabo/te/stra/re/theatre_alsacien/demos/heb_pfingstmontag/unistra-methal-sources/group/methal-sources

SINDIV=$PTHINDIV/work/stoskopf-ins-ropfers-apothek
SGRP=$PTHGRP/work/stoskopf-ins-ropfers-apothek

for dname in $SINDIV $SGRP; do
    [[ ! -d $dname ]] && mkdir -p $dname
    [[ ! -d $dname/${TEI} ]] && mkdir -p $dname/${TEI}
    cp -r $DATA $dname/.
    for sdname in $ORIG $HTML; do
      cp -r $sdname $dname/.
    done
    for fname in $XSLT $TEIFINAL $MANUAL; do
      cp $fname $dname/$fname
    done
done

TEIBASIC=$TEI/stoskopf-ropfer.xml
TEICLEAN=$TEI/stoskopf-ropfer_temp.xml
TEIFINAL=$TEI/stoskopf-ropfer_final.xml
TEIDRACOR=$TEI/stoskopf-ropfer_final_dracor.xml

for fname in $TEIBASIC $TEICLEAN $TEIFINAL $TEIDRACOR; do
    for dname in $SINDIV $SGRP;
        do cp $fname ${dname}/${fname}
    done
done

cp README.md $SINDIV
cp README.md $SGRP
cp README-work.md $(dirname ${SINDIV})/README.md
cp README-work.md $(dirname ${SGRP})/README.md
