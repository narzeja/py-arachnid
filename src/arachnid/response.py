
class Response:
    def __init__(self, url, status=200, headers=None, body=b'', flags=None, request=None):
        self._cached_selector = None
        self.headers = headers or {}
        self.status = int(status)
        self.body = body
        self.url = url
        self.request = request
        self.flags = [] if flags is None else list(flags)

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, url):
        if isinstance(url, str):
            self._url = url
        else:
            raise TypeError('%s url must be str, got %s:' % (type(self).__name__,
                type(url).__name__))

    @property
    def body(self):
        return self._body

    @body.setter
    def body(self, body):
        if body is None:
            self._body = b''
        elif not isinstance(body, bytes):
            raise TypeError(
                "Response body must be bytes. "
                "If you want to pass unicode body use TextResponse "
                "or HtmlResponse.")
        else:
            self._body = body

    @property
    def selector(self):
        from parsel import Selector
        if self._cached_selector is None:
            self._cached_selector = Selector(self.body.decode('utf-8'))
        return self._cached_selector

    def xpath(self, query):
        return self.selector.xpath(query)

    def css(self, query):
        return self.selector.css(query)
