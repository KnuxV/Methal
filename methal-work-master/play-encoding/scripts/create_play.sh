#!/usr/bin/env bash

# Create directory structure for a new play
# play_id as per spreadsheet in ../../characters
# order_id is the order of encoding of the plays (Pfingstmontag is 001, we started there)
# play_abbrev is a short name to use in the directory for each play

play_id="$1"
order_id="$2"
play_abbrev="$3"

if [[ "$#" -ne 3 ]]; then
    echo -e "\nUsage: create_play.sh play_id order_id play_abbreviation\n"
    exit
fi

play_dir=../plays/${1}_${2}_${3}

if [[ -d "$play_dir" ]]; then
  echo -e "\nPlay exists\n"
  exit
fi

for dn in sources data scripts logs out ; do
  echo $dn
  mkdir -p ${play_dir}/${dn}
done

echo -e "# Encodage de XXXX\n" > ${play_dir}/README.md