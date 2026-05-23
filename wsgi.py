"""
Vercel WSGI entry point
"""

from app import app

app.json.sort_keys = False

def handler(environ, start_response):
    return app(environ, start_response)