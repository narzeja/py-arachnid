import asyncio
from . import middleware
from .request import Request
from .response import Response


def _isiterable(maybe_iter):
    return hasattr(maybe_iter, '__iter__')


class SpiderMiddlewareManager(middleware.MiddlewareManager):
    """
    Responsibilities:

    * Execute all middlewares that operate on Responses (input to Spider)
    * Execute all middlewares that operate on Incoming Results/Requests (output from Spider).

.. method:: process_spider_input(response)

    This method is called for each response that goes through the spider middleware and into the spider, for processing.

    * Run middlewares on responses sent to Spiders
    * Returns either None or raises an exception


.. method:: process_spider_output(result)

    This method is called with the results returned from the Spider, after it has processed the response.

    * Run middlewares on results produced by Spider
    * Must return an iterable of Request or dict (iterable may yield both)

.. method:: process_spider_exception(failure)

    ...

"""

    name = 'spider middleware'

    def _add_middleware(self, mw):
        super()._add_middleware(mw)
        if hasattr(mw, 'process_spider_input'):
            self.methods['process_spider_input'].append(mw.process_spider_input)
        if hasattr(mw, 'process_spider_output'):
            self.methods['process_spider_output'].insert(0, mw.process_spider_output)
        if hasattr(mw, 'process_spider_exception'):
            self.methods['process_spider_exception'].insert(0, mw.process_spider_exception)

    async def scrape_response(self, scrape_func, response, request, logger, spider):
        logger.debug("Handling response: {} (code: {}, from: {})".format(response.url, response.status, spider.name))

        async def process_spider_input(response):
            for method in self.methods['process_spider_input']:
                result = method(response=response, spider=spider)
                assert result is None, \
                    'Middleware {}.process_spider_input must returns None or raise an exception, got {} '.format(
                        method.__class__.__name__, type(result))
            return scrape_func(response)

        async def process_spider_output(result):
            for method in self.methods['process_spider_output']:
                result = method(response=response, result=result, spider=spider)
                assert _isiterable(result), \
                    'Middleware {}.process_spider_output must returns an iterable object, got {} '.format(
                        method.__class__.__name__, type(result))
            return result

        async def process_spider_exception(_failure):
            exception = _failure
            for method in self.methods['process_spider_exception']:
                result = method(response=response, exception=exception, spider=spider)
                assert result is None or _isiterable(result), \
                    'Middleware {}.process_spider_exception must returns None, or an iterable object, got {}'.format(
                        method.__class__.__name__, type(result))
                if result is not None:
                    return result
            return _failure

        results = []
        try:
            for i in await process_spider_input(response):
                results.append(await process_spider_output(i))
        except Exception as exc:
            results = await process_spider_exception(exc)
        return results
