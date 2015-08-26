# -*- coding: utf-8 -*-
from aldryn_client import forms
import json


class Form(forms.BaseForm):
    cms_templates = forms.CharField('CMS Templates', required=True, initial='[["default.html", "Default"]]')

    def to_settings(self, data, settings):
        # TODO: break out a lot of this stuff into other Addons
        # aldryn-sites
        settings['INSTALLED_APPS'].extend([
            'aldryn_sites',
            # django-cms
            'cms',
            'treebeard',
            'menus',
            'sekizai',
            'djangocms_admin_style',
            'reversion',

            # django-filer
            'mptt',
        ])
        settings['TEMPLATE_CONTEXT_PROCESSORS'].extend([
            'sekizai.context_processors.sekizai',
            'cms.context_processors.cms_settings',
        ])
        settings['MIDDLEWARE_CLASSES'].extend([
            'cms.middleware.user.CurrentUserMiddleware',
            'cms.middleware.page.CurrentPageMiddleware',
            'cms.middleware.toolbar.ToolbarMiddleware',
            'cms.middleware.language.LanguageCookieMiddleware',
        ])

        settings['ADDON_URLS_I18N_LAST'] = 'cms.urls'

        settings['CMS_TEMPLATES'] = settings.get(
            'CMS_TEMPLATES',
            # TODO: optionally load from the json file for fast syncing?
            json.loads(data['cms_templates'])
        )

        # aldryn-boilerplates
        settings['ALDRYN_BOILERPLATE_NAME'] = settings.get('ALDRYN_BOILERPLATE_NAME', 'legacy')
        settings['INSTALLED_APPS'].append('aldryn_boilerplates')
        settings['TEMPLATE_CONTEXT_PROCESSORS'].append('aldryn_boilerplates.context_processors.boilerplate')
        settings['TEMPLATE_LOADERS'].insert(
            settings['TEMPLATE_LOADERS'].index('django.template.loaders.app_directories.Loader'),
            'aldryn_boilerplates.template_loaders.AppDirectoriesLoader'
        )
        settings['STATICFILES_FINDERS'].insert(
            settings['STATICFILES_FINDERS'].index('django.contrib.staticfiles.finders.AppDirectoriesFinder'),
            'aldryn_boilerplates.staticfile_finders.AppDirectoriesFinder',
        )

        # TODO: move this to ckeditor addon aldyn config when we extract it from the base project
        # boilerplate should provide /static/js/modules/ckeditor.wysiwyg.js and /static/css/base.css
        # CKEDITOR_SETTINGS = {
        #     'height': 300,
        #     'language': '{{ language }}',
        #     'toolbar': 'CMS',
        #     'skin': 'moono',
        #     'extraPlugins': 'cmsplugins',
        #     'toolbar_HTMLField': [
        #         ['Undo', 'Redo'],
        #         ['cmsplugins', '-', 'ShowBlocks'],
        #         ['Format', 'Styles'],
        #         ['TextColor', 'BGColor', '-', 'PasteText', 'PasteFromWord'],
        #         ['Maximize', ''],
        #         '/',
        #         ['Bold', 'Italic', 'Underline', '-', 'Subscript', 'Superscript', '-', 'RemoveFormat'],
        #         ['JustifyLeft', 'JustifyCenter', 'JustifyRight'],
        #         ['HorizontalRule'],
        #         ['Link', 'Unlink'],
        #         ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Table'],
        #         ['Source'],
        #         ['Link', 'Unlink', 'Anchor'],
        #     ],
        # }
        # boilerplate_name = locals().get('ALDRYN_BOILERPLATE_NAME', 'legacy')
        # if boilerplate_name == 'bootstrap3':
        #     CKEDITOR_SETTINGS['stylesSet'] = 'default:/static/js/addons/ckeditor.wysiwyg.js'
        #     CKEDITOR_SETTINGS['contentsCss'] = ['/static/css/base.css']
        # else:
        #     CKEDITOR_SETTINGS['stylesSet'] = 'default:/static/js/modules/ckeditor.wysiwyg.js'
        #     CKEDITOR_SETTINGS['contentsCss'] = ['/static/css/base.css']

        settings['MIGRATION_COMMANDS'].append(
            'python manage.py cms fix-tree --noinput'
        )
        return settings

