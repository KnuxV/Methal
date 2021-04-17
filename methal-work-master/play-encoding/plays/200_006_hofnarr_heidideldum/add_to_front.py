#coding=utf8

"""
To add elements to the <front> element, Hofnarr Heidideldum version
"""

from lxml import etree
import pandas as pd
import re
import sys

sys.path.append("../..")

import config as cf
import oconfig as ocf
import utils.utils as ut


def extract_character_description_from_df(dfpath=cf.cast_list_data):
    """
    Prepare character description to write TEI page, based on dataframe
    information (columns _otherDesc_ and _persName_)

    Parameters
    ----------
    dfpath : str, optional
        Path to ODS sheet with information to create dataframe.
        Default value is in :obj:`config` module (`cf.cast_list_data`)

    Returns
    -------
    pandas.DataFrame
        Dataframe with information to write out.
    """
    df = ut.read_character_info(dfpath)
    df['persName'] = df['persName'].apply(lambda x: re.sub("^Dr\.?\s*", "", x))
    df_name_des = df.loc[pd.notnull(df.otherDesc), ['persName', 'otherDesc']]
    return df_name_des


def create_character_description_page(df):
    """

    Parameters
    ----------
    df : pandas.DataFrame

    Returns
    -------
    lxml.etree.Element
        A `<div>` element containing a TEI <list> element
        with the character description
    """
    div = etree.Element("div", type="character-description")
    list = etree.SubElement(div, "list", rend="numbered")
    etree.SubElement(list, "head").text = "Personebeschriewung:"
    for idx, row in df.iterrows():
        # adding a tail (would be ';' here) not allowed in TEI schema
        etree.SubElement(list, "label").text = row.persName
        etree.SubElement(list, "item").text = row.otherDesc
    return div


def add_character_description_to_front(
        fr, dfpath=cf.cast_list_data, pnbr=cf.character_description_pnbr):
    """
    Append a div with a character description list to the front element
    of a TEI file.

    Parameters
    ----------
    fr : lxml.etree.Element
        TEI `<front>` element to append to
    dfpath : str, optional
        Path to ODS sheet with information to create dataframe with
        character information.
        Default value is in :obj:`config` module (`cf.cast_list_data`)
    pnbr : int, optional
        Page number for the `<pb>` element to insert before the description

    Returns
    -------
    None
    """
    fr.append(etree.fromstring(f"<pb n='{pnbr}'/>"))
    cd = extract_character_description_from_df(dfpath)
    div =  create_character_description_page(cd)
    fr.append(div)


def add_dedication_to_front(fr, de, position=0, page_after_add=1):
    """
    Insert dedication or similar in the front, based on `de`, an XML element.
    By default it is inserted at the beginning of the front.

    Parameters
    ----------
    fr : lxml.etree.Element
        TEI `<front>` element to append to
    de : `lxml.etree.Element`
        XML element containing the dedication information.
        A `@pnbr` attribute may encode the page number for it.
    position : int, optional
        Index to insert the information at. Default is 0.
    page_after_add : int, optional
        Number of page-breaks to add after the dedication. Default is 1.
    Returns
    -------
    None
    """
    # figure out page number if available; insert it
    pnbr = de.xpath("./@pnbr")
    if pnbr:
        fr.insert(position, etree.fromstring(f"<pb n='{pnbr[0]}'/>"))
        de.attrib.pop("pnbr")
    # change tag to 'div'
    de.tag = "div"
    de.attrib["type"] = "dedication"
    # insert
    fr.insert(position+1, de)
    # if page number was available, add pb after (one or more)
    if pnbr:
        for pg in range(page_after_add):
            fr.insert(position+pg+2, etree.fromstring(
                f"<pb n='{int(pnbr[0])+pg+1}'/>"))


if __name__ == "__main__":
    dd = extract_character_description_from_df()
    div = create_character_description_page(dd)
