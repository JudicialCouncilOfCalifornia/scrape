import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import DatacrawlerItem
from configparser import ConfigParser  # ver. < 3.0

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
        item['title'] = response.css(self.title_v).get().strip()
        item['body'] = response.css(self.body_v).get().strip()
        item['parent'] = self.url_v + response.css(self.parent_v).get().strip()
        yield item
