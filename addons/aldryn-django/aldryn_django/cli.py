#-*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
import click
import os
import sys
import yaml
from getenv import env
from django.template import loader, Context
from django.conf import settings as django_settings
from aldryn_addons.utils import openfile

# add the current directory to pythonpath. So the project files can be read.
BASE_DIR = os.getcwd()
sys.path.insert(0, BASE_DIR)

settings = {}


@click.command()
def web():
    """
    launch the webserver of choice (uwsgi)
    """
    if any(settings[key] for key in ['ENABLE_NGINX', 'ENABLE_PAGESPEED', 'ENABLE_BROWSERCACHE']):
        # uwsgi behind nginx. possibly with pagespeed/browsercache
        start_with_nginx(settings)
    else:
        # pure uwsgi
        execute(start_uwsgi_command())


@click.command()
def worker():
    """
    coming soon: launch the background worker
    """
    # TODO: celery worker startup, once available
    pass


@click.command()
def migrate():
    """
    run any migrations needed at deploy time. most notably database migrations.
    """
    # TODO: create/integrate aldryn-addons migrate api
    pass



@click.group()
def main():
    if not os.path.exists(os.path.join(BASE_DIR, 'manage.py')):
        raise click.UsageError('make sure you are in the same directory as manage.py')
    from . import startup
    startup._setup(BASE_DIR)
    # TODO: there must be a better way
    global settings
    settings = {key: getattr(django_settings, key) for key in dir(django_settings)}


main.add_command(web)
main.add_command(worker)
main.add_command(migrate)


def execute(args, script=None):
    # TODO: is cleanup needed before calling exec? (open files, ...)
    command = script or args[0]
    os.execvp(command, args)


def start_uwsgi_command(port=None):
    return [
        'uwsgi',
        '--module=wsgi',
        '--http=0.0.0.0:{}'.format(port or settings.get('PORT')),
        '--workers={}'.format(settings['DJANGO_WEB_WORKERS']),
        '--max-requests={}'.format(settings['DJANGO_WEB_MAX_REQUESTS']),
        '--harakiri={}'.format(settings['DJANGO_WEB_TIMEOUT']),
    ]


def start_procfile_command(procfile_path):
    return [
        'forego',
        'start',
        '-f',
        procfile_path
    ]


def start_with_nginx(settings):
    # TODO: test with pagespeed and static or media on other domain
    if not all([settings['NGINX_CONF_PATH'], settings['NGINX_PROCFILE_PATH']]):
        raise click.UsageError('NGINX_CONF_PATH and NGINX_PROCFILE_PATH must be configured')
    procfile = yaml.safe_dump(
        {
            'nginx': 'nginx',
            'django': ' '.join(start_uwsgi_command(port=settings['BACKEND_PORT']))
        },
        default_flow_style=False,
    )
    nginx_template = loader.get_template('aldryn_django/configuration/nginx.conf')
    context = Context(dict(settings))
    nginx_conf = nginx_template.render(context)
    with openfile(settings['NGINX_CONF_PATH']) as f:
        f.write(nginx_conf)
    with openfile(settings['NGINX_PROCFILE_PATH']) as f:
        f.write(procfile)
    execute(start_procfile_command(settings['NGINX_PROCFILE_PATH']))


