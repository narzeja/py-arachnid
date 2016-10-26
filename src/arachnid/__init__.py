""" Experimental implementation of a Scraping Framework complete with middleware and pipelines.

Showcases both asyncio.coroutines decorators and the Py3.5 async/await syntax.

"""

from .spider import Spider
from .request import Request
from .response import Response
