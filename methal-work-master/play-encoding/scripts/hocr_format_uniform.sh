#!/usr/bin/env bash

# different programs (xmllint, gImageReader, tesseract) have different
# 'habits't when writing hOCR. Make it all uniform

indir="$1"

sed -i -e 's/<html xmlns="http:\/\/www.w3.org\/1999\/xhtml" xml:lang="en" lang="en">/<html>/g' "$1"
sed -i -e 's/<meta charset="utf-8" \/>/<meta http-equiv="Content-Type" content="text\/html;charset=utf-8" \/>/g' "$1"

for x in $(ls $indir) ; do grep -Pv 'DOCTYPE' $indir/$x > bla ; mv bla $indir/$x ; done
for x in $(ls $indir) ; do grep -Pv 'transitional.dtd' $indir/$x > bla ; mv bla $indir/$x ; done

