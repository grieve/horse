import re


import horse.models


class Bridle(object):

    class Meta:
        display_name = 'Horse'
        display_icon = 'http://ryangrieve.com/labs/slack_icons/horse.png'
        description = 'No description provided'

    def __init__(self, jockey):
        self.jockey = jockey

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


class CommandBridle(Bridle):

    class Meta(Bridle.Meta):
        command = ''
        help_text = ['No help text provided']
        secret = False

    def execute(self, user, channel, operands):
        return ""


class ListenerBridle(Bridle):

    class Meta(Bridle.Meta):
        regex = ''

    def __init__(self, jockey):
        super(ListenerBridle, self).__init__(jockey)
        self._pattern = re.compile(self.Meta.regex)

    def execute(self, user, channel, context):
        return ""


class WebhookBridle(Bridle):

    class Meta(Bridle.Meta):
        method = 'GET'
        path = ''

    def execute(self, path, data):
        return ""


class EventBridle(Bridle):

    class Meta(Bridle.Meta):
        event = ''

    def execute(self, data):
        return ""


class BridleModel(horse.models.Base):
    pass
