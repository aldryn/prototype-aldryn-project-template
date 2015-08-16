# aldryn project template

Welcome to the first prototype of the new aldryn project template.

**Use https://github.com/aldryn/prototype-aldryn-project-template to setup locally.**

Your feedback is very valuable! Please help.

This prototype is intended to get feedback in order to flesh out a good api
and very understandable project structure. Add github issues on this repo for
questions, ideas, bugs. Please also look at existing issues of other people and
join the discussion.

So... what am I looking at?

This repo represents a user-accessible git repo of a website on aldryn. It's
goal is to have as little non-project specific code as possible. All the heavy
lifting is outsourced into Addons.

```
addons   # all Addons installed on this website
    my-installed-addon
        addon.json
        aldryn_config.py
        settings.json
addons-dev  # in .gitignore
    my-addon-that-i-am-activly-developing-locally   
        .git
        addon.json
        aldryn_config.py
        settings.json
        setup.py
        my_addon
            __init__.py
            models.py
            ...
private
    sass
        ...
static
    js
    css
    img
templates
    base.html
.git
.gitignore
Dockerfile
manage.py
Procfile
README.md
requirements.in
requirements.txt
settings.py
urls.py
wsgi.py
```

For this prototype the ``addons-dev`` folder actually contains some sourcecode
within the git repo. In real usage the code for each Addon would be in a git repo of its own
and manually cloned into the ``addons-dev`` folder.

## ``addons`` and ``addons-dev``

There is a folder here for every Addon that is installed in the project and 
contains these 3 files:

* ``aldryn_addon.py``: holds the configuration logic and the form to edit exposed settings (just a copy of the one from the Addon package)
* ``addon.json``: holds some metadata about the Addon (just a copy of the one from the Addon package)
* ``settings.json`` the (non secret) values for the form fields defined in ``aldryn_addon.py``

These files (and ``requirements.in``) will be updated/commited by the
controlpanel whenever an Addon is added or upgraded over the UI.

If you're developing an Addon locally, you'd just clone the Addon git repo
into ``addons-dev`` and ``pip install -e`` it.
``aldryn_addon.py`` and ``addon.json`` are already at the right location.
Remember to ``.gitignore`` ``settings.json`` in the Addon repo.

Even *Django* itself is an Addon. It constructs all the common settings like
``DATABASES``, ``CACHES`` and many more. It also provides the manage.py script
and a standardised command to start the webserver, encapsulating all the 
nitty-gritty details. What is also planned, is that Addons will be able to
register scripts for the ``migrate`` step (mainly used for database
migrations and fix-mptt by django-cms).
So upgrading the common ``aldryn-django`` package can also
upgrades the way django is started and how migrations are run (Django 1.6 to
Django 1.7 migrations upgrade anyone? ;-) ).
 
Similarly *django CMS* is an Addon. It adds all the django-cms settings. In 
the future it will be able to register migrate steps as well
(e.g delete orphaned plugins).
In the first iteration the django-cms Addon will be fat with a lot of other
dependencies built in (django-filer, aldryn-boilerplates, ...). Later, when
we have Addon dependency support, we'll split it into smaller Addons.


## settings.py

Here you can add any project specific settings. The special thing about it, is
that we mostly get the settings from the installed Addons:

```
import aldryn_addons.settings
aldryn_addons.settings.load(locals())
```

But you can do whatever you want in here. Including shooting yourself in the
foot. The controlpanel will auto update ``INSTALLED_ADDONS`` based on what
is done in the UI.

## private

contains all the project specific static resources that are private. Mostly
used for the sass sources.l

## static

nothing special to say here.

## templates

nothing special to say here

## Dockerfile

All the heavy lifting is done in the parent docker image. But you can do
do anything you want here... install apt-packages or other binary
dependencies.
Or if you want to go all-in and fully customised: use an entirely different
base image.
