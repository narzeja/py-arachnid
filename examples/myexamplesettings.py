# spider_location = 'myexample.py'

engine = {'executers': 5}


spiders = [
    {'spider': 'myexample.MyExample',
     'spider_middleware': [],
     'downloader_middleware': [],
     'result_middleware': ['myexample.JSONSaver']}
]
