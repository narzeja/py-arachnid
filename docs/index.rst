.. Arachnid documentation master file, created by
   sphinx-quickstart on Mon Sep  5 10:34:05 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Arachnid
========
This project was used as a practical exercise in coroutines and asyncronous
programming in Python. It uses primarily the async/await syntax introduced in
Python3.5.

It is a modular web-crawling and web-scraping framework inspired by the `Scrapy
<http://scrapy.readthedocs.io>`_ project. If you are here because you want to
use a mature web scraping framework, I urge you to seek out `Scrapy
<http://scrapy.readthedocs.io>`_.


The Example
===========
A simple example that fetches the first page of articles from the `Hackernews
<https://news.ycombinator.com/>`_ frontpage.


Defining a Crawler
--------------------
Save the file as `myexample.py`.


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

Save as `myexamplesettings.py` and issue the following command to execute your job:


.. code-block:: bash

  arachnid settings myexamplesettings.py


Features
========
* Built-in support for CSS/XPath data extraction using the `Parsel <http://parsel.readthedocs.io>`_ library.
* Extensibility support, allowing you to plug-in your own functionality with a well-defined API (pipelines, middlewares).
* Ability to load multiple spiders with their own middleware.


TODO
====
* Find another module for performing http requests. Aiohttp.client is fine but does not support Socks. Requests itself is excellent but is not asynchronous. Make a fork of Requests and rewrite to async? Maybe `aiosocks <https://github.com/nibrag/aiosocks>`_?
* Provide an option to plug in different http request libraries. Kind of follows the above.
* Binary data (images/videos/etc.) downloading. Figure out a clean way to handle that, so it doesn't get wrapped in an HTML Response object (with Parsel selectors enabled and all).
* Make a default result middleware to save collected results to disk?
* Naming scheme for middlewares. It's inconsistent right now.


Contents:
=========

.. toctree::
   :maxdepth: 2


API:
----

.. toctree::
   :maxdepth: 2

   api_middleware


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


