# -*- coding: utf-8 -*-
from django.conf import settings


def debug(request):
    # we don't use django.core.context_processors.debug because it does not set True for
    # ip that are not in INTERNAL_IPS
    # TODO: (django-cms) we should not use "debug" as variable for the yellow
    #       bar on the cms toolbar. it should be it's own setting that defaults
    #       to settings.DEBUG
    return {'debug': settings.DEBUG}
