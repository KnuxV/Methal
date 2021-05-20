from lxml import etree as ET

NSMAP = {"xmlnsxs": "http://www.w3.org/2001/XMLSchema",
         "xmlns": "http://www.tei-c.org/ns/1.0"}


def create_id(name):
    """
    :param name: a string
    :return: the string in lowercase with a _ instead of a space
    """
    try:
        res = name.replace(" ", "_").lower()
    except AttributeError:
        res = name
    return res


class Tei:
    def __init__(self, title_main, lst_perso):
        self.tei = ET.Element("TEI", nsmap=NSMAP)
        hdr = ET.SubElement(self.tei, "teiHeader")
        # structure
        file_desc = ET.SubElement(hdr, "fileDesc")
        #  fileDesc
        title_stmt = ET.SubElement(file_desc, "titleStmt")
        #  titleStmt
        ET.SubElement(title_stmt, "title", type="main").text = title_main

        # If sub title needed
        # ET.SubElement(titleStmt, "title", type="sub").text = sub
        ET.SubElement(title_stmt, "author", key="wikidata:Q17038136").text \
            = "August Lustig"
        respstmt = ET.SubElement(title_stmt, "respStmt")
        ET.SubElement(respstmt, "name").text = "Kévin Michoud"
        ET.SubElement(respstmt, "resp").text = "TEI encoding"

        publication_stmt = ET.SubElement(file_desc, "publicationStmt")
        ET.SubElement(publication_stmt,
                      "publisher").text = "LiLPa - Université de Strasbourg"
        availability = ET.SubElement(publication_stmt, "availability")
        licence = ET.SubElement(availability, "licence")
        ET.SubElement(licence, "ab").text = "CC BY 2.0"
        ET.SubElement(licence, 'url').text = "Licence"
        source_desc = ET.SubElement(file_desc, "sourceDesc")
        bibl = ET.SubElement(source_desc, "bibl", type="digitalSource")

        ET.SubElement(bibl, "name").text = "name"
        ET.SubElement(bibl, "idno", type="URL").text = \
            "https://als.wikipedia" \
            ".org/wiki/Text" \
            ":August_Lustig/A" \
            "._Lustig_S%C3" \
            "%A4mtliche_Werke" \
            ":_Band_2 "
        bibl2 = ET.SubElement(bibl, "bibl", type="type")
        ET.SubElement(bibl2, "author", key="wikidata:Q17038136").text \
            = "August Lustig "
        ET.SubElement(bibl2, "title", type="main").text = title_main

        # If sub title needed
        # ET.SubElement(bibl2, "title", type="sub").text = "sub"

        ET.SubElement(bibl2, "publisher").text = "Publisher"
        ET.SubElement(bibl2, "date").text = "date"

        profile_desc = ET.SubElement(self.tei, "profileDesc")
        partic_desc = ET.SubElement(profile_desc, "particDesc")

        # Creating the listPerson
        list_person = ET.SubElement(partic_desc, "listPerson")
        for elem in lst_perso:
            pers = ET.SubElement(list_person, "person")
            # If no listPerson, just create an empty tag
            if not type(elem[0]) == float:
                pers.set("xmlid", create_id(elem[0]))
                pers.set("sex", elem[2])
                ET.SubElement(pers, "persName").text = elem[0]

        # TODO relations
        ET.SubElement(partic_desc, "listRelation")

        # Cast list
        text = ET.SubElement(self.tei, "text")
        front = ET.SubElement(text, "front")
        # Cast List
        castlist = ET.SubElement(front, "castList")
        ET.SubElement(castlist, "head").text = "Personen"
        for elem in lst_perso:
            if not type(elem[0]) == float:
                cast_item = ET.SubElement(castlist, "castItem")
                cast_item.set("corresp", "#" + create_id(elem[0]))
                role = ET.SubElement(cast_item, "role")
                ET.SubElement(role, "persName").text = elem[0]
                if not type(elem[1]) == float:
                    ET.SubElement(cast_item, "roleDesc").text = elem[1]
        # TODO Set infos, add manually
        ET.SubElement(front, "set")

        # Body section
        body_path = "data/body/" + title_main.replace(" ", "_") + ".xml"
        body = ET.parse(body_path).getroot()
        text.insert(1, body)

    def create_tree(self, path):
        tree = ET.ElementTree(self.tei)
        tree.write(path, encoding="utf-8", xml_declaration=True)
