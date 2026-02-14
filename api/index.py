"""Vercel serverless entrypoint for Django.

Vercel's Python runtime supports WSGI apps by exporting an `app` callable.
"""

import os
import sys

# Add the project directory to the sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set the settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myeyelevel_django.settings')

from django.core.wsgi import get_wsgi_application

app = get_wsgi_application()
