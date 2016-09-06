import asyncio

from .middleware import MiddlewareManager


class PipelineManager(MiddlewareManager):
    """ PipelineManager.
Responsibilities:
 * Execute all middlewares that operate on Incoming Results/Requests (output from Spider).

process_item:
This method is called for each result produced by the spider.

 * run middleware on results from spider.
 * return the item for further processing.

"""

    name = 'pipeline middleware'
    def _add_middleware(self, pipe):
        super()._add_middleware(self, pipe)
        if hasattr(pipe, 'process_item'):
            self.methods['process_item'].append(pipe.process_item)

    async def process_item(self, item, logger, spider):
        logger.debug("Handling item: {} (from: {})".format(item, spider.name))
        async def process_chain(item):
            for method in self.methods['process_item']:
                item = method(item=item, spider=spider)
            return item

        return await process_chain(item)

