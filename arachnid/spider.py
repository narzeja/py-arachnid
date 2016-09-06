

class Spider:
    name = None
    def __init__(self, name=None, **kwargs):
        if name is not None:
            self.name = name
        elif not getattr(self, 'name', None):
            raise ValueError("%s must have a name" % type(self).__name__)
        self.__dict__.update(kwargs)

        if not hasattr(self, 'start_urls'):
            self.start_urls = []

    def parse(self, response):
        raise NotImplementedError

    def close_spider(self, reason):
        self.reason = reason
        self.logger.info("Spider '%s' stopped (reason: %s)" % (self.name, reason))
        closed = getattr(self, 'closed', None)
        if callable(closed):
            return closed(reason)
