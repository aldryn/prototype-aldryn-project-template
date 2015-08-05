# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls import patterns, url, include
from django.conf.urls.i18n import i18n_patterns
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
