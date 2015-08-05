# -*- coding: utf-8 -*-
from aldryn_client import forms


class Form(forms.BaseForm):
    name = forms.CheckboxField('Name', required=False)

    def to_settings(self, data, settings):
        # TODO: break out a lot of this stuff into other Addons
        # aldryn-sites
        settings['INSTALLED_APPS'].append('aldryn_sites')

        # aldryn-boilerplates
        settings['INSTALLED_APPS'].append('aldryn_boilerplates')
        settings['TEMPLATE_LOADERS'].insert(
            settings['TEMPLATE_LOADERS'].index('django.template.loaders.app_directories.Loader'),
            'aldryn_boilerplates.template_loaders.AppDirectoriesLoader'
        )
        settings['ALDRYN_BOILERPLATE_NAME'] = settings.get('ALDRYN_BOILERPLATE_NAME', 'legacy')
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
        return settings
