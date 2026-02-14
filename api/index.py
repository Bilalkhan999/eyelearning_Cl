"""
Vercel serverless function entry point for Django using Mangum.
"""
import os
import sys

# Add the project directory to the sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set the settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myeyelevel_django.settings')

# Import Django ASGI application
from django.core.asgi import get_asgi_application
from mangum import Mangum

# Get the ASGI application
django_app = get_asgi_application()

# Wrap with Mangum for Lambda/Vercel compatibility
handler = Mangum(django_app, lifespan="off")
