import pytest
import uvloop
import logging
from arachnid import pipeline
from arachnid import spider


@pytest.fixture
def logger():
    return logging.getLogger('test_logger')


@pytest.fixture
def test_spider():
    class MyTestSpider(spider.Spider):
        pass

    return MyTestSpider(name='test_spider')

@pytest.fixture
def middleware():
    class GenericMiddleware:
        def process_item(self, item, spider):
            return item
    return GenericMiddleware()


@pytest.fixture
def loop():
    return uvloop.new_event_loop()


def test_add_middleware(middleware):
    manager = pipeline.PipelineManager()
    manager._add_middleware(middleware)
    assert middleware.process_item in manager.methods['process_item']


def test_add_middleware_no_process():
    class GenericMiddleware:
        pass

    middleware = GenericMiddleware()
    manager = pipeline.PipelineManager()
    manager._add_middleware(middleware)
    assert not manager.methods['process_item']


def test_middleware_simple_process_item(test_spider, middleware, loop, logger):
    manager = pipeline.PipelineManager()
    manager._add_middleware(middleware)
    result = {'result': 'dummy'}
    processed_result = loop.run_until_complete(manager.process_item(result, logger, test_spider))
    assert processed_result == result


def test_middleware_manipulate_process_item(test_spider, loop, logger):
    class GenericMiddleware:
        def process_item(self, item, spider):
            item = {'result': 'dummy2'}
            return item

    middleware = GenericMiddleware()
    manager = pipeline.PipelineManager()
    manager._add_middleware(middleware)
    result = {'result': 'dummy'}
    processed_result = loop.run_until_complete(manager.process_item(result, logger, test_spider))
    assert processed_result['result'] == 'dummy2'


def test_middleware_manipulate_process_item_no_return(test_spider, loop, logger):
    class GenericMiddleware:
        def process_item(self, item, spider):
            return

    middleware = GenericMiddleware()
    manager = pipeline.PipelineManager()
    manager._add_middleware(middleware)
    result = {'result': 'dummy'}
    processed_result = loop.run_until_complete(manager.process_item(result, logger, test_spider))
    assert processed_result is None
