from __future__ import absolute_import

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

from ..utils.spiders import BasePortiaSpider
from ..utils.processors import Item, Field
from ..items import PageItem

class DcaPageSpider(BasePortiaSpider):
    name = "dca-page"
    allowed_domains = ['www.courts.ca.gov']
    start_urls = ['https://www.courts.ca.gov/courtsofappeal.htm']

    rules = [
        Rule(
            LinkExtractor(
                allow=('.*'),
                deny=(),
                restrict_xpaths=(
                    '//ul[@id="leftNav"]//a'
                )
            ),
            callback='parse_item',
            follow=True
        )
    ]
    items = [
        [
            Item(
                PageItem,
                None,
                'body',
                [
                    Field(
                        'url',
                        '#none',
                        []),
                    Field(
                        'title',
                        '#mainPanel h1::text',
                        []),
                    Field(
                        'body',
                        '#mainContent',
                        []),
                    Field(
                        'parent',
                        '#breadcrumb a:last-of-type::attr(href)',
                        []),
                    Field(
                        'grandparent',
                        '#breadcrumb > a:nth-of-type(2)::attr(href)',
                        [])
                ])
        ]
    ]
