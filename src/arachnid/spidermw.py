import asyncio
from . import middleware
from .request import Request
from .response import Response


def _isiterable(maybe_iter):
    return hasattr(maybe_iter, '__iter__')


class SpiderMiddlewareManager(middleware.MiddlewareManager):
    """ SpiderMiddlewareManager.
Responsibilities:
 * Execute all middlewares that operate on Responses (input to Spider)
 * Execute all middlewares that operate on Incoming Results/Requests (output from Spider).

process_spider_input:
This method is called for each response that goes through the spider middleware and into the spider, for processing.

 * Run middlewares on responses sent to Spiders
 * Returns either None or raises an exception


process_spider_output:
This method is called with the results returned from the Spider, after it has processed the response.

 * Run middlewares on results produced by Spider
 * Must return an iterable of Request or dict (iterable may yield both)

"""

    name = 'spider middleware'

    def _add_middleware(self, mw):
        super()._add_middleware(self, mw)
        if hasattr(mw, 'process_spider_input'):
            self.methods['process_spider_input'].append(mw.process_spider_input)
        if hasattr(mw, 'process_spider_output'):
            self.methods['process_spider_output'].insert(0, mw.process_spider_output)
        if hasattr(mw, 'process_spider_exception'):
            self.methods['process_spider_exception'].insert(0, mw.process_spider_exception)

    @asyncio.coroutine
    def scrape_response(self, scrape_func, response, request, logger, spider):
        logger.debug("Handling response: {} (code: {}, from: {})".format(response.url, response.status, spider.name))

        @asyncio.coroutine
        def process_spider_input(response):
            for method in self.methods['process_spider_input']:
                result = method(response=response, spider=spider)
                assert result is None, \
                    'Middleware {}.process_spider_input must returns None or raise an exception, got {} '.format(
                        method.__class__.__name__, type(result))
            yield from scrape_func(response)

        @asyncio.coroutine
        def process_spider_output(result):
            for method in self.methods['process_spider_output']:
                result = method(response=response, result=result, spider=spider)
                assert _isiterable(result), \
                    'Middleware {}.process_spider_output must returns an iterable object, got {} '.format(
                        method.__class__.__name__, type(result))
            yield result

        @asyncio.coroutine
        def process_spider_exception(_failure):
            exception = _failure.value
            for method in self.methods['process_spider_exception']:
                result = method(response=response, exception=exception, spider=spider)
                assert result is None or _isiterable(result), \
                    'Middleware {}.process_spider_exception must returns None, or an iterable object, got {}'.format(
                        method.__class__.__name__, type(result))
                if result is not None:
                    return result
            return _failure

        # def process_spider_exception(response):
        #     return

        for i in process_spider_input(response):
            yield from process_spider_output(i)
