"""
WSGI config for quizitsite project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""
import os
import sys

sys.path.append('/home/bitnami/apps/django/django_projects/QuizIt/quizitsite')

os.environ.setdefault("PYTHON_EGG_CACHE", "/home/bitnami/apps/django/django_projects/QuizIt/quizitsite/egg_cache")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "quizitsite.settings")

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()

