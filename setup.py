try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Tool to search files for matching strings',
    'author': 'Steven Hansen',
    'url': 'https://github.com/sahglie/logfind',
    'download_url': 'Where to download it.',
    'author_email': 'sahglie@gmail.com',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['logfind'],
    'scripts': ["bin/logfind"],
    'name': 'logfind'
}

setup(**config)
