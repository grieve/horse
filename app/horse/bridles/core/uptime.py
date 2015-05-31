import datetime

from ..base import Bridle


class Uptime(Bridle):

    class Meta(Bridle.Meta):
        command_word = 'uptime'

    def handle_command(self, user, channel, operands):
        response = '> Uptime {0}'.format(
            datetime.datetime.now() - self.jockey.start_time
        )
        self.message(channel, response)
