import json
from bs4 import BeautifulSoup
import os

def parseJson(filename):
    count = 0

    files = {}
    for item in json.load(open(filename)):
        # print(item['body'])

        # extract links using regex from body
        # links = re.compile(r'([-\w]+\.(?:jpg|gif|png|jpeg|pdf))', re.IGNORECASE | re.MULTILINE | re.DOTALL)
        # for match in links.finditer(str(item['body'])):
        #     print(match.groups())
        #     count+=1
        #     print(count)

        html = BeautifulSoup(str(item['body']))

        for img in html.findAll('img'):
            url = 'https://www.courts.ca.gov' + img['src'] if img['src'].startswith('/') else img['src']
            title = img.get('alt')
            files[url] = title

        for a in html.findAll('a'):
            href = a.get('href')
            if (href
                and os.path.splitext(href)[1]
                and '.htm' not in href
                and '.xhtml' not in href
                and '.cfm' not in href
                and 'youtube.com' not in href
                and 'youtu.be' not in href
                and 'maps.google.com' not in href
                and 'granicus.com' not in href
                and not href.startswith('#')
                and not href.startswith('mailto')
                and not href.endswith('.com')
                and not href.endswith('.gov')
                and not href.endswith('.org')
                and not href.endswith('.net')
                and not href.endswith('/')
            ):
                url = 'https://www.courts.ca.gov' +href if href.startswith('/') else href
                title = a.get('title') or a.text
                files[url] = title

    print(len(files))

    jsonfiles = []
    for url,title in files.items():

        if (not title
                or 'click here' in title.lower()
                or 'read more' in title.lower()
                or 'read >>' in title.lower()
                or 'video' == title.lower()
                or 'video icon' == title.lower()
                or 'icon video' == title.lower()
                or 'here' == title.lower()
                or 'transcript' == title.lower()
                or 'order' == title.lower()
                or 'emergency order' == title.lower()
                or 'briefs' == title.lower()
                or 'sample briefs' == title.lower()
                or 'petitions' == title.lower()
                or 'sample petitions' == title.lower()
                or 'appendix' == title.lower()
                or 'sample appendix' == title.lower()
                or 'exhibits' == title.lower()
                or 'sample exhibits' == title.lower()
                or 'sample writ petitions' == title.lower()
                or 'fee schedule' == title.lower()
                or 'fee schedules' == title.lower()
        ):
            title = os.path.splitext(os.path.basename(url))[0].replace('-', ' ').replace('_', ' ').replace('%20', ' ')

        title = title[0:200].encode('ascii', 'ignore').decode()

        jsonfiles.append(
            {
                "url": url,
                "title": title
            }
        )

    with open("../../results/dca-files.json", "w") as outfile:
        json.dump(jsonfiles, outfile)

parseJson('../../results/dca-page.json')