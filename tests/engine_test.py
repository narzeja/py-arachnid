from arachnid import engine
from arachnid import spider
from arachnid.request import Request


class myCrawler(spider.Spider):
    start_urls = ['https://www.google.com', ]
    name = 'TestCrawler'

    def parse(self, response):
        self.logger.info('Inside PARSE')
        yield Request('https://www.bing.com', self.another)
        # yield Request('https://www.duckduckgo.com', self.another)
        # yield Request('https://www.bbc.com', self.another)
        # yield Request('https://www.yahoo.com', self.another)
        # yield Request('https://www.startpage.com', self.another)

    def another(self, response):
        self.logger.info('Inside ANOTHER')
        yield {'test': 'asd'}


def test_engine():
    e = engine.Engine()
    e.register_spider(myCrawler)
    e.start()


if __name__ == "__main__":
    test_engine()
