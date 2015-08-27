# -*- coding: utf-8 -*-
from django.conf.urls.i18n import i18n_patterns as django_i18n_patterns


def i18n_patterns(*args):
    """
    compatibility shim for i18n_patterns. In django 1.8 the prefix parameter
    was deprecated. We want to avoid having to change anything in the projects
    root urls.py when new versions of Django are released.
    """
    return django_i18n_patterns('', *args)
