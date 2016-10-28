import pytest
from arachnid.response import Response
from parsel import Selector


def test_response_with_none_str_url():
    with pytest.raises(TypeError) as e_info:
        Response(b'http://www.url.com')


def test_response_without_body():
    resp = Response('http://www.url.com')
    assert resp.body == b''


def test_response_with_none_body():
    resp = Response('http://www.url.com', body=None)
    assert resp.body == b''


def test_response_with_str_body():
    with pytest.raises(TypeError) as e_info:
        Response('http://www.url.com', body='fails')


def test_response_callable_selector():
    body = b'<html><body></body></html>'

    resp = Response('http://www.url.com', body=body)
    assert isinstance(resp.selector, Selector)

    # next call retrieves the cached selector
    assert resp._cached_selector == resp.selector


def test_response_simple_xpath_selection():
    body = b'<html><body>my body</body></html>'

    resp = Response('http://www.url.com', body=body)
    elm = resp.xpath('//body/text()').extract_first()
    assert elm == 'my body'


def test_response_simple_css_selection():
    body = b'<html><body>my body</body></html>'

    resp = Response('http://www.url.com', body=body)
    elm = resp.css('body::text').extract_first()
    assert elm == 'my body'
