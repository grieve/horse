import inspect
import logging
import datetime
import traceback
import importlib


from . import config
from . import slack
from . import servers
from . import database
from .bridles.base import Bridle
from .bridles.base import BridleModel


class Jockey(object):

    def __init__(self):
        logging.info('Jockey initialising.')
        self.socket = servers.SocketServer(self)
        self.http = servers.HTTPServer(self)
        self.slack = slack.API(config.SLACK_API_TOKEN)
        database.configure()
        self.load_bridles()
        logging.info('Jockey ready.')

    def start(self):
        logging.info('Jockey starting.')
        self.socket.start()
        self.http.start()
        self.start_time = datetime.datetime.now()
        logging.info('Jockey started.')
        while True:
            pass

    def load_bridles(self):
        self.bridles = []
        self.bridle_models = []
        for bridle_path in config.BRIDLES:
            logging.info('Loading Bridle: {0}'.format(bridle_path))
            bridle_module = importlib.import_module(bridle_path)
            for cls in bridle_module.__dict__.values():
                if inspect.isclass(cls):
                    if issubclass(cls, Bridle) and cls != Bridle:
                        logging.info('\tCommand: {0} -> {1}'.format(
                            cls.Meta.command_word,
                            cls.__name__
                        ))
                        self.bridles.append(cls(self))
                    elif issubclass(cls, BridleModel) and cls != BridleModel:
                        logging.info('\tModel: {0}'.format(cls.__name__))
                        self.bridle_models.append(cls)

        database.verify_models(self.bridle_models)

    def handle_socket(self, data):
        logging.info('Handling socket event')

    def handle_http_get(self, path, params):
        pass

    def handle_http_post(self, path, data):
        pass

    def handle_command(self, data):
        logging.info('Handling command event')

        if (
            'text' not in data or
            'user_id' not in data or
            'channel_id' not in data
        ):
            logging.error('Malformed command request')
            return 'Malformed command request'

        operands = data['text'].split(' ', 1)
        command_word = operands[0]
        for bridle in self.bridles:
            if bridle.Meta.command_word == command_word:
                try:
                    response = bridle.handle_command(
                        data['user_id'],
                        data['channel_id'],
                        operands[1:]
                    )
                    if not response:
                        response = ""
                    return response
                except:
                    traceback.print_exc()
                    return "Failure: '{0}'".format(data['text'])
        return "Unknown command!"
