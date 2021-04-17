#!/usr/bin/env bash

PUBREPODIR=/home/ruizfabo/te/stra/re/theatre_alsacien/demos/heb_pfingstmontag/unistra-methal-sources
PTHINDIV=$PUBREPODIR/indiv/methal-sources/work
PTHGRP=$PUBREPODIR/group/methal-sources/work

for repo in $PTHINDIV $PTHGRP ; do
    for dname in css utils ; do
        [[ ! -d ${repo}/${dname} ]] && mkdir ${repo}/${dname}
        for fname in $(ls ../$dname); do
            if [[ -z $(echo "$fname" | grep -P "(bkp)") ]]; then
                cp "../$dname/$fname" "$repo/$dname"
            fi
        done
    done
done