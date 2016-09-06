""" Minimal example of arachnid.
Implements a basic scraper that opens Hacker News and yield the titles of the scraped articles..
"""
import arachnid


class MyExample(arachnid.Spider):
    start_urls = ['http://news.ycombinator.com/']
    name = 'MyExample'

    def parse(self, response):
        articles = response.css('tr.athing, tr.athing+tr')
        for idx in range(0, len(articles), 2):
            title_elm  = articles[idx]
            title = title_elm.css('.title a::text').extract_first()
            meta_elm = articles[idx+1]
            yield {'title': title}
