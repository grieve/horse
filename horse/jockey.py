import types
import inspect
import logging
import datetime
import traceback
import importlib


import horse.config
import horse.slack
import horse.servers.http
import horse.servers.socket
import horse.database
import horse.models
import horse.bridles.base

DO_NOT_REGISTER = [
    horse.bridles.base.CommandBridle,
    horse.bridles.base.ListenerBridle,
    horse.bridles.base.WebhookBridle,
    horse.bridles.base.EventBridle,
    horse.bridles.base.BridleModel
]


class Jockey(object):

    def __init__(self):
        logging.info('Jockey initialising.')
        self.socket = horse.servers.socket.SocketServer(self)
        self.http = horse.servers.http.HTTPServer(self)
        self.slack = horse.slack.API(horse.config.SLACK_API_TOKEN)
        horse.database.configure()
        self.load_metadata()
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

    def get_user(self, id):
        query = horse.models.User.selectBy(string_id=id)
        results = list(query)
        if len(results) > 0:
            return results[0]
        else:
            return None

    def get_channel(self, id):
        query = horse.models.Channel.selectBy(string_id=id)
        results = list(query)
        if len(results) > 0:
            return results[0]
        else:
            return None

    def load_metadata(self):
        for user in self.socket.metadata['users']:
            if user['deleted']:
                continue
            if not self.get_user(user['id']):
                horse.models.User(
                    string_id=user['id'],
                    username=user['name'],
                    real_name=user['profile']['real_name_normalized'],
                    image=user['profile']['image_72']
                )
        for channel in self.socket.metadata['channels']:
            if channel['is_archived']:
                continue
            if not self.get_channel(channel['id']):
                horse.models.Channel(
                    string_id=channel['id'],
                    name=channel['name']
                )

    def load_bridles(self):
        self.bridles = {
            "event": [],
            "command": [],
            "listener": [],
            "webhook": {
                "GET": [],
                "POST": []
            }
        }
        self.bridle_models = []

        logging.info("")
        logging.info('<<<< START Loading Bridles >>>>')
        for bridle_path in horse.config.BRIDLES:
            logging.info("")
            logging.info('Loading Bridle: {0}'.format(bridle_path))
            if isinstance(bridle_path, basestring):
                bridle_module = importlib.import_module(
                    bridle_path.replace('horse.ext.', 'horse_')
                )
            elif isinstance(bridle_path, types.ModuleType):
                bridle_module = bridle_path
            else:
                logging.warning("\tFailed: {0}".format(bridle_path))
                continue

            for cls in bridle_module.__dict__.values():
                if inspect.isclass(cls):

                    if cls in DO_NOT_REGISTER:
                        continue

                    if issubclass(cls, horse.bridles.base.CommandBridle):
                        logging.info('\tCommand: {0} -> {1}'.format(
                            cls.Meta.command,
                            cls.__name__
                        ))
                        self.bridles['command'].append(cls(self))

                    elif issubclass(cls, horse.bridles.base.ListenerBridle):
                        logging.info('\tListener: {0} -> {1}'.format(
                            cls.Meta.regex,
                            cls.__name__
                        ))
                        self.bridles['listener'].append(cls(self))

                    elif issubclass(cls, horse.bridles.base.WebhookBridle):
                        logging.info('\tWebhook: {0}:{1} -> {2}'.format(
                            cls.Meta.method,
                            cls.Meta.path,
                            cls.__name__
                        ))
                        self.bridles['webhook'][cls.Meta.method].append(
                            cls(self)
                        )

                    elif issubclass(cls, horse.bridles.base.EventBridle):
                        logging.info('\tEvent: {0} -> {1}'.format(
                            cls.Meta.event,
                            cls.__name__
                        ))
                        self.bridles['event'].append(cls(self))

                    elif issubclass(cls, horse.bridles.base.BridleModel):
                        logging.info('\tModel: {0}'.format(cls.__name__))
                        self.bridle_models.append(cls)

        logging.info("")
        horse.database.verify_models(self.bridle_models)
        logging.info('<<<< END Loading Bridles >>>>')
        logging.info("")

    def handle_socket(self, data):
        logging.info('Handling socket event: Type={0}'.format(data['type']))

        if 'user' in data:
            if isinstance(data['user'], basestring):
                user = self.get_user(data['user'])
            elif isinstance(data['user'], dict):
                user = self.get_user(data['user']['id'])
                if user is None:
                    user = data['user']
                    user = horse.models.User(
                        string_id=user['id'],
                        username=user['name'],
                        real_name=user['profile']['real_name_normalized'],
                        image=user['profile']['image_72']
                    )
            if user is not None:
                data['user'] = user

        if 'channel' in data:
            channel = self.get_channel(data['channel'])
            if channel is not None:
                data['channel'] = channel

        if data['type'] == 'message' and 'subtype' not in data:
            self.handle_message(data)

        else:
            for bridle in self.bridles['event']:
                if data['type'] == bridle.Meta.event:
                    bridle.execute(data)

    def handle_message(self, data):
        logging.debug(data)
        for bridle in self.bridles['listener']:
            match = bridle._pattern.search(data['text'])
            if match:
                bridle.execute(
                    data['user'],
                    data['channel'],
                    match,
                    data['text']
                )

    def handle_http_get(self, path, params):
        logging.info('Handling GET webhook: {0}'.format(path))
        for bridle in self.bridles['webhook']['GET']:
            if bridle.Meta.path == path:
                return bridle.execute(path, params)

        return ""

    def handle_http_post(self, path, data):
        logging.info('Handling POST webhook: {0}'.format(path))
        for bridle in self.bridles['webhook']['POST']:
            if bridle.Meta.path == path:
                return bridle.execute(path, data)

        return ""

    def handle_command(self, data):
        logging.info('Handling command event')

        if (
            'text' not in data or
            'user_id' not in data or
            'channel_id' not in data
        ):
            logging.error('Malformed command request')
            return 'Malformed command request'

        if 'user_id' in data:
            user = self.get_user(data['user_id'])

        if 'channel_id' in data:
            channel = self.get_channel(data['channel_id'])

        operands = data['text'].split(' ')
        command = operands[0]
        for bridle in self.bridles['command']:

            if bridle.Meta.command == command:
                try:
                    return bridle.execute(
                        user,
                        channel,
                        operands[1:]
                    )
                except:
                    traceback.print_exc()
                    return "Failure: '{0}'".format(data['text'])

        return "Unknown command!"
