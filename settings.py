# -*- coding: utf-8 -*-
import os
import json


ADDONS_DIR = os.path.join(os.path.dirname(__file__), 'addons')
INSTALLED_ADDONS = [
    'aldryn-django',
    'aldryn-cms',
    # <INSTALLED_ADDONS>
    # Warning: this is auto-generated by aldryn
    # </INSTALLED_ADDONS>
    # 'aldryn-newsblog',
    # 'aldryn-people',
]

import aldryn_addons.settings
aldryn_addons.settings.load(locals())
INSTALLED_APPS.append('aldryn_addons')
