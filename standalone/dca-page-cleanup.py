import json
from bs4 import BeautifulSoup
import os

def parseJson(filename):

    data = {}
    with open(filename, "r") as jsonFile:
        data = json.load(jsonFile)

    for i in range(len(data)):
        html = BeautifulSoup(str(data[i]['body']).encode(), 'lxml')
        html.find('div', id='leftNavDropdown').decompose()
        if html.find('div', id='printWrap'):
            html.find('div', id='printWrap').decompose()
        if html.find('div', id='mobileFloatRight'):
            html.find('div', id='mobileFloatRight').decompose()
        html.find('div', id='leftPanel').decompose()

        data[i]['body'] = str(html.find('div', id='mainContent')).replace('\\n', ' ').replace('\\r', '').replace('\\t', '')

    with open("../../results/dca-page-clean.json", "w") as jsonFile:
        json.dump(data, jsonFile)

parseJson('../../results/dca-page.json')