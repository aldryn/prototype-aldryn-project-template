# -*- coding: utf-8 -*-
import imp
import os
import shutil
import uuid
from aldryn_addons import utils
from pprint import pformat


def save_settings_dump(settings, path):
    to_dump = {key: value for key, value in settings.items() if key == key.upper()}
    with open(path, 'w+') as fobj:
        fobj.write(
            pformat(
                to_dump,
                indent=4,
            )
        )


def count_str(number):
    return '{0:05d}'.format(number)


def load(settings):
    settings['BASE_DIR'] = settings.get(
        'BASE_DIR',
        os.path.dirname(os.path.abspath(settings['__file__']))
    )
    settings['ADDONS_DIR'] = settings.get(
        'ADDONS_DIR',
        os.path.join(settings['BASE_DIR'], 'addons')
    )
    utils.mkdirs(settings['ADDONS_DIR'])
    # TODO: .debug is not multi-process safe!
    debug_path = os.path.join(settings['ADDONS_DIR'], '.debug')
    shutil.rmtree(debug_path, ignore_errors=True)
    utils.mkdirs(debug_path)

    def dump(obj, count, name):
        dump_name = '{}-{}.dump'.format(count_str(count), name)
        dump_path = os.path.join(debug_path, dump_name)
        save_settings_dump(obj, dump_path)
        return count + 1

    debug_count = 0
    debug_count = dump(settings, debug_count, 'initial')
    # load global defaults
    from django.conf import global_settings
    for key, value in global_settings.__dict__.items():
        if not key in settings:
            settings[key] = value
    debug_count = dump(settings, debug_count, 'load-globals')
    # normalise settings
    for key, value in settings.items():
        if isinstance(value, tuple):
            settings[key] = list(value)
    debug_count = dump(settings, debug_count, 'normalise')
    # add Addon default settings if they are not there yet
    if 'ADDON_URLS' not in settings:
        settings['ADDON_URLS'] = []
    if 'ADDON_URLS_I18N' not in settings:
        settings['ADDON_URLS_I18N'] = []
    settings['INSTALLED_APPS'].append('aldryn_addons')
    # load Addon settings
    if not (settings['INSTALLED_ADDONS'] and settings['ADDONS_DIR']):
        return
    for addon_name in settings['INSTALLED_ADDONS']:
        if os.path.isabs(addon_name):
            addon_path = addon_name
            addon_name = os.path.basename(os.path.normpath(addon_path))
        else:
            addon_path = os.path.join(settings['ADDONS_DIR'], addon_name)
        load_addon_settings(name=addon_name, path=addon_path, settings=settings)
        debug_count = dump(settings, debug_count, addon_name)


def load_addon_settings(name, path, settings):
    addon_json_path = os.path.join(path, 'addon.json')
    addon_json = utils.json_from_file(addon_json_path)
    addon_settings_path = os.path.join(path, 'settings.json')
    addon_settings = utils.json_from_file(addon_settings_path)
    # TODO: once we have "secrets" support on certain field:
    #       load the secret settings from environment variables here and add
    #       them to addon_settings
    aldryn_config_py_path = os.path.join(path, 'aldryn_config.py')
    if os.path.exists(aldryn_config_py_path):
        aldryn_config = imp.load_source(
            '{}_{}'.format(name, uuid.uuid4()).replace('-', '_'),
            aldryn_config_py_path,
        )
        # Usually .to_settings() implementations will update settings in-place, as
        # well as returning the resulting dict.
        # But because the API is not defined clear enough, some might return a new
        # dict with just their generated settings. So we also update the settings
        # dict here, just to be sure.
        if hasattr(aldryn_config, 'Form'):
            settings.update(
                aldryn_config.Form().to_settings(addon_settings, settings)
            )
    # backwards compatibility for when installed-apps was defined in addon.json
    for app in addon_json.get('installed-apps', []):
        if app not in settings['INSTALLED_APPS']:
            settings['INSTALLED_APPS'].append(app)
    # remove duplicates
    settings['INSTALLED_APPS'] = list(set(settings['INSTALLED_APPS']))
    # settings['MIDDLEWARE_CLASSES'] = list(set(settings['MIDDLEWARE_CLASSES']))
