import datetime

import sqlobject

from ..base import Bridle
from ..base import BridleModel


class Uptime(Bridle):

    class Meta(Bridle.Meta):
        command_word = 'uptime'

    def handle_command(self, user, channel, operands):
        response = '> Uptime {0}'.format(
            datetime.datetime.now() - self.jockey.start_time
        )
        self.message(channel, response)


class TestModel(BridleModel):
    name = sqlobject.StringCol()
