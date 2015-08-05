# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name="aldryn-cms",
    version="3.1.2",
    install_requires=(
        'django-cms==3.1.2',
        # common
        # TODO: mostly to be split out into other packages
        'django-compressor',
        'django-health-check',
        'YURL',
        'South',
        'requests',
        'Pillow',
        'lxml',
        'django-treebeard',
        'django-simple-captcha',
        'BeautifulSoup',
        'subprocess32',
        'django-parler',
        'django-robots',
        'aldryn-boilerplates',
        'aldryn-sites',
    ),
)
