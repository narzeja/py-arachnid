import click
from . import utils
from . import engine

@click.group()
def cli():
    pass


# @click.command()
# @click.argument('filename', type=click.Path(exists=True))
# def crawler(filename):
#     eng = engine.Engine()
#     try:
#         module, path = utils.load_module_py(filename)
#     except ImportError as exc:
#         print(exc)
#         print('failed importing thing')
#     else:
#         eng.register_spider(module.MyExample)
#         eng.start()


@click.command()
@click.option('-d', is_flag=True, default=False)
@click.argument('filename', type=click.Path(exists=True))
def settings(filename, d):
    # eng = engine.Engine()
    try:
        settings = utils.load_settings(filename)
        settings.log_level = 'DEBUG' if d else 'INFO'
        eng = engine.Engine.from_settings(settings)
    except ImportError as exc:
        print(exc)
        print('failed importing settings file')
        raise

    for spider in settings.spiders:
        try:
            module, _ = utils.load_module(spider['spider'])
        except ImportError as exc:
            print(exc)
            print('failed importing spider')
            raise
        else:
            spider_obj = utils.load_spider(module)
            registered = eng.register_spider(spider_obj)
            if not registered:
                continue

            for mw in spider.get('spider_middleware', []):
                mw_obj = utils.load_module_obj(mw)
                eng.spiders[registered.name]['spidermwmanager']._add_middleware(mw_obj())

            for mw in spider.get('result_middleware', []):
                mw_obj = utils.load_module_obj(mw)
                eng.spiders[registered.name]['resultmwmanager']._add_middleware(mw_obj())

    eng.start()


# cli.add_command(crawler)
cli.add_command(settings)


if __name__ == "__main__":
    cli()
