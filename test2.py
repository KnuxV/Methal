import re
line = "::<small>'''Herr Guld''' (kunnt hinte-n-ine hintersi un schint ebbes z'bschaüe duss).</small>"
line1 = "::<small>'''Herr Kalt.'''</small>"
line2 = "Ich mag noch so nogeh un nolüege, 's hilft alles nit meh!"

line3 = "::<small>'''Herr Guld''' (fir sich).</small>"
line4 ="Wie schön as se doch g'wachse-n-isch!"

regex = r'(<small>)(.+)(</small>)'

reg_parenthesis = r"\(([^)]+)\)"
re_obj = re.compile(reg_parenthesis)
match = re_obj.search(line)
print(match)
print(match.group())
# print(match.groups())


reg_name = r"(\'\'\')([^\']+)(\'\'\')"
re_name = re.compile(reg_name)
a = re_name.search(line)
print(a.groups())
print(a.group(2))
print("\nNew stuff")
reg_start_line = r"\:\:<small>"
match = re.match(reg_start_line,line1)
if match:
    print(re.search(regex, line1).group())


t1 = "::<small>'''Pierrot, Domino.'''</small>"
t2 = "::<small>'''Pierrot''' (no-n-em Nachtesse im Restaurant).</small>"
t3 = "'s isch Zit glaüb, liewer Domino,"
t4 = "== I. Uftritt. =="
t5 = "::(er b'schaüt's g'naüer)"
t6 = "<poem>"
t7 = "{{ImDruckVerbergen|[[Datei:ALustig SämtlicheWerke ZweiterBand page724 725.pdf|thumb|724 - 725]]}}"

several_chars = re.compile(r"::<small>\'\'\'([^,]+,[^,]+)\'\'\'</small>")
act = re.compile(r"==\s(.+)\s==")
single_char = re.compile(r"::<small>\'\'\'([^']+)\'\'\'\s*"
                         r"(\([^)]+\))\.*</small>")
stage_line = r"[:]*(\([^)]+\))"
line = r"[\:]*([^(<:]+)"
re_page = r"{{.+page(\d+\s\d+)\.pdf.+]]}}"
m = re.match(re_page, t7)
if m:
    print(m.group(1))

