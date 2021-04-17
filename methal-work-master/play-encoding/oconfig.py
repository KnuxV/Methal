#coding=utf8

from collections import OrderedDict as OD
import os

# TEI schema path
tei_rng = os.path.abspath(os.path.join("../../schema", "my-tei.rng"))

# licenses
availability = {
    "ccby": "".join(["<availability>",
                     "<licence><ab>CC BY 2.0</ab>",
                     '<ref target="https://creativecommons.org/licenses/by/2.0/">Licence</ref>',
                     "</licence></availability>"])
}

respStmt = OD([
    (("Delphine Bernhard", "OCR & its correction"), False),
    (("Valentine Jung", "OCR correction"), True),
    (("Pablo Ruiz", "OCR, TEI encoding"), True)
])

character_sheet_name = "personnages"
header_sheet_name = "pieces"
play_set_dir = "../../../sets"
play_set_data = os.path.abspath(os.path.join(play_set_dir, "sets.xml"))
dedication_fn = os.path.abspath("../../other/dedications.xml")
