# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf import urls
from django.conf.urls.i18n import i18n_patterns

def patterns():
    args = []
    for pat in getattr(settings, 'ADDON_URLS', []):
        print pat
        args.append(
            urls.url(
                r'^',
                urls.include(pat),
            )
        )
    urlpatterns = urls.patterns('', *args)
    args = []
    for pat in getattr(settings, 'ADDON_URLS_I18N', []):
        print pat
        args.append(
            urls.url(
                r'^',
                urls.include(pat),
            )
        )
    i18n_urlpatterns = i18n_patterns('', *args)
    return urlpatterns + i18n_urlpatterns
