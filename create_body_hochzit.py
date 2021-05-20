import os
from lxml import etree as ET
from body_classes import Body, Div, Sp, Lg, spGrp
from itertools import islice
import re

# Regex
# Act MATCH specific
re_ACT = re.compile(r"=\s(II?\.\sACT)\.\s=")
# To match the acts like == I. Uftritt. ==
re_act = re.compile(r"==\s(.+)\s==")
# For match type=characters
re_several_chars = re.compile(r"::<small>\'\'\'([^,]+,[^,]+)\'\'\'</small>")
# For match group1 = speaker and sp who=, group2= stage info
re_single_char = re.compile(r"::<small>'''(?P<char>[^']+)'''\s*"
                            r"(?P<stage>\([^)]+\))?\.*</small>")
# Regex for the single char but inside de table
re_single_char_table = re.compile(r"<small>'''(?P<char>[^']+)'''\s*"
                                  r"(?P<stage>\([^)]+\))?\.*</small>")
# for match about stage
re_stage_line = r"[:]*(\([^)]+\))"

# re_line = r"[:]*([^\(<:=\[{]+)"
# For a line of text or poem, we need 3 groups, first one checking for ":" indicating a part line,
# 2nd one for the text, and 3rd one for stage indications
re_line = r'(?P<part>[:]{1,3})?(?P<line>[^\(<:=\[{\)_]+)(?P<stage>\([^\)]+\))?'
# page numbers
re_page = r"{{.+page(\d+\s\d+)\.pdf.+]]}}"

re_line_w_part_and_stage = r"([:]{1,3})([^\(<:=\[{\)]+)(\([^\)]+\))?"

# G'sang match
re_song = re.compile(r"::<small>'''G'sang\.?'''\s*"
                     r"(?P<stage>\([^)]+\))?\.*</small>")
# Poem related, variable true or false to know if we add <l> or <p>
# If we match a <poem> line, we need to open <lg> too, and close it when we match </poem>
re_poem = r'<(?P<close_tag>/)?poem>'

# Table regex
re_table_open = r'\{\| border="0"'
re_table_close = r'\|\}'

# Match Mitnander line
mit1 = r"::<small>'''Mitnander\.?'''\s*(?P<stage>\([^)]+\))?\.*</small>"
mit2 = r"::\(Mitnander\.?\)"
re_mitnander = re.compile(mit1 + "|" + mit2)


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


