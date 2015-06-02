import datetime

from horse.bridles.base import CommandBridle


class Uptime(CommandBridle):

    class Meta(CommandBridle.Meta):
        command = 'uptime'

    def execute(self, user, channel, operands):
        response = '> Uptime {0}'.format(
            datetime.datetime.now() - self.jockey.start_time
        )
        self.message(channel, response)
