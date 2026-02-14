"""
Vercel serverless function entry point for Django using HTTP handler.
"""
import os
import sys
from http.server import BaseHTTPRequestHandler
from io import BytesIO

# Add the project directory to the sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set the settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myeyelevel_django.settings')

# Import Django WSGI application
from django.core.wsgi import get_wsgi_application

# Get the WSGI application
application = get_wsgi_application()


class handler(BaseHTTPRequestHandler):
    """
    Vercel-compatible HTTP handler for Django.
    """
    
    def do_GET(self):
        self.handle_request()
    
    def do_POST(self):
        self.handle_request()
    
    def do_PUT(self):
        self.handle_request()
    
    def do_DELETE(self):
        self.handle_request()
    
    def do_OPTIONS(self):
        self.handle_request()
    
    def handle_request(self):
        """Handle any HTTP request and forward to Django WSGI app."""
        # Read body
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length) if content_length > 0 else b''
        
        # Build environ
        environ = {
            'REQUEST_METHOD': self.command,
            'SCRIPT_NAME': '',
            'PATH_INFO': self.path.split('?')[0],
            'QUERY_STRING': self.path.split('?')[1] if '?' in self.path else '',
            'SERVER_NAME': self.headers.get('Host', 'localhost').split(':')[0],
            'SERVER_PORT': '443',
            'HTTP_HOST': self.headers.get('Host', 'localhost'),
            'HTTP_USER_AGENT': self.headers.get('User-Agent', ''),
            'HTTP_ACCEPT': self.headers.get('Accept', '*/*'),
            'HTTP_ACCEPT_ENCODING': self.headers.get('Accept-Encoding', ''),
            'HTTP_ACCEPT_LANGUAGE': self.headers.get('Accept-Language', ''),
            'CONTENT_TYPE': self.headers.get('Content-Type', ''),
            'CONTENT_LENGTH': str(len(body)),
            'wsgi.version': (1, 0),
            'wsgi.url_scheme': 'https',
            'wsgi.input': BytesIO(body),
            'wsgi.errors': sys.stderr,
            'wsgi.multithread': False,
            'wsgi.multiprocess': False,
            'wsgi.run_once': False,
        }
        
        # Add all headers
        for header_name in self.headers.keys():
            header_value = self.headers.get(header_name)
            if header_value:
                wsgi_name = 'HTTP_' + header_name.upper().replace('-', '_')
                if wsgi_name not in environ:
                    environ[wsgi_name] = header_value
        
        # Response collector
        response_started = [False]
        response_status = [None]
        response_headers = [None]
        response_body = []
        
        def start_response(status, headers):
            response_started[0] = True
            response_status[0] = status
            response_headers[0] = headers
            return lambda x: response_body.append(x)
        
        # Call WSGI app
        result = application(environ, start_response)
        
        for chunk in result:
            if chunk:
                response_body.append(chunk)
        
        # Send response
        status_code = int(response_status[0].split()[0])
        self.send_response(status_code)
        
        for header_name, header_value in response_headers[0]:
            self.send_header(header_name, header_value)
        self.end_headers()
        
        self.wfile.write(b''.join(response_body))
