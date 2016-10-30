Arachnid
========
This project was used as a practical exercise in coroutines and asyncronous
programming in Python. It uses primarily the async/await syntax introduced in
Python3.5.

It is a modular web-crawling and web-scraping framework inspired by the Scrapy
project. If you are here because you want to use a mature web scraping
framework, I urge you to seek out Scrapy.


The Example
===========
A simple example.


Defining a Crawler
--------------------
Save the file as myexample.py


.. code-block:: python

    from arachnid import spider

    class ItemPrinter:
        def process_item(self, item, spider):
            print(item)
            return item


    class MyExample(arachnid.Spider):
        start_urls = ['http://news.ycombinator.com/']
        name = 'HackerNews'

        def parse(self, response):
            articles = response.css('tr.athing, tr.athing+tr')
            for idx in range(0, len(articles), 2):
                title_elm  = articles[idx]
                title = title_elm.css('.title a::text').extract_first()
                meta_elm = articles[idx+1]
                yield {'title': title}


Defining the configuration
--------------------------
You need to define a configuration for your crawl job to execute the above scraper.

.. code-block:: python

    spiders = [
        {'spider': 'myexample.MyExample',
         'spider_middleware': [],
         'downloader_middleware': [],
         'result_middleware': ['myexample.ItemPrinter']}
    ]

Save as myexamplesettings.py

Run `arachnid settings myexamplesettings.py`.


Features
========
* Built-in support for CSS/XPath data extraction using the .. _ Parsel: https://parsel.readthedocs.io library.
* Extensibility support, allowing you to plug-in your own functionality with a well-defined API (pipelines, middlewares).
* Ability to load multiple spiders with their own middleware.
