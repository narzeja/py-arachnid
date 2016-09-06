Arachnid
=========
This project was used as a practical exercise in coroutines and asyncronous programming in Python.
It uses both the asyncio library, as well as the async/await syntax introduced in Python3.5.

It is a modular web-crawling and web-scraping framework inspired by the Scrapy project.
If you are here because you want to use a mature web scraping framework, I urge you to seek out Scrapy.


The Example
===========
Here's a shitty example.

.. code-block:: python

    from arachnid import spider

    class myCrawler(spider.Spider):
        start_urls = ['https://www.google.com', ]
        name = 'TestCrawler'

        def parse(self, response):
            self.logger.info('Inside PARSE')
            yield Request('https://www.bing.com', self.another)
            yield Request('https://www.duckduckgo.com', self.another)
            yield Request('https://www.bbc.com', self.another)
            yield Request('https://www.yahoo.com', self.another)
            yield Request('https://www.startpage.com', self.another)

        def another(self, response):
            self.logger.info('Inside ANOTHER')
            yield {'test': 'asd'}


Features
========
* Built-in support for CSS/XPath data extraction
* Extensibility support, allowing you to plug-in your own functionality with a well-defined API (pipelines, middlewares).
*
