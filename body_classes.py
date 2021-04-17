# import re
from lxml import etree as ET


class Body:
    """
    Création de la structure du body
    The body tag is the root of the tree.
    """
    def __init__(self):
        self.xml_body = ET.Element("body")

    def add_pb(self, number):
        page_tag = ET.SubElement(self.xml_body, "pb")
        page_tag.set("n", number)

    def create_tree(self, path):
        tree = ET.ElementTree(self.xml_body)
        tree.write(path, encoding="utf-8", xml_declaration=True)


class Div:
    """
    Each scene is described inside a div tag with :
    a type attribute, usually "scene",
    and sub elements :
    head, the number of the scene
    stage with information about the scene
    a list of Sp class instances, (see Sp class)

    """
    def __init__(self, parent):
        self.xml_div = ET.SubElement(parent, "div")

    def add_head(self, head):
        head_tag = ET.SubElement(self.xml_div, "head")
        head_tag.text = head

    def add_stage(self, stage, stage_att=None):
        stage_tag = ET.SubElement(self.xml_div, "stage")
        stage_tag.text = stage
        if stage_att:
            stage_tag.set("type", stage_att)

    def add_type_att(self, type_att):
        self.xml_div.set("type", type_att)

    def add_pb(self, number):
        page_tag = ET.SubElement(self.xml_div, "pb")
        page_tag.set("n", number)


class Sp:
    """

    """

    def __init__(self, parent):
        # Readable version of the name of the speaker.
        self.speaker = ""
        # who = hashtagged version of the name available in castList
        self.who = ""
        self.stage = ""
        self.line = []
        self.xml_sp = ET.SubElement(parent, "sp")

    def add_speaker(self, speaker, who):
        self.speaker = speaker
        self.who = who
        self.xml_sp.set("who", self.who)
        speaker = ET.SubElement(self.xml_sp, "speaker")
        speaker.text = self.speaker

    def add_stage(self, stage):
        self.stage = stage
        stg = ET.SubElement(self.xml_sp, "stage")
        stg.text = stage

    def add_line(self, line):
        self.line.append(line)
        lin = ET.SubElement(self.xml_sp, "p")
        lin.text = line

    def add_poem(self, line, part=None):
        lin = ET.SubElement(self.xml_sp, "l")
        lin.text = line
        if part:
            lin.set("part", "Y")

    def add_pb(self, number):
        page_tag = ET.SubElement(self.xml_sp, "pb")
        page_tag.set("n", number)
