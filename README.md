# scrape

## Prerequisites

* Install Python Virtual Environment: https://opensource.com/article/19/6/python-virtual-environments-mac
  * Python version might need to be newer than what is documented. For example on Ventura, install Python 3.11.1.
* Create a virtual env and install scrapy: pip install Scrapy
  * You might need to install dateparser if missing: pip install dateparser

## Adding a new website to scrape

1. Add a new entry here: https://github.com/JudicialCouncilOfCalifornia/scrape/blob/main/spiders.ini
2. For example
```
    [sf]
    allowed_domains = www.sfsuperiorcourt.org
    start_urls = https://www.sfsuperiorcourt.org
    title = .hero h1::text,.another-class-used-for-title
    body = #mainContent,.contentCenterWide
    parent = .breadcrumb li:nth-last-of-type(2) a::attr(href)
    allowed_urls_file = false
```
Different pages may use different classes for the body.  Concatenate the selectors with comma.

In the case of courts.ca we only want to scrape a subset of urls. This requires the `allowed_urls_file` key in the config. Leave it `false` if not needed. If it is needed set it to the file name of the list of urls to scrape. The file should be in the same directory as the spiders.ini file.  i.e. sf-urls.ini

This file should contain the heading that matches your new heading in spiders.ini.  i.e. [sf]. Following that is the key `allowed_urls` with a space separated list of urls you want to scrape.

```
    [sf]
    allowed_urls = https://www.sfsuperiorcourt.org/general-info/locations-and-contact-information https://www.sfsuperiorcourt.org/general-info/locations-and-contact-information https://www.sfsuperiorcourt.org/general-info/locations-and-contact-information
```

3. Run this command
```
    scrapy crawl datacrawler -o results/sf.json -a target=sf
```
Replace sf.json with a new filename.
Replace sf with the target you defined in spiders.ini

4. Commit the code and push.
5. Grab the raw value of the json file, ie https://raw.githubusercontent.com/JudicialCouncilOfCalifornia/scrape/main/results/sf.json
6. Import the results into new migration spreadsheet with the json file. Duplicate a previous spreadsheet from https://docs.google.com/spreadsheets/d/1zsZ-cEIZGWvmv0dXVTyL8Hh4Y9ld64Gcqy3TuxQAP7c/edit?pli=1#gid=0.
   - Update the import value for the 'url' cell under the `PageScrape` sheet.
7. Permit public access to spreadsheet for the migration import to pull content.
   - `Share > Anyone with the link` with `Viewer` level access.

### Files
Migration import will depend on media to be imported first. Use any tool that can find and report on all media in use.

1. brew install httrack
2. on your terminal
   - ```
      httrack https://www.amadorcourt.org/  -O "/path/to/Amador"  -%v -r10 -v
      cd /path/to/Amador/www.amadorcourt.org
      find . -type f -not -name "*.html" -not -name "*.js" -not -name "*.xml" -not -name "*.LOG" -not -name "*.db" -not -name "*.asp" -not -name "*.cfm" -not -name "*.txt" -not -name ".htaccess" -not -name "*.htm" -not -name "*.html" -not -name "*.wal" -not -name "*.dbn" -not -name "*.mdb" -not -name "*.cfc" -not -name "*.css" -not -name "*.inc" -not -name "*.class" -not -name "*.ds" > ../links.txt
      cd ..
     ```
   - open links.txt and transfer to the `Forms` sheet in the migration spreadsheet
