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
perl -pi -e 's/ rend=["][^"]+["]//g' $oufi
# renames
sed -i -e 's/<div type="character-description">/<div type="front">/' $oufi
sed -i -e 's/<div type="dedication">/<div type="front">/' $oufi
sed -i -e 's/<div type="set">/<div type="front">/' $oufi