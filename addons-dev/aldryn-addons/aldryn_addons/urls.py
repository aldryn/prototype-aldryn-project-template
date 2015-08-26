# -*- coding: utf-8 -*-
"""
usage in root urls.py:

import aldryn_addons.urls

urlpatterns = patterns(
    '',
    # add your own patterns here
    *aldryn_addons.urls.patterns()
) + i18n_patterns(
    '',
    # add your own i18n patterns here
    url(r'^myapp/', include('myapp.urls')),
    *aldryn_addons.urls.i18n_patterns()  # MUST be the last entry!
)
"""
from django.conf import settings
from django.conf import urls


def patterns():
    pats = [
        urls.url(r'^', urls.include(url))
        for url in getattr(settings, 'ADDON_URLS', [])
    ]
    last_url = getattr(settings, 'ADDON_URLS_LAST', None)
    if last_url:
        pats.append(
            urls.url(r'^', urls.include(last_url))
        )
    return pats


def i18n_patterns():
    pats = [
        urls.url(r'^', urls.include(url))
        for url in getattr(settings, 'ADDON_URLS_I18N', [])
    ]
    last_url = getattr(settings, 'ADDON_URLS_I18N_LAST', None)
    if last_url:
        pats.append(
            urls.url(r'^', urls.include(last_url))
        )
    return pats
