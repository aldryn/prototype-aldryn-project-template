# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf import urls
from django.conf.urls.i18n import i18n_patterns

def patterns():
    return [
        urls.url(r'^', urls.include(url))
        for url in getattr(settings, 'ADDON_URLS', [])
    ]

def i18n_patterns():
    return [
        urls.url(r'^', urls.include(url))
        for url in getattr(settings, 'ADDON_URLS_I18N', [])
    ]
