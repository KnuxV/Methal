import os


for file in os.scandir("data/final"):
    inFile = open(file, 'r')
    data = inFile.readlines()
    inFile.close()
    # some manipulation on `data`
    outFile = open('data/modif_namespace/' + file.name, 'w')
    for line in data:
        # line = line.rstrip()
        if 'xmlns:xmlnsxs="http://www.w3.org/2001/XMLSchema"' in line:
            line = line.replace("xmlns:xmlnsxs", "xmlns:xs")
        elif 'xmlns:xmlns="http://www.tei-c.org/ns/1.0"' in line:
            line = line.replace("xmlns:xmlns", "xmlns")
        elif "xmlid" in line:
            line = line.replace("xmlid", "xml:id")
        outFile.writelines(line)
    outFile.close()
