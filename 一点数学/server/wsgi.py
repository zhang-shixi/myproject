"""
WSGI config for server project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os


from os.path import join,dirname,abspath#1.
PROJECT_DIR = dirname(dirname(abspath(__file__)))#2.

import sys
sys.path.insert(0,PROJECT_DIR)#3.

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")

application = get_wsgi_application()
