#!/usr/bin/env bash

# write differences in word-diff as tab-separated

oufn=$1

if [ "$#" -eq 2 ]; then
    infn=$2
  else
    infn=""
fi

git  diff --word-diff $infn > $oufn
grep -Po "\[.+?\}" $oufn > .t ; mv .t $oufn
sed -i 's/^..//g' $oufn
sed -i 's/..$//g' $oufn
perl -pi -e 's/-\]\{\+/\t/g' $oufn
sort $oufn | uniq -c | sort -rn > .t ; mv .t $oufn
