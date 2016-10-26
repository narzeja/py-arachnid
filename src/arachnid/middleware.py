from collections import defaultdict


class MiddlewareManager:
    name = 'abstract middleware manager'

    def __init__(self, *middlewares):
        self.middlewares = middlewares
        self.methods = defaultdict(list)
        for mw in self.middlewares:
            self._add_middleware(mw)

    def _add_middleware(self, mw):
        if hasattr(mw, 'open_spider'):
            self.methods['open_spider'].append(mw.open_spider)
        if hasattr(mw, 'close_spider'):
            self.methods['close_spider'].insert(0, mw.close_spider)

    def open_spider(self, spider):
        for method in self.methods['open_spider']:
            method(spider=spider)

    def close_spider(self, spider):
        for method in self.methods['close_spider']:
            method(spider=spider)
