"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
import sys
from django.core.wsgi import get_wsgi_application
from django.contrib.staticfiles.handlers import StaticFilesHandler

# Añadir el path al proyecto (asegúrate que 'Kinef' es el nombre correcto)
path = os.path.expanduser('~/Kinef')
if path not in sys.path:
    sys.path.insert(0, path)

# Ajusta 'project.settings' según el nombre de tu carpeta del proyecto
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'



application = StaticFilesHandler(get_wsgi_application())
