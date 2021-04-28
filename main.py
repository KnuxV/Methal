import requests
from bs4 import BeautifulSoup

# text file extraction using the Wikipedia API

# First, main link, get all the titles
r2 = requests.get("https://als.wikipedia.org/wiik/Text:August_Lustig/A"
                  "._Lustig_S%C3%A4mtliche_Werke:_Band_2")
soup = BeautifulSoup(r2.text, "html.parser")

# Getting all the titles/ only the 26 plays
count = 0
lst_url = []
for a in soup.find_all('a', href=True):
    if "Werke:_Band_2" in a["href"]:
        count += 1
        if count < 27:
            lst_url.append(a["href"])

# Title is after the last "/"
lst_title = [url.split("/")[-1] for url in lst_url]

# api json
api_wiki = "https://als.wikipedia.org/w/api.php?action=query&prop=revisions" \
           "&rvprop=content&format=json&rvslots=main&titles=Text" \
           ":August_Lustig/A._Lustig_S%C3%A4mtliche_Werke:_Band_2/"

# Creating the .txt files
if __name__ == '__main__':
    for title in lst_title:
        r = requests.get(api_wiki + title)
        num = list(r.json()["query"]["pages"].keys())[0]
        title = r.json()["query"]["normalized"][0]["from"].split("/")[-1]

        text = r.json()["query"]["pages"][str(num)]["revisions"][0]["slots"] \
            ["main"]["*"]
        with open("data/txt/" + title + ".txt", "w", encoding="utf-8") as f:
            f.write(text)
