import json
import thread
import logging

import requests
import websocket

import horse.config


class SocketServer(websocket.WebSocketApp):

    def __init__(self, jockey):
        response = requests.get('https://slack.com/api/rtm.start', params={
            "token": horse.config.SLACK_API_TOKEN
        })
        self.metadata = response.json()
        self.url = self.metadata['url']
        self.keep_running = True
        self.last_ping_tm = 0
        self.header = []
        self.cookie = None
        self.subprotocols = None
        self.sock = None
        self.get_mask_key = None
        self.jockey = jockey

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
        data = json.loads(message)
        self.jockey.handle_socket(data)

    def on_ping(self, socket, ping):
        logging.info('Socket PING')

    def on_pong(self, socket, pong):
        logging.info('Socket PONG')

    def on_cont_message(self, socket):
        logging.info('Socket CONT')

    def on_error(self, socket, error):
        logging.error('Socket ERROR: {0}'.format(error))
