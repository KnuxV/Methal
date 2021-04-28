import os
from lxml import etree as ET
from body_classes import Body, Div, Sp, Lg
from itertools import islice
import re

# Regex

# To match the acts like == I. Uftritt. ==
act = re.compile(r"==\s(.+)\s==")
# For match type=characters
several_chars = re.compile(r"::<small>\'\'\'([^,]+,[^,]+)\'\'\'</small>")
# For match group1 = speaker and sp who=, group2= stage info
single_char = re.compile(r"::<small>'''(?P<char>[^']+)'''\s*"
                         r"(?P<stage>\([^)]+\))?\.*</small>")
# for match about stage
stage_line = r"[:]*(\([^)]+\))"

# re_line = r"[:]*([^\(<:=\[{]+)"
# For a line of text or poem, we need 3 groups, first one checking for ":" indicating a part line,
# 2nd one for the text, and 3rd one for stage indications
re_line = r'(?P<part>[:]{1,3})?(?P<line>[^\(<:=\[{\)_]+)(?P<stage>\([^\)]+\))?'
# page numbers
re_page = r"{{.+page(\d+\s\d+)\.pdf.+]]}}"

re_line_w_part_and_stage = r"([:]{1,3})([^\(<:=\[{\)]+)(\([^\)]+\))?"

# G'sang match
re_song = re.compile(r"::<small>'''G'sang'''\s*"
                     r"(?P<stage>\([^)]+\))?\.*</small>")
# Poem related, variable true or false to know if we add <l> or <p>
# If we match a <poem> line, we need to open <lg> too, and close it when we match </poem>


re_poem = r'</?poem>'


def get_files(base_dir, form):
    # Returns the path of each file in the data folder as a list
    lst_of_plays = [entry.name for entry in os.scandir(base_dir) if
                    entry.name.endswith("." + form) and entry.is_file()]
    return lst_of_plays


lst_xml = sorted(get_files("data/castList", "xml"))
lst_txt = sorted(get_files("data", "txt"))


def get_list_char(title):
    """
    :param title: title of the play
    :return: a list with the characters from the castList.xml
    example :
    [#pierrot, #marie, #domino]
    """
    xml = "data/castList/" + title
    tree = ET.parse(xml)
    return tree.xpath("//castItem/@corresp")


# print(get_list_char("Am_letzte_Maskebal.xml"))


def create_body(path, startline):
    """
    Create the body of the plays with are fully <poem>
    :param path: relative path of the .txt
    :param startline: the start line after the castList
    :return:
    """
    body = Body()
    poem_bool = False
    with open(path, 'r', encoding="utf-8") as f:
        # skip lines according to star tine
        head = list(islice(f, startline))

        for index, line in enumerate(f):
            line = line.rstrip()
            match_act = re.search(act, line)
            match_several_chars = re.match(several_chars, line)
            match_single_char = re.match(single_char, line)
            match_stage_line = re.match(stage_line, line)
            match_line = re.match(re_line, line)
            match_page = re.match(re_page, line)
            match_poem = re.match(re_poem, line)
            match_song = re.match(re_song, line)

            if match_act:
                print("act", index, line)
                div = Div(body.xml_body)
                div.add_type_att("scene")
                div.add_head(match_act.group(1))

            elif match_several_chars:
                print("SeC", index, line)
                div.add_stage(match_several_chars.group(1), "characters")

            elif match_single_char:
                # If only one scene, the div must be created with the first sp
                try:
                    sp = Sp(div.xml_div)
                except NameError:
                    div = Div(body.xml_body)
                    div.add_type_att("scene")
                    sp = Sp(div.xml_div)
                sp.add_speaker(match_single_char.group("char"), "#" +
                               match_single_char.group("char").lower().replace(" ", "_"))
                if match_single_char.group("stage"):
                    sp.add_stage(match_single_char.group("stage"))

            elif match_song:
                sp.add_gsang()
                if match_song.group("stage"):
                    sp.add_stage(match_song.group("stage"))

            elif match_stage_line:
                print("St", index, line)
                sp.add_stage(match_stage_line.group(1))

            elif match_page:
                # For the pages, we add then the <pb> tag wherever we find it.
                try:
                    sp.add_pb(match_page.group(1))
                except NameError:
                    try:
                        div.add_pb(match_page.group(1))
                    except NameError:
                        body.add_pb(match_page.group(1))
            elif match_poem:
                if "/" not in line:
                    poem = Lg(div.xml_div)
                poem_bool = not poem_bool

            elif match_line:
                if poem_bool:
                    poem.add_poem(match_line.group("line"), match_line.group("part"))
                    if match_line.group("stage"):
                        poem.add_stage(match_line.group("stage"))
                else:
                    sp.add_line(line)

    print("data/body" + path[8:-3])
    xml_path = "data/body"+path[8:-3]+"xml"
    body.create_tree(xml_path)


if __name__ == "__main__":
    create_body("data/txt/Bi_de_Wilde.txt", 33)
