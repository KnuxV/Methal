#!/usr/bin/env bash

rng='<?xml-model href="https://dracor.org/schema.rng" type="application/xml" schematypens="http://relaxng.org/ns/structure/1.0"?>
'
infi="$1"
oufi="${infi%.*}_for_dracor.xml"
# remove non-dracor relations
grep -Pv "type=[\"']m[\"']" "$1" > .t ; mv .t $oufi
# add dracor schema
sed -i "3i ${rng}" $oufi
# comment or remove non-dracor
perl -0pe 's/(<respStmt.*<\/respStmt>)/<!-- $1 -->/gms' $oufi > .t ; mv .t $oufi
perl -0pe 's/<encodingDesc.*<\/encodingDesc>//gms' $oufi > .t ; mv .t $oufi
perl -pi -e 's/<\/?span[^>]*>//g' $oufi
# renames
sed -i -e 's/<div type="character-description">/<div type="front">/' $oufi
sed -i -e 's/<div type="set">/<div type="front">/' $oufi
perl -0pe 's/<back>.*<div>/<stage>/gms' $oufi > .t ; mv .t $oufi
perl -0pe 's/<\/div>[^<]+<\/back>/<\/stage>/gms' $oufi > .t ; mv .t $oufi
# move back to last <sp>
head -n 1115 $oufi > part1
sed -n 1119,1121p $oufi > stage
sed -n 1116,1118p $oufi > close
cat part1 stage close > .t
echo -e "  </text>\n</TEI>" >> .t
mv .t $oufi
rm part1 stage close

