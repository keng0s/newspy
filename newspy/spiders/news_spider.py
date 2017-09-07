import scrapy
from newspy.items import ArticleItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import re


class NewsSpider(CrawlSpider):
    name = 'news'
    allowed_domains = ['bbc.com']
    start_urls = ['http://www.bbc.com/news']

    rules = (
        Rule(
            LinkExtractor(allow=(), unique=True),
            callback='parse_item'
        ),
    )

    def parse_item(self, response):
        page_type = response.xpath("//meta[@property='og:type']/@content").extract_first()

        if page_type == 'article':
            item = ArticleItem()
            item['url'] = response.url
            item['title'] = response.xpath("//meta[@property='og:title']/@content").extract_first() or \
                            response.xpath("//h1[@itemprop='headline']/text()").extract_first()
            item['description'] = response.xpath("//meta[@property='og:description']/@content").extract_first()
            item['author'] = response.xpath("//meta[@property='article:author']/@content").extract_first()
            item['section'] = response.xpath("//meta[@property='article:section']/@content").extract_first()
            item['keywords'] = response.xpath("//meta[@name='keywords']/@content").extract_first()

            text_contents = response.xpath("//div[@itemprop='articleBody' or @property='articleBody']/p").extract()
            item['text'] = re.sub(r'<.*?>', ' ', ''.join(text_contents)).strip() if text_contents else None

            return item

