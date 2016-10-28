from setuptools import setup, find_packages
from os.path import join, dirname


with open(join(dirname(__file__), 'requirements.txt'), 'r') as fd:
    requirements = fd.read().split('\n')

with open(join(dirname(__file__), 'requirements-dev.txt'), 'r') as fd:
    dev_requirements = fd.read().split('\n')

with open('README.rst', 'r') as f:
    readme = f.read()

with open(join(dirname(__file__), 'VERSION'), 'r') as f:
    version = f.read().strip()

with open('HISTORY.rst', 'r') as f:
    history = f.read()

setup(
    name='arachnid',
    version=version,
    url='http://www.github.com/narzeja/arachnid',
    author='Arachnid developers',
    maintainer='narzeja',
    maintainer_email='narzeja@gmail.com',
    license='BSD',
    description="Async Web Crawling and Scraping",
    long_description=readme +'\n\n' + history,
    packages=find_packages('src', exclude=('tests', 'tests.*')),
    package_dir={'': 'src'},
    package_data={'': ['LICENSE'], '': ['VERSION']},
    include_package_data=True,
    entry_points={
        'console_scripts': ['arachnid = arachnid.cli:cli'],
    },
    install_requires=requirements,
    extras_require={'develop': dev_requirements},
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Operating System :: POSIX :: Linux',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
