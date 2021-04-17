"""Merge publisher variants"""

from pandas_ods_reader import read_ods

infile = "maisons_ed_improved.ods"
oufile = "editeurs_concat.tsv"

df = read_ods(infile, "Feuille1")

df.groupby(['id'])["name_one"].apply('|'.join).reset_index()

df = df[["id", "chosen_variant", "name_one", "place"]]
df.rename(columns={"name_one": "variants"})
df = df.astype({"id": int})

df.to_csv(oufile,
          sep='\t',
          index=False)
