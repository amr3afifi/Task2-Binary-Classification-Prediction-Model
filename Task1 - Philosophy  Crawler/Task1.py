import urllib
import time
import requests
import string
from bs4 import BeautifulSoup
visitedLinks=[]

def htmlParser(wikilink):
    if(wikilink.startswith('/wiki')):
        wikilink="https://en.wikipedia.org"+wikilink

    if (wikilink=="https://en.wikipedia.org/wiki/Wikipedia:Getting_to_Philosophy"):
        print("**************** Reached Getting_to_Philosophy ****************")
        exit()

    re=requests.get(wikilink)
    data=re.text
    soup = BeautifulSoup(data, "html.parser")
    Content=soup.find(id="bodyContent")
    findTags(Content)

def findTags(Content):
    Found=False
    if Content is not None:
        for link in Content.find_all("a", attrs={"class": ""}):
            LinkEnter=link.get('href')
            if LinkEnter is not None:
                if LinkEnter not in visitedLinks:
                    if(LinkEnter.startswith('/wiki') or LinkEnter.startswith('https')):
                        if((not LinkEnter.startswith('/wiki/Special')) and (not LinkEnter.startswith('/wiki/Help'))and (not LinkEnter.startswith('/wiki/Category')) and (not LinkEnter.startswith('/wiki/Template'))):
                            Found=True
                            break

    if(Found==True):
        if LinkEnter not in visitedLinks:
            print(LinkEnter)
            visitedLinks.append(LinkEnter)
        time.sleep(0.5)
        htmlParser(LinkEnter)
    else:
        print("**************** Reached Article without any outgoing Wikilinks ****************")
        exit()

htmlParser("/wiki/Special:Random")