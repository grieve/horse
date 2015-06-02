import json
import thread
import logging

from flask import Flask
from flask import request


class HTTPServer(object):

    FORM_DATA_MIME = 'application/x-www-form-urlencoded'
    JSON_DATA_MIME = 'application/json'

    def __init__(self, jockey):
        self.jockey = jockey
        self.app = Flask('horse-http-server')
        self.app.add_url_rule(
            '/',
            'handler',
            self.handle_request,
            methods=['GET', 'POST'],
            defaults={'path': ''}
        )
        self.app.add_url_rule(
            '/<path:path>',
            'handler',
            self.handle_request,
            methods=['GET', 'POST']
        )

    def handle_request(self, path):
        logging.info('Inbound request: {0}'.format(path))
        if path == 'command':
            response = self.jockey.handle_command(request.form)
        else:
            if request.method == 'GET':
                response = self.jockey.handle_http_get(path, request.args)
            elif request.method == 'POST':
                if request.headers['Content-Type'] == self.FORM_DATA_MIME:
                    response = self.jockey.handle_http_post(path, request.form)
                elif request.headers['Content-Type'] == self.JSON_DATA_MIME:
                    data = json.loads(request.body)
                    response = self.jockey.handle_http_post(path, data)
        logging.info('Outbound response: {0}'.format(response))
        if response is None:
            response = ""
        return str(response)

    def start(self):
        def run(*args):
            self.app.run(host="0.0.0.0", port=5000)

        logging.info('Starting HTTP server on new thread.')
        thread.start_new_thread(run, ())