def create_body(path, startline):
    """
    Create the body of the plays with are not fully <poem>
    :param path: relative path of the .txt
    :param startline: the start line after the castList
    :return:
    """

    def handle_table(wrapper, sp_class):
        # When in table, first thing create a spgrp
        sp_group = spGrp(div.xml_div)
        # Always add a mitnander
        sp_group.add_stage("Mitnander")
        # For the first sp in table, get the speaker from last sp
        who_table = sp_class.get_who()
        speaker_table = sp_class.get_speaker()
        # Create first Sp
        sp = Sp(sp_group.xml_spGrp)
        sp.add_speaker(speaker=speaker_table, who=who_table)

        for index, table_line in enumerate(wrapper):
            table_line = table_line.rstrip()
            # Regex
            match_single_char_table = re.search(re_single_char_table,
                                                table_line)
            match_line_table = re.match(re_line, table_line)

            # Exit handle_table function if at the end of the table
            if re.match(re_table_close, table_line):
                return True
            else:

                if match_single_char_table:
                    sp = Sp(sp_group.xml_spGrp)
                    speaker_table = match_single_char_table.group("char")
                    who_table = "#" + match_single_char_table.group(
                        "char").lower().replace(" ", "_")
                    sp.add_speaker(speaker_table, who_table)
                elif match_line_table:
                    if not sp.has_lg:
                        lg = Lg(sp.xml_sp)
                        sp.change_lg()
                    lg.add_poem(match_line_table.group("line"),
                                match_line_table.group("part"))
                    if match_line_table.group("stage"):
                        lg.add_stage(match_line_table.group("stage"))
        return False

    body = Body()
    poem_bool = False
    # To deal with a problem of <li> between two table and without a <small>
    # bla <small> which acts as speaker
    end_of_table = False
    # end of G'sand // To deal with a problem where there's no <poem> before
    # G'sand
    g_sang = False
    with open(path, 'r', encoding="utf-8") as f:
        # skip lines according to star tine
        head = list(islice(f, startline))

        for index, line in enumerate(f):
            line = line.rstrip()
            match_ACT = re.search(re_ACT, line)
            match_act = re.search(re_act, line)
            match_several_chars = re.match(re_several_chars, line)
            match_single_char = re.match(re_single_char, line)
            match_stage_line = re.match(re_stage_line, line)
            match_line = re.match(re_line, line)
            match_page = re.match(re_page, line)
            match_poem = re.match(re_poem, line)
            match_song = re.match(re_song, line)
            match_table_open = re.match(re_table_open, line)
            match_mitnander = re.match(re_mitnander, line)

            if match_ACT:
                act_div = Div(body.xml_body)
                act_div.add_type_att("ACT")
                act_div.add_head(match_ACT.group(0))

            # Creating act
            if match_act:
                div = Div(act_div.xml_div)
                div.add_type_att("scene")
                div.add_head(match_act.group(1))

            elif match_several_chars:
                div.add_stage(match_several_chars.group(1), "characters")

            elif match_single_char:
                # If only one scene, the div must be created with the first sp
                end_of_table = False
                g_sang = False
                try:
                    sp = Sp(div.xml_div)
                except NameError:
                    div = Div(act_div.xml_div)
                    div.add_type_att("scene")
                    sp = Sp(div.xml_div)
                speaker = match_single_char.group("char")
                who = "#" + match_single_char.group("char").lower().replace(
                    " ", "_")
                sp.add_speaker(speaker, who)
                if match_single_char.group("stage"):
                    sp.add_stage(match_single_char.group("stage"))

            elif match_song:
                sp.add_gsang()
                g_sang = True
                if match_song.group("stage"):
                    sp.add_stage(match_song.group("stage"))

            elif match_mitnander:
                last_who = sp.get_who()
                # speaker = sp.get_speaker()
                sp = Sp(div.xml_div)
                sp.add_speaker(speaker="NEED SECOND WHO", who=last_who)
                sp.add_stage("(Mitnander)")

            elif match_stage_line:
                if poem_bool or g_sang:
                    try:
                        lg.add_stage(match_stage_line.group(1))
                    except NameError:
                        sp.add_stage(match_stage_line.group(1))
                else:
                    try:
                        sp.add_stage(match_stage_line.group(1))
                    except UnboundLocalError:
                        try:
                            div.add_stage(match_stage_line.group(1))
                        except UnboundLocalError:
                            act_div.add_stage(match_stage_line.group(1))

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
                poem_bool = not poem_bool

            elif match_table_open:
                # if match the opening of the table, open handle_table with the wrapper as arg so that lines are not
                # read twice. last sp as arg too, as too get the last speaker
                end_of_table = handle_table(f, sp)

            elif match_line:
                if end_of_table:
                    last_who_t, last_speaker_t = sp.get_who(), sp.get_speaker()
                    sp = Sp(div.xml_div)
                    sp.add_speaker(last_speaker_t, last_who_t)
                    end_of_table = False
                if poem_bool or g_sang:
                    # We are inside a <poem>, need to create a <lg> for each sp
                    if not sp.has_lg:
                        lg = Lg(sp.xml_sp)
                        sp.change_lg()
                    lg.add_poem(match_line.group("line"))
                    # That's the line to add part, but I don't understand how many : makes a part
                    # lg.add_poem(match_line.group("line"), match_line.group("part"))
                    if match_line.group("stage"):
                        lg.add_stage(match_line.group("stage"))
                else:
                    sp.add_line(line)

    print("data/body" + path[8:-3])
    xml_path = "data/body" + path[8:-3] + "xml"
    body.create_tree(xml_path)


if __name__ == "__main__":
    create_body("data/txt/Vor_un_no_dr_Hochzit.txt", 24)
