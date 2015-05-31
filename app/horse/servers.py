import cgi
import json
import thread
import logging
import urlparse
import BaseHTTPServer

import requests
import websocket

from . import config


class Socket(websocket.WebSocketApp):

    def __init__(self, func):
        response = requests.get('https://slack.com/api/rtm.start', params={
            "token": config.SLACK_API_TOKEN
        })
        data = response.json()
        self.url = data['url']
        self.keep_running = True
        self.last_ping_tm = 0
        self.header = []
        self.cookie = None
        self.subprotocols = None
        self.sock = None
        self.get_mask_key = None
        self.func = func

    def start(self):
        def run(*args):
            self.run_forever()

        logging.info('Starting socket client on new thread.')
        thread.start_new_thread(run, ())

    def on_open(self, socket):
        logging.info('Socket client open')

    def on_close(self, socket):
        logging.info('Socket client closed. Reopening.')
        self.start()

    def on_message(self, socket, message):
        self.func(message)

    def on_ping(self, socket, ping):
        logging.info('Socket PING')

    def on_pong(self, socket, pong):
        logging.info('Socket PONG')

    def on_cont_message(self, socket):
        logging.info('Socket CONT')

    def on_error(self, socket, error):
        logging.error('Socket ERROR: {0}'.format(error))


class HTTP(object):

    def __init__(self, func):
        self.server = BaseHTTPServer.HTTPServer(("", 5000), HTTP.Handler)
        self.server.func = func

    class Handler(BaseHTTPServer.BaseHTTPRequestHandler):

        def do_GET(self):
            self.log_request(200)
            self.send_response(200, "OK")
            path, params = self.parse_GET()
            self.server.func(path, params)

        def do_POST(self):
            self.log_request(200)
            self.send_response(200, "OK")
            path, params = self.parse_GET()
            params.update(self.parse_POST())
            self.server.func(path, params)

        def parse_GET(self):
            parsed = urlparse.urlparse(self.path)
            params = urlparse.parse_qs(parsed.query)
            return parsed.path, params

        def parse_POST(self):
            content, parts = cgi.parse_header(self.headers['content-type'])
            if content == 'multipart/form-data':
                params = cgi.parse_multipart(self.rfile, parts)
            else:
                length = int(self.headers['content-length'])
                data = self.rfile.read(length)
                if content == 'application/json':
                    params = json.loads(data)
                else:
                    params = urlparse.parse_qs(data, keep_blank_values=1)
            return params

    def start(self):
        def run(*args):
            self.server.serve_forever()

        logging.info('Starting HTTP server on new thread.')
        thread.start_new_thread(run, ())
