from __future__ import absolute_import

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

from ..utils.spiders import BasePortiaSpider
from ..utils.processors import Item, Field
from ..items import JusticeItem

class DcaJusticeSpider(BasePortiaSpider):
    name = "dca-justices"
    allowed_domains = ['www.courts.ca.gov']
    start_urls = [
        'https://www.courts.ca.gov/2344.htm',
        'https://www.courts.ca.gov/2129.htm',
        'https://www.courts.ca.gov/2514.htm',
        'https://www.courts.ca.gov/2524.htm',
        'https://www.courts.ca.gov/2998.htm',
        'https://www.courts.ca.gov/3000.htm'
    ]

    rules = [
        Rule(
            LinkExtractor(
                allow=('.*'),
                deny=(
                    '7418.htm',
                    '7419.htm',
                    '7433.htm',
                    '7434.htm',
                    '7435.htm',
                    '7431.htm',
                    '3162.htm',
                    '3154.htm',
                    '4052.htm',
                    '7425.htm',
                    '7426.htm',
                    '4081.htm',
                    '4097.htm',
                    '4192.htm',
                    '7420.htm',
                    '/cms',
                    'cfm',
                    'find-my-court',
                    'selfhelp'
                ),
                restrict_xpaths=(
                    '//*[@id="mainPanel"]//a'
                )
            ),
            callback='parse_item',
            follow=True
        )
    ]
    custom_settings = {
        "DEPTH_LIMIT": 2
    }

    items = [
        [
            Item(
                JusticeItem,
                None,
                'body',
                [
                    Field(
                        'marker',
                        '//*[@id="breadcrumb"]//a[4][text()="Justices"]',
                        [],
                        True,
                        'xpath'),
                    Field(
                        'url',
                        '#none',
                        []),
                    Field(
                        'title',
                        '#mainPanel h1::text',
                        []),
                    Field(
                        'district',
                        '#breadcrumb a:nth-of-type(3)::text',
                        []),
                    Field(
                        'division',
                        '#twoColumns',
                        []),
                    Field(
                        'role',
                        '#twoColumns',
                        []),
                    Field(
                        'image',
                        '#twoColumns',
                        []),
                    Field(
                        'body',
                        '#twoColumns',
                        [])
                ])
        ]
    ]
