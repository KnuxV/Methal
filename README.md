# Methal
The goal is to retrieve the plays from Lustig on Wikipedia,
and to transform them into .xml files with TEI encoding.

The files are available there : 
https://als.wikipedia.org/wiik/Text:August_Lustig/A._Lustig_S%C3%A4mtliche_Werke:_Band_2

Step 1 : main.py
The main.py file is used to retrieve, parse them and 
create a txt file in order to store them.

A TEI file is made of three parts, the TeiHeader, 
the profileDesc and the text (made of front and body)

The teiHeader is countains information about the play, 
profileDesc and front are about the characters,
and the body countains the text.

Step 2 : castList.py (optional)
To make the xml tree, we'll use classes and the module
etree from lxml.

The castList.py creates the folder castList and within 
a file for each play with the list of the characters, using
Tei encoding. However, I chose to use the info available 
in the personnages_vj.xlsx file for the final work. 
Therefore, castList.py is redundant.

Step 3: create_body.py
The main part of the task is to create the body of each play.
In order to so, we use body_classes.py to describe each
class used in the tree. 
The files create_body_poem.py, create_body.py and 
create_body_hochzit.py read the .txt files line by line.
Then it creates the body in xml format in a folder 
named body.
The script mainly relies on regex expression reading the
text files line by line. However, there are a considerable
number of exceptions. 

Step 4 : parse_xlsx.py
This script retrieves the info about each play in 
personnages_vj.xlsx and the body of each play in the body folder.
Thanks to the tei_class.py, it creates a "final" xml file in 
the final folder. However, this is no longer the final folder.

Step 5 : modif_namespace.py
Etree has issue with the Tei namespaces that I've not been
able to understand, so I manually fixed the namespaces thanks
to this script.

#TODO
Still many issues with the songs, especially when the 
characters sing together ("mitnander"). These must be fixed
with another script or manually.