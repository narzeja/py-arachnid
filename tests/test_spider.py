import pytest
from arachnid import spider
from arachnid.response import Response
import logging
logger = logging.getLogger('test_logger')


def test_spider_no_name():
    class MyTestSpider(spider.Spider):
        pass

    with pytest.raises(ValueError) as e_info:
        MyTestSpider()


def test_spider_descriptor_name():
    class MyTestSpider(spider.Spider):
        name = 'foo'

    my_spider = MyTestSpider()
    assert my_spider.name == 'foo'


def test_spider_start_urls():
    class MyTestSpider(spider.Spider):
        name = 'foo'
        start_urls = ['http://my.url']

    my_spider = MyTestSpider()
    assert 'http://my.url' in my_spider.start_urls


def test_spider_no_parse():
    class MyTestSpider(spider.Spider):
        name = 'foo'
        start_urls = ['http://my.url']

    my_spider = MyTestSpider()
    response = Response(my_spider.start_urls[0], body=b'no_body')
    with pytest.raises(NotImplementedError) as e_info:
        my_spider.parse(response)


def test_spider_close_it_up_with_closed():
    class MyTestSpider(spider.Spider):
        name = 'foo'
        start_urls = ['http://my.url']
        def closed(self, reason):
            return reason

    my_spider = MyTestSpider(logger=logger)
    result = my_spider.close_spider('shutdown')
    assert result == 'shutdown'


def test_spider_close_it_up_no_closed():
    class MyTestSpider(spider.Spider):
        name = 'foo'
        start_urls = ['http://my.url']

    my_spider = MyTestSpider(logger=logger)
    result = my_spider.close_spider('shutdown')
    assert result is None
