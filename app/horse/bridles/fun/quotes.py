import random

import requests

from ... import config
from ...models import Channel
from ..base import CommandBridle


class Quote(CommandBridle):

    class Meta(CommandBridle.Meta):
        command = 'quote'
        description = "Fetches a random quote shared in #quotes"
        help_text = ["Usage: `/horse quote`"]
        display_name = "+rehabstudio Quotes"

    def __init__(self, jockey):
        super(Quote, self).__init__(jockey)
        self.quotes_channel = Channel.selectBy(name='quotes').getOne(None)

    def get_random_quote(self):
        quotes = self.get_all_quotes()
        if quotes:
            quotes = self.filter_quotes(quotes)
            print quotes
            return random.choice(quotes)
        else:
            return None

    def get_all_quotes(self):
        url = "https://slack.com/api/files.list"
        params = {
            "token": config.SLACK_API_TOKEN,
            "types": "images",
            "count": 1000
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            quotes = response.json()
            return quotes['files']
        else:
            return None

    def filter_quotes(self, quotes):
        filtered = []
        for quote in quotes:
            if self.quotes_channel.string_id in quote['channels']:
                filtered.append(quote)
        return filtered

    def execute(self, user, channel, operands):
        if len(operands) == 0:
            quote = self.get_random_quote()
            response = quote['url']
            self.message(channel, response)
        elif operands[0] == 'all':
            quotes = self.get_all_quotes()
            quotes = self.filter_quotes(quotes)
            response = "\n".join([q['url'] for q in quotes])
            self.message(user, response)
