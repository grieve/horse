from .. import models


class Bridle(object):

    class Meta:
        command_word = ''
        display_name = 'Horse'
        display_icon = 'http://ryangrieve.com/labs/slack_icons/horse.png'
        description = 'No description provided'
        help_text = ['No help text provided']
        secret = False

    def __init__(self, jockey):
        self.jockey = jockey

    def handle_command(self, user, channel, operands):
        return None

    def message(self, channel, message, **kwargs):
        if 'username' not in kwargs:
            kwargs['username'] = self.Meta.display_name
        if 'icon_url' not in kwargs:
            kwargs['icon_url'] = self.Meta.display_icon

        self.jockey.slack.send_message(
            channel=channel,
            text=message,
            **kwargs
        )


class BridleModel(models.Base):
    pass
