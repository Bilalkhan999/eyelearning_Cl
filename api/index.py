"""
Vercel ASGI serverless function entry point for Django.
"""
import os
import sys

# Add the project directory to the sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set the settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myeyelevel_django.settings')

# Import Django ASGI application
from django.core.asgi import get_asgi_application

# Get the ASGI application - Vercel expects 'app' or 'handler' variable
app = get_asgi_application()
handler = app
