import pandas as pd
from tei_class import Tei

# Opening the notebook
xlsx = pd.ExcelFile("data/personnages_vj.xlsx")

sheet_pieces = xlsx.parse("pieces")
sheet_pieces = sheet_pieces[["workId", "titleMain", "author"]]
condition_lustig = sheet_pieces.workId.between(110, 135)
sheet_pieces_lustig = sheet_pieces[condition_lustig]

sheet_perso = xlsx.parse("personnages")
condition_lustig = sheet_perso.workId.between(110, 135)
sheet_perso_lustig = sheet_perso[condition_lustig]
sheet_perso_lustig = sheet_perso_lustig[["workId", "persId", "persName",
                                         "roleDesc", "sex",
                                         "profession", "normProf", "age",
                                         "rel"]]

# sheet_perso_lustig = sheet_perso_lustig.merge(sheet_pieces, on="workId")
# print(sheet_perso_lustig.columns)

if __name__ == "__main__":
    for row in sheet_pieces_lustig.iterrows():
        titleMain = row[1].titleMain
        Id = row[1].workId
        lst_perso = []
        condition_id = sheet_perso_lustig.workId == Id
        for row_perso in sheet_perso_lustig[condition_id].iterrows():
            lst_perso.append((row_perso[1].persName, row_perso[1].roleDesc,
                              row_perso[1].sex))

        if Id == 135:
            tei = Tei(title_main=titleMain, lst_perso=lst_perso)
            tei.create_tree("data/final/" + titleMain.replace(" ", "_") + ".xml")
