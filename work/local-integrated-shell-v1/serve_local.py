"""Read-only, loopback preview with a Pages-subdirectory alias and exact-case paths."""
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[2]

class PreviewServer(ThreadingHTTPServer):
    request_queue_size = 128

class PreviewHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def do_GET(self):
        self._read_request(False)

    def do_HEAD(self):
        self._read_request(True)

    def _read_request(self, head):
        path = unquote(urlsplit(self.path).path)
        prefix = '/the-haunted-realm'
        if path == prefix:
            self.send_response(302)
            self.send_header('Location', prefix + '/')
            self.end_headers()
            return
        if path.startswith(prefix + '/'):
            path = path[len(prefix):]
        current = ROOT
        for part in path.strip('/').split('/'):
            if not part:
                continue
            if part in ('.', '..') or '\\' in part or not current.is_dir():
                self.send_error(404)
                return
            if part not in {child.name for child in current.iterdir()}:
                self.send_error(404, 'Missing or incorrectly cased path')
                return
            current = current / part
        self.path = path
        if head:
            super().do_HEAD()
        else:
            super().do_GET()

    def log_message(self, format, *args):
        if args and str(args[1]) not in ('200', '304'):
            super().log_message(format, *args)

if __name__ == '__main__':
    server = PreviewServer(('127.0.0.1', 4173), PreviewHandler)
    print('Local preview: http://127.0.0.1:4173/ - read-only; no deployment', flush=True)
    server.serve_forever()
