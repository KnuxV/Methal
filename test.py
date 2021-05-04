from lxml import etree as ET
from itertools import islice
import re


def table(wrap):
    f.__next__()
    f.__next__()
    for line in f:
        print(line)


with open("data/txt/test.txt", 'r', encoding="utf-8") as f:
    table(f)
