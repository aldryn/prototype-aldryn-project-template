# -*- coding: utf-8 -*-

INSTALLED_ADDONS = [
    # <INSTALLED_ADDONS>  # Warning: this is auto-generated. Manual changes will be overwritten.
    'aldryn-django',
    'aldryn-cms',
    'aldryn-newsblog',
    # </INSTALLED_ADDONS>
]


import aldryn_addons.settings
aldryn_addons.settings.load(locals())


INSTALLED_APPS.extend([
    # add you project specific apps here
])

TEMPLATE_CONTEXT_PROCESSORS.extend([
    # add your template context processors here
])

MIDDLEWARE_CLASSES.extend([
    # add your own middlewares here
])
