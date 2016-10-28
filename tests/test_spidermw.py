import pytest
import uvloop
import logging
from arachnid import spidermw
from arachnid import spider
from arachnid.response import Response
from arachnid.request import Request


@pytest.fixture
def logger():
    return logging.getLogger('test_logger')


@pytest.fixture
def test_spider():
    class MyTestSpider(spider.Spider):
        def parse(self, response):
            yield {'dummy': 'result'}

    return MyTestSpider(name='test_spider')


@pytest.fixture
def loop():
    return uvloop.new_event_loop()

@pytest.fixture
def middleware():
    class GenericMiddleware:
        def process_spider_input(self, response, spider):
            return
        def process_spider_output(self, response, result, spider):
            return result
    return GenericMiddleware()


def test_add_middleware(test_spider, middleware, loop):
    manager = spidermw.SpiderMiddlewareManager()
    manager._add_middleware(middleware)
    assert middleware.process_spider_input in manager.methods['process_spider_input']
    assert middleware.process_spider_output in manager.methods['process_spider_output']


def test_with_open_close_spider(test_spider, loop):
    class GenericMiddleware:
        def __init__(self, state):
            self.state = state

        def open_spider(self, spider):
            self.state['foo'] = 'bar'

        def close_spider(self, spider):
            self.state.pop('foo')

    state = {}
    middleware = spidermw.SpiderMiddlewareManager(*(GenericMiddleware(state),))
    middleware.open_spider(test_spider)
    assert state.get('foo') == 'bar'
    middleware.close_spider(test_spider)
    assert state.get('foo') is None


def test_with_process_chain(test_spider, middleware, loop, logger):
    request = Request('http://www.url.com', test_spider.parse)
    response = Response('http://www.url.com', body=b'')
    expected_result = {'dummy': 'result'}
    state = {}
    manager = spidermw.SpiderMiddlewareManager(*(middleware,))

    result = loop.run_until_complete(
        manager.scrape_response(test_spider.parse, response, request, logger, test_spider))
    assert result[0]['dummy'] == expected_result['dummy']


def test_with_process_chain_failure(test_spider, loop, logger):
    class GenericMiddleware:
        def process_spider_input(self, response, spider):
            raise Exception('processing failed')
        def process_spider_exception(self, response, exception, spider):
            return 'processing failed'

    request = Request('http://www.url.com', test_spider.parse)
    response = Response('http://www.url.com', body=b'')
    expected_exception_value = 'processing failed'
    state = {}
    middleware = GenericMiddleware()
    manager = spidermw.SpiderMiddlewareManager(*(middleware,))
    assert middleware.process_spider_exception in manager.methods['process_spider_exception']

    processed_result = loop.run_until_complete(
        manager.scrape_response(test_spider.parse, response, request, logger, test_spider))
    assert processed_result == expected_exception_value


def test_with_process_chain_failure_without_handler(test_spider, loop, logger):
    class GenericMiddleware:
        def process_spider_input(self, response, spider):
            raise Exception('processing failed')


    request = Request('http://www.url.com', test_spider.parse)
    response = Response('http://www.url.com', body=b'')
    expected_exception_value = 'processing failed'
    state = {}
    manager = spidermw.SpiderMiddlewareManager(*(GenericMiddleware(),))

    exception = loop.run_until_complete(
        manager.scrape_response(test_spider.parse, response, request, logger, test_spider))
    assert exception.args[0] == expected_exception_value


def test_with_process_chain_failure_returning_none(test_spider, loop, logger):
    class GenericMiddleware:
        def process_spider_input(self, response, spider):
            raise Exception('processing failed')
        def process_spider_exception(self, response, exception, spider):
            return

    request = Request('http://www.url.com', test_spider.parse)
    response = Response('http://www.url.com', body=b'')
    expected_exception_value = 'processing failed'
    state = {}
    manager = spidermw.SpiderMiddlewareManager(*(GenericMiddleware(),))

    exception = loop.run_until_complete(
        manager.scrape_response(test_spider.parse, response, request, logger, test_spider))
    assert exception.args[0] == expected_exception_value
