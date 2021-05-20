from lxml import etree as ET

tei = ET.Element("TEI")
tree = ET.parse('data/body/Am_letzte_Maskebal.xml').getroot()
tei.insert(0, tree)



ET.dump(tei)