#!/usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import os
import threading
from parlai.core.params import ParlaiParser
from parlai.scripts.interactive_web import WEB_HTML, STYLE_SHEET, FONT_AWESOME
from http.server import BaseHTTPRequestHandler, HTTPServer


class BrowserHandler(BaseHTTPRequestHandler):
    """
    Handle HTTP requests.
    """

    def do_HEAD(self):
        """
        Handle HEAD requests.
        """
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        """
        Respond to GET request, especially the initial load.
        """
        paths = {
            '/': {'status': 200},
            '/favicon.ico': {'status': 202},  # Need for chrome
        }
        if self.path in paths:
            self._respond(paths[self.path])
        else:
            self._respond({'status': 500})

    def _handle_http(self, status_code, path, text=None):
        self.send_response(status_code)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        server_endpoint = 'wss://master-blenderbot2-server-scy6500.endpoint.ainize.ai'
        #if os.environ['SERVER_ENDPOINT']:
         #   server_endpoint = os.environ['SERVER_ENDPOINT']:
        content = WEB_HTML.format(STYLE_SHEET, FONT_AWESOME, server_endpoint)
        return bytes(content, 'UTF-8')

    def _respond(self, opts):
        response = self._handle_http(opts['status'], self.path)
        self.wfile.write(response)


def _run_browser():
    httpd = HTTPServer(('0.0.0.0', 8080), BrowserHandler)
    httpd.serve_forever()


if __name__ == "__main__":
    threading.Thread(target=_run_browser).start()
