import os
from aldryn_django import startup

startup.wsgi(path=os.path.dirname(__file__))
