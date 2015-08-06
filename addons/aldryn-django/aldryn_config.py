# -*- coding: utf-8 -*-
import os
import dj_database_url
import django_cache_url
import sys
import warnings
from aldryn_addons.utils import boolean_ish
from aldryn_client import forms
from getenv import env


class Form(forms.BaseForm):
    name = forms.CheckboxField('Name', required=False)

    def to_settings(self, data, settings):
        # TODO: once we have proper "secrets" support, these should not load
        #       from the env themselves anymore
        # TODO: some sort of warnings mechanism for required settings where
        #       defaults have been set (like SECRET_KEY)
        settings['BASE_DIR'] = settings.get(
            'BASE_DIR',
            os.path.dirname(os.path.abspath(settings['__file__']))
        )
        settings['DATA_ROOT'] = env('DATA_ROOT', os.path.join(settings['BASE_DIR'], 'data'))
        settings['SECRET_KEY'] = env('SECRET_KEY', 'this-is-not-very-random')
        settings['DEBUG'] = boolean_ish(env('DEBUG', False))
        settings['TEMPLATE_DEBUG'] = boolean_ish(env('TEMPLATE_DEBUG', settings['DEBUG']))

        settings['DATABASE_URL'] = env('DATABASE_URL')
        if settings['DATABASE_URL']:
            pass
        elif env('DJANGO_MODE') == 'build':
            settings['DATABASES']['default'] = {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        else:
            settings['DATABASE_URL'] = 'sqlite:///{}'.format(
                os.path.join(settings['DATA_ROOT'], 'db.sqlite3')
            )
            warnings.warn(
                'no database configured. Falling back to DATABASE_URL={0}'.format(
                    settings['DATABASE_URL']
                ),
                RuntimeWarning,
            )
        settings['DATABASES']['default'] = dj_database_url.parse(settings['DATABASE_URL'])

        settings['ALLOWED_HOSTS'] = env('ALLOWED_HOSTS', ['localhost', '*'])
        settings['ROOT_URLCONF'] = 'urls'
        settings['ADDON_URLS'].append('aldryn_django.urls')
        settings['ADDON_URLS_I18N'].append('aldryn_django.i18n_urls')

        settings['WSGI_APPLICATION'] = 'wsgi.application'

        if not settings['STATIC_URL']:
            settings['STATIC_URL'] = env('STATIC_URL', '/static/')
        if not settings['STATIC_ROOT']:
            settings['STATIC_ROOT'] = env(
                'STATIC_ROOT',
                os.path.join(settings['BASE_DIR'], 'static_collected'),
            )
        settings['STATICFILES_DIRS'] = [
            os.path.join(settings['BASE_DIR'], 'static'),
        ]

        if not settings['MEDIA_URL']:
            settings['MEDIA_URL'] = '/media/'
        if not settings['MEDIA_ROOT']:
            settings['MEDIA_ROOT'] = env('MEDIA_ROOT', os.path.join(settings['DATA_ROOT'], 'media'))

        settings['LANGUAGE_CODE'] = 'en'

        settings['INSTALLED_APPS'].extend([
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.sites',
            'django.contrib.messages',
            'django.contrib.admin',
            'django.contrib.staticfiles',
            'south',
        ])
        settings['SITE_ID'] = env('SITE_ID', 1)


        self.logging_settings(settings)
        self.cache_settings(settings)
        return settings

    def logging_settings(self, settings):
        settings['LOGGING'] = {
            'version': 1,
            'disable_existing_loggers': False,
            'filters': {
                'require_debug_false': {
                    '()': 'django.utils.log.RequireDebugFalse',
                },
                'require_debug_true': {
                    '()': 'django.utils.log.RequireDebugTrue',
                },
            },
            'handlers': {
                'console': {
                    'level': 'INFO',
                    'class': 'logging.StreamHandler',
                    'stream': sys.stdout,
                },
                'null': {
                    'class': 'django.utils.log.NullHandler',
                },
            },
            'loggers': {
                '': {
                    'handlers': ['console'],
                    'level': 'INFO',
                },
                'django': {
                    'handlers': ['console'],
                    'level': 'INFO',
                },
                'django.request': {
                    'handlers': ['console'],
                    'level': 'INFO',
                    'propagate': False,
                },
                'aldryn': {
                    'handlers': ['console'],
                    'level': 'INFO',
                },
                'py.warnings': {
                    'handlers': ['console'],
                },
            }
        }

    def cache_settings(self, settings):
        cache_url = env('CACHE_URL', settings.get('CACHE_URL'))
        if cache_url:
            settings['CACHES']['default'] = django_cache_url.parse(cache_url)
