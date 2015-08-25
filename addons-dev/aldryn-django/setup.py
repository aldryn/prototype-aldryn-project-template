# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name="aldryn-django",
    version="1.6.11",
    install_requires=(
        'aldryn-addons',
        'Django==1.6.11',
        # setup utils
        'dj-database-url',
        'dj-email-url',
        'dj-redis-url',
        'django-cache-url',
        'django-appconf',
        'django-dotenv',
        'django-getenv',
        'aldryn-client',
        'webservices',
        'raven',
        'opbeat',
        # wsgi server related
        'uwsgi',
        'dj-static',
        # database
        'psycopg2',
        'structlog',
        'click',
    ),
    entry_points='''
        [console_scripts]
        aldryn-django=aldryn_django.cli:main
    ''',
    include_package_data=True,
    zip_safe=False,
)
