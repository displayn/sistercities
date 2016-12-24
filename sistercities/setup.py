try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Sister Cities',
    'author': 'Tobias Scholz',
    'url': 'URL to get it at.',
    'download_url': 'Where to download it.',
    'author_email': 'fh@display.name',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['NAME'],
    'scripts': [],
    'name': 'Sister Cities'
}

setup(**config)