import random

import requests
import sqlobject

from ..base import CommandBridle
from ..base import BridleModel


class SexyPaddyURL(BridleModel):
    url = sqlobject.StringCol()
    added_by = sqlobject.ForeignKey('User')
    invoked = sqlobject.IntCol(default=0)


class SexyPaddy(CommandBridle):

    class Meta(CommandBridle.Meta):
        command = 'sexypaddy'
        display_name = "Sexy Paddy"
        display_icon = (
            "https://secure.gravatar.com/avatar/"
            "6f836d78a34bd1e63b51e9a700188e5c.jpg"
        )
        description = 'So you want some sexy paddy, huh?'
        help_text = [
            'Usage:',
            '\t`/horse sexypaddy` - get a random paddy',
            '\t`/horse sexypaddy list` - get a list of paddies'
            '\t`/horse sexypaddy add <url>` - add a new paddy'
        ]

    def execute(self, user, channel, operands):
        print operands
        if len(operands) == 0:
            return self.random_paddy(user, channel)
        elif operands[0] == 'add':
            url = operands[1]
            response = requests.get(url)
            if response.status_code != 200:
                return "Can't seem to access URL. Not added.".format(url)
            else:
                return self.add_paddy(user, url)
        elif operands[0] == 'remove':
            url = operands[1]
            return self.remove_paddy(url)
        elif operands[0] == 'list':
            return self.list_paddies()

    def random_paddy(self, user, channel):
        paddies = list(SexyPaddyURL.select())
        if len(paddies) == 0:
            return "No paddies found, try using `/horse sexypaddy add <url>`."
        selected = random.choice(paddies)
        selected.set(invoked=selected.invoked + 1)
        self.message(channel, selected.url)

    def add_paddy(self, user, url):
        exists = SexyPaddyURL.selectBy(url=url).getOne(None)
        if exists is None:
            SexyPaddyURL(url=url, added_by=user)
            return "Added to sexypaddy".format(url)
        else:
            return "URL was already added by {0}".format(
                exists.added_by.username
            )

    def remove_paddy(self, url):
        exists = SexyPaddyURL.selectBy(url=url).getOne(None)
        if exists is None:
            return "Can't find this URL."
        else:
            exists.destroySelf()
            return "URL deleted."

    def list_paddies(self):
        paddies = SexyPaddyURL.select()
        return "\n".join([
            "{0} - {1}".format(p.added_by.username, p.url)
            for p in paddies
        ])
