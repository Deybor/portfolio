"""Serve the exact Pages artifact under its public /portfolio/ prefix for QA."""
from pathlib import Path
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
ROOT = Path(__file__).resolve().parents[1] / 'dist-pages'
class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs): super().__init__(*args, directory=str(ROOT), **kwargs)
    def translate_path(self, path):
        if path.startswith('/portfolio'): path = path[len('/portfolio'):] or '/'
        return super().translate_path(path)
    def log_message(self, *args): pass
ThreadingHTTPServer(('127.0.0.1', 8082), Handler).serve_forever()
