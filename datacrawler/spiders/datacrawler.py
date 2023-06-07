import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import DatacrawlerItem
from configparser import ConfigParser  # ver. < 3.0
from urllib.parse import urlparse

class DatacrawlerSpider(CrawlSpider):
    name = 'datacrawler'

    def __init__(self, target=None, *args, **kwargs):
        super(DatacrawlerSpider, self).__init__(*args, **kwargs)

        config = ConfigParser()
        config.read('spiders.ini')

        self.allowed_domains = [config.get(target, 'allowed_domains')]
        self.start_urls = [config.get(target, 'start_urls')]
        self.url_v = config.get(target, 'start_urls')
        self.title_v = config.get(target, 'title')
        self.body_v = config.get(target, 'body')
        self.parent_v = config.get(target, 'parent')

        print(self.start_urls)

    rules = [
        Rule(
            LinkExtractor(
                allow=('.*'),
                deny=()
            ),
            callback='parse_item',
            follow=True
        )
    ]

    def parse_item(self, response):
        item = DatacrawlerItem()
        item['url'] = response.url

        # Replace filesystem path notations with relative url paths.
        url = urlparse(response.url)
        directories = list(filter(None, url.path.split('/')))
        del directories[-1]
        ancestorCount = len(directories)

        # Generate a list of search/replace tuples.
        #
        # Example for a/b/c:
        #
        # [
        #     ('../../../', '/')
        #     ('../../', 'a/')
        #     ('../', 'a/b/')
        # ]
        REPLACEMENTS = []

        # Generate Search and Replace tuple for the max number of ancestors
        # for this page, ie. tuple('../../../', '/') for /a/b/c
        search_string = ''
        for i in range(ancestorCount):
            search_string += '../'
        REPLACEMENTS.append((search_string, '/'))

        # Generate tuple for lower level parents
        replace_string = ''
        dir_count = 1
        for i in directories:
            search_string = ''
            for k in range(ancestorCount - dir_count):
                search_string += '../'

            replace_string += '/' + i

            REPLACEMENTS.append((search_string, replace_string + '/'))
            dir_count += 1

        del REPLACEMENTS[-1]

        try:
            item['title'] = response.css(self.title_v).get().strip().title()
        except AttributeError:
            item['title'] = None

        try:
            item['body'] = response.css(self.body_v).get().strip()
            for search, replace in REPLACEMENTS:
                item['body'] = item['body'].replace(search, replace)
        except AttributeError:
            item['body'] = None

        try:
            item['parent'] = self.url_v + response.css(self.parent_v).get().strip()
        except AttributeError:
            item['parent'] = None

        yield item
