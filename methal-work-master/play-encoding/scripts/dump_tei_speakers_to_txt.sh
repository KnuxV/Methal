#!/usr/bin/env bash

# Grep speakers to a log

TEI="$1"
TXT="$2"

grep -Po "<speaker>.+?</speaker>" $TEI | sed 's/<speaker>//g' | sed 's/<\/speaker>//g' | sort | uniq > $TXT
