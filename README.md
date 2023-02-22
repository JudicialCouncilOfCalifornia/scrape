# scrape

## Prerequisites

* Install Python Virtual Environment: https://opensource.com/article/19/6/python-virtual-environments-mac
  * Python version might need to be newer than what is documented. For example on Ventura, install Python 3.11.1.
* Create a virtual env and install scrapy: pip install Scrapy 
  * You might need to install dateparser if missing: pip install dataparser

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
```    
Different pages may use different classes for the body.  Concatenate the selectors with comma.
    
3. Run this command
```
    scrapy crawl datacrawler -o results/sf.json -a target=sf
```
Replace sf.json with a new filename.
Replace sf with the target you defined in spiders.ini

4. Commit the code and push.
5. Grab the raw value of the json file, ie https://raw.githubusercontent.com/JudicialCouncilOfCalifornia/scrape/main/results/sf.json
6. Import the results into new migration spreadsheet with the json file. See https://github.com/JudicialCouncilOfCalifornia/trialcourt/blob/master/docs/migrations.md and update the url in the import value for the first spreadsheet cell.
