# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import Join, MapCompose, Identity, TakeFirst, Compose
from w3lib.html import remove_tags
from .utils.processors import Text, Number, Price, Date, Url, Image, PageUrl, Regex, Prepend, SafeHtml


class DatacrawlerItem(scrapy.Item):
    url = scrapy.Field(
        input_processor=Url(),
        output_processor=Join(),
    )
    title = scrapy.Field(
        input_processor=Text(),
        output_processor=Join(),
    )
    body = scrapy.Field()
    parent = scrapy.Field(
        input_processor=Url(),
        output_processor=Join(),
    )

class PageItem(scrapy.Item):
    url = scrapy.Field(
        input_processor=PageUrl(),
        output_processor=Join(),
    )
    title = scrapy.Field(
        input_processor=Text(),
        output_processor=Join(),
    )
    body = scrapy.Field()
    parent = scrapy.Field(
        input_processor=Url(),
        output_processor=Join(),
    )
    grandparent = scrapy.Field(
        input_processor=Url(),
        output_processor=Join(),
    )

class JusticeItem(scrapy.Item):
    url = scrapy.Field(
        input_processor=PageUrl(),
        output_processor=Join(),
    )
    title = scrapy.Field(
        input_processor=Text(),
        output_processor=Join(),
    )
    body = scrapy.Field()
    district = scrapy.Field(
        input_processor=Text(),
        output_processor=Join(),
    )
    division = scrapy.Field(
        input_processor=Regex('(Division\ (?i)[One|Two|Three|Four|Five|Six|1|2|3|4|5|6]*)'),
        output_processor=Join(),
    )
    image = scrapy.Field(
        input_processor=Compose(Regex('<img[^>]*src="([^"]+)"[^>]*>'), Prepend('https://www.courts.ca.gov')),
        output_processor=Join(),
    )
    role = scrapy.Field(
        input_processor=Regex('(?i)(Presiding|Associate)\ Justice'),
        output_processor=TakeFirst(),
    )
    marker = scrapy.Field(
        input_processor=Text(),
        output_processor=Join(),
    )
    bodytext = scrapy.Field(
        input_processor=Text(),
        output_processor=Join(),
    )