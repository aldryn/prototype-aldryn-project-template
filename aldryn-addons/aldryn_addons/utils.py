# -*- coding: utf-8 -*-
import json
import os


def boolean_ish(value):
    if isinstance(value, basestring):
        value = value.lower()
    if value in [True, 'true', '1', 'on', 'yes']:
        return True
    elif value in [False, 'false', '0', 'off', 'no']:
        return False
    return bool(value)


def json_from_file(path):
    try:
        with open(path) as fobj:
            return json.load(fobj)
    except ValueError as e:
        raise ValueError('{} ({})'.format(e, path))


def mkdirs(path):
    try:
        os.makedirs(path)
    except:
        if not os.path.exists(path):
            raise


def openfile(path):
    """
    opens the file, creating it and directories if needed
    """
    mkdirs(os.path.dirname(path))
    return open(path, 'w+')
