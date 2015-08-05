# -*- coding: utf-8 -*-
import os
import dotenv
from getenv import env
import django.core.management


def manage(path):
    _setup(path=path)
    utility = django.core.management.ManagementUtility(None)
    utility.execute()


def wsgi(path):
    _setup(path=path)
    from django.core.wsgi import get_wsgi_application
    from dj_static import Cling
    return Cling(get_wsgi_application())


def _setup(path):
    os.environ['DJANGO_SETTINGS_MODULE'] = env('DJANGO_SETTINGS_MODULE', 'settings')
    dotenv_path = os.path.join(path, '.env')
    if os.path.exists(dotenv_path):
        print 'reading environment variables from {0}'.format(dotenv_path)
        dotenv.read_dotenv(dotenv_path)
