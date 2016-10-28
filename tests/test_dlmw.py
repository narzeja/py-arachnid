import pytest
from arachnid import downloadermw
from arachnid.response import Response
from arachnid.request import Request
from arachnid.exceptions import IgnoreRequest
from arachnid import spider
import logging
import uvloop
logger = logging.getLogger('test_logger')
logger.setLevel(logging.DEBUG)


@pytest.fixture
def middleware():
    return downloadermw.DownloaderMiddlewareManager()


@pytest.fixture
def test_spider():
    class MyTestSpider(spider.Spider):
        pass

    return MyTestSpider(name='test_spider')


@pytest.fixture
def loop():
    return uvloop.new_event_loop()


async def downloader(request, logger, spider):
    url = request.url
    return Response(url, body=b'my_body')


def test_no_middleware(middleware, test_spider, loop):
    expected_body = b'my_body'
    expected_url = 'http://foo.bar'
    req = Request('http://foo.bar', test_spider.parse)
    ret_response = loop.run_until_complete(middleware.download(downloader, req, logger, test_spider))
    assert isinstance(ret_response, Response)
    assert ret_response.body == expected_body
    assert ret_response.url == expected_url


def test_with_request_dropper(middleware, test_spider, loop):
    class RequestManipulator:
        def process_request(self, request, spider):
            raise IgnoreRequest

    middleware._add_middleware(RequestManipulator())

    original_url = 'http://foo.bar'
    req = Request(original_url, test_spider.parse)

    dropped_request = loop.run_until_complete(middleware.download(downloader, req, logger, test_spider))
    assert isinstance(dropped_request, IgnoreRequest)


def test_with_request_manipulator(middleware, test_spider, loop):
    class RequestManipulator:
        def process_request(self, request, spider):
            # only redirect certain requests
            if request.url == 'http://foo.bar':
                request.url = 'http://url-is-altered.com'
                return request

    middleware._add_middleware(RequestManipulator())

    original_url = 'http://foo.bar'
    expected_url = 'http://url-is-altered.com'
    req = Request(original_url, test_spider.parse)

    altered_request = loop.run_until_complete(middleware.download(downloader, req, logger, test_spider))
    assert isinstance(altered_request, Request)
    assert altered_request.url == expected_url

    proper_response = loop.run_until_complete(middleware.download(downloader, altered_request, logger, test_spider))
    assert isinstance(proper_response, Response)
    assert proper_response.url == expected_url
    assert proper_response.body == b'my_body'


def test_with_response_manipulator(middleware, test_spider, loop):
    class ResponseManipulator:
        def process_response(self, response, request, spider):
            return response

    middleware._add_middleware(ResponseManipulator())

    original_url = 'http://foo.bar'
    req = Request(original_url, test_spider.parse)

    ret_response = loop.run_until_complete(middleware.download(downloader, req, logger, test_spider))
    assert isinstance(ret_response, Response)
    assert ret_response.url == original_url


def test_with_response_manipulator_return_new_request(middleware, test_spider, loop):
    class ResponseManipulator:
        def process_response(self, response, request, spider):
            req = Request('http://new.url', spider.parse)
            return req

    middleware._add_middleware(ResponseManipulator())

    original_url = 'http://foo.bar'
    req = Request(original_url, test_spider.parse)

    ret_request = loop.run_until_complete(middleware.download(downloader, req, logger, test_spider))
    assert isinstance(ret_request, Request)
    assert ret_request.url == 'http://new.url'


def test_with_exception_handler_none(middleware, test_spider, loop):
    class ExceptionManipulator:
        def process_exception(self, request, exception, spider):
            return

    def failing_downloader(request, logger, spider):
        raise Exception('failed')

    middleware._add_middleware(ExceptionManipulator())

    original_url = 'http://foo.bar'
    req = Request(original_url, test_spider.parse)

    ret = loop.run_until_complete(middleware.download(failing_downloader, req, logger, test_spider))
    assert isinstance(ret, Exception)
    assert ret.args[0] == 'failed'


def test_with_exception_handler_iterable(middleware, test_spider, loop):
    class ExceptionManipulator:
        def process_exception(self, request, exception, spider):
            return [{'failed': 'ye'}]

    def failing_downloader(request, logger, spider):
        raise Exception('failed')

    middleware._add_middleware(ExceptionManipulator())

    original_url = 'http://foo.bar'
    req = Request(original_url, test_spider.parse)

    ret = loop.run_until_complete(middleware.download(failing_downloader, req, logger, test_spider))
    assert ret[0]['failed'] == 'ye'


def test_with_open_close_spider(test_spider, loop):
    class RequestManipulator:
        def __init__(self, state):
            self.state = state

        def open_spider(self, spider):
            self.state['foo'] = 'bar'

        def close_spider(self, spider):
            self.state.pop('foo')

    state = {}
    middleware = downloadermw.DownloaderMiddlewareManager(*(RequestManipulator(state),))
    middleware.open_spider(test_spider)
    assert state.get('foo') == 'bar'
    middleware.close_spider(test_spider)
    assert state.get('foo') is None
