# -*- coding: utf-8 -*-
import re
from django.conf import settings
from django.conf.urls import patterns, url, include
from django.conf.urls.i18n import i18n_patterns


urlpatterns = patterns(
    '',
    url(
        r'^%s(?P<path>.*)$' % re.escape(settings.STATIC_URL.lstrip('/')),
        'django.contrib.staticfiles.views.serve',
        {'insecure': True}
    ),
)
