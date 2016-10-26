import click
from . import utils
from . import engine

@click.group()
def cli():
    pass

@click.command()
@click.argument('filename', type=click.Path(exists=True))
def crawler(filename):
    eng = engine.Engine()
    try:
        module, path = utils.load_module(filename)
    except ImportError as exc:
        print(exc)
        print('failed importing thing')
    else:
        eng.register_spider(module.MyExample)
        eng.start()

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
            module = utils.load_module(spider['spider'])
        except ImportError as exc:
            print(exc)
            print('failed importing spider')
        else:
            spider = utils.load_spider(module)
            eng.register_spider(spider)
    eng.start()


cli.add_command(crawler)
cli.add_command(settings)


if __name__ == "__main__":
    cli()
