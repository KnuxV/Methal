from lxml import etree as ET
from copy import deepcopy


def create_body():
    return ET.Element("body")


xml_body = ET.Element("body")
print(xml_body)


def create_div(body, act):
    div = ET.SubElement(body, "div")
    div.set("act", act)
    sp = ET.SubElement(div, "sp")
    sp.text = "stuff"


create_div(xml_body, "1")

xml_sp = ET.Element("sp")
speaker = ET.SubElement(xml_sp, "speaker")
speaker.text = "Jean"
p = ET.SubElement(xml_sp, 'p')
p.text = "Ta mère en slip"
p = ET.SubElement(xml_sp, 'p')
p.text = "ta mere a poil"
print(ET.tostring(xml_sp))


def combine_xmltree_element(element_1, element_2):
    """
    Recursively combines the given two xmltree elements. Common properties will be overridden by values of those
    properties in element_2.

    :param element_1: A xml Element
    :type element_1: L{Element}

    :param element_2: A xml Element
    :type element_2: L{Element}

    :return: A xml element with properties combined.
    """

    if element_1 is None:
        return element_2.copy()

    if element_2 is None:
        return element_1.copy()

    if element_1.tag != element_2.tag:
        raise TypeError(
            "The two XMLtree elements of type {t1} and {t2} cannot be combined".format(
                t1=element_1.tag,
                t2=element_2.tag
            )
        )

    combined_element = ET.Element(tag=element_1.tag, attrib=element_1.attrib)
    combined_element.attrib.update(element_2.attrib)

    # Create a mapping from tag name to child element
    element_1_child_mapping = {child.tag: child for child in element_1}
    element_2_child_mapping = {child.tag: child for child in element_2}

    for child in element_1:
        if child.tag not in element_2_child_mapping:
            combined_element.append(child.copy())

    for child in element_2:
        if child.tag not in element_1_child_mapping:
            combined_element.append(child.copy())

        else:
            if len(child) == 0:  # Leaf element
                combined_child = element_1_child_mapping[child.tag].copy()
                combined_child.text = child.text
                combined_child.attrib.update(child.attrib)

            else:
                # Recursively process the element, and update it in the same way
                combined_child = combine_xmltree_element(
                    element_1_child_mapping[child.tag], child)

            combined_element.append(combined_child)

    return combined_element


print(xml_sp.tag)
