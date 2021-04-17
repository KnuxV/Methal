from lxml import etree as ET
import re
import os
from unidecode import unidecode


class CastList:
    """
    create a castList.xml file for a given play
    """

    def __init__(self, play):
        self.play = play
        self.persone = dict()

    def add_actor(self, persname, roledesc, corresp):
        self.persone[persname] = (unidecode(corresp), roledesc)

    def create_tree(self):
        xml_castlist = ET.Element("castList")
        head = ET.SubElement(xml_castlist, "head")
        head.text = "PERSONE:"

        for pers in self.persone:
            castitem = ET.SubElement(xml_castlist, "castItem")
            castitem.set("corresp", self.persone[pers][0])
            role = ET.SubElement(castitem, "role")
            roleDesc = ET.SubElement(castitem, "roleDesc")
            persName = ET.SubElement(role, "persName")
            persName.text = pers
            roleDesc.text = self.persone[pers][1]

        tree = ET.ElementTree(xml_castlist)
        print("data/castList/" + str(self.play) + ".xml")
        tree.write("data/castList/" + str(self.play) + ".xml",
                   encoding="utf-8",
                   xml_declaration=True)


def pers_transform(line):
    """
    from a line in the ::PERSONE: section, gives a triplet (name, lowercase
    name, activity)
    example : :Herr SPATZLE, dr Liebhawer vom Lisettle.
    return (Herr SPATZLE, #herr_spatzle, dr Liebhawer vom Lisettle)
    :param line:
    :return:
    """
    if len(line) < 1:
        return "", "", ""
    elif len(line.rstrip().split(",")) > 1:
        line = line.rstrip().split(",")
        name = re.search(r"\w[\w\s]+\w", line[0])
        name = name[0]
        corresp = "#" + name.lower().replace(" ", "_")
        activity = line[1]
    else:
        name = re.search(r"\w[\w\s]+\w", line)[0]
        corresp = "#" + name.lower().replace(" ", "_")
        activity = ""
    return name, activity, corresp


def file_to_castlist(path):
    # Given the path of a file, locate the :::PERSONE:''' section with the
    # name and description of the characters
    lst_pers = []
    with open(path, "r", encoding="utf-8") as f:
        index_persone = 0
        for ind_line, line in enumerate(f):
            if "PERSONE" in line:
                index_persone = ind_line
            if 0 < index_persone != ind_line and len(line.rstrip()) > 0:
                lst_pers.append(line)
            if line.rstrip() == "" and index_persone > 0 and ind_line > \
                    index_persone + 1:
                break
    # cleans the title of the play using the path
    title = path[5:-4]
    # set up an instance of castList
    xml = CastList(title)
    for pers in lst_pers:
        # see the pers_transform function above
        xml.add_actor(*pers_transform(pers))
    xml.create_tree()


def get_txt_files(base_dir):
    # Returns the path of each .txt file in the data folder as a list
    lst_of_plays = [entry.name for entry in os.scandir(base_dir) if
                    entry.name.endswith(".txt") and entry.is_file()]
    return lst_of_plays


if __name__ == '__main__':
    for path_play in get_txt_files("data"):
        a = "data/" + path_play
        file_to_castlist("data/" + path_play)
