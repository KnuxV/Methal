from lxml import etree as ET
from itertools import islice
import re
xml = "data/castList/D'Singstund.xml"
tree = ET.parse(xml)

r = tree.xpath("//castItem/@corresp")
print(r)

re_line = r'(?P<part>[:]{2,3})?(?P<line>[^\(<:=\[{\)]+)(?P<stage>\([^\)]+\))?'

f1 = "::Ich dank... Sie excüsiere -(tamere)"
f2 = "::(er b'schaüt's g'naüer)"
f3 = "Was soll das heisse!..."
m = re.match(re_line,f1)

print(m.group("part"))
print(m.group("line"))
print(m.group("stage"))

a = "data/Am_letzte_Maskebal.txt"

a = "data/body"+a[3:]
print(a)