oufn=$1
git  diff --word-diff > $oufn
grep -Po "\[.+?\}" $oufn > .t ; mv .t $oufn
sed -i 's/^..//g' $oufn
sed -i 's/..$//g' $oufn
perl -pi -e 's/-\]\{\+/\t/g' $oufn
sort $oufn | uniq -c | sort -rn > .t ; mv .t $oufn
