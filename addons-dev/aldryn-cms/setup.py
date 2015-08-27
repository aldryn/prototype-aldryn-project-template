# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name="aldryn-cms",
    version="3.1.2",
    install_requires=(
        'aldryn-addons',
        'django-cms==3.1.2',
        'django-reversion',
        # common
        # TODO: mostly to be split out into other packages
        'django-compressor',
        'YURL',
        'South',
        'requests',
        'Pillow',
        'lxml',
        'django-treebeard',
        'django-simple-captcha',
        'BeautifulSoup',
        'django-parler',
        'django-robots',
        'aldryn-boilerplates',
        'django-filer',
        'django-hvad',
        'aldryn-snake',

        # default plugins
        # TODO: split into other packages
        'djangocms-googlemap',
        'djangocms-link',
        'djangocms-snippet',
        'djangocms-text-ckeditor',
        'cmsplugin-filer',
    ),
)
