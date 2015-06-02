import logging

import requests


class API(object):

    api_root = 'https://slack.com/api/{0}'

    def __init__(self, api_token):
        logging.info('Slack API client started with {0}'.format(api_token))
        self._token = api_token

    def _make_request(self, endpoint, **params):
        params['token'] = self._token
        response = requests.post(self.api_root.format(endpoint), data=params)
        logging.info(
            'Request: {0} - {1}'.format(endpoint, response.status_code)
        )
        if response.status_code != 200:
            logging.error(response.content)
        return response

    def send_message(self, **kwargs):
        return self._make_request('chat.postMessage', **kwargs)
