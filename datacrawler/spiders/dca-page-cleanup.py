import json
from bs4 import BeautifulSoup
import os

def parseJson(filename):

    data = {}
    with open(filename, "r") as jsonFile:
        data = json.load(jsonFile)

    for i in range(len(data)):
        html = BeautifulSoup(str(data[i]['body']))
        html.find('div', id='leftNavDropdown').decompose()
        if html.find('div', id='printWrap'):
            html.find('div', id='printWrap').decompose()
        if html.find('div', id='mobileFloatRight'):
            html.find('div', id='mobileFloatRight').decompose()
        html.find('div', id='leftPanel').decompose()

        data[i]['body'] = str(html)

    with open(filename, "w") as jsonFile:
        json.dump(data, jsonFile)

parseJson('../../results/dca-page.json')