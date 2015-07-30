try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Privacy aware Daily Journal',
    'author': 'Balasankar C',
    'url': 'http://gitlab.com/balasankarc/rahasya',
    'download_url': 'http://gitlab.com/balasankarc/rahasya',
    'author_email': 'balasankarc@autistici.org',
    'version': '0.1',
    'packages': ['rahasya'],
    'scripts': ['bin/rahasya'],
    'name': 'rahasya'
}

setup(**config)
