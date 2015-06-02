import random

from horse import config
from horse.bridles.base import CommandBridle


class Hangouts(CommandBridle):

    class Meta(CommandBridle.Meta):
        command = 'hangout'
        display_name = "Google+ Hangouts"
        display_icon = "http://ryangrieve.com/labs/slack_icons/hangouts.png"
        description = "Create hangouts and share the URL"
        help_text = [
            "Usage:",
            "\t`/horse hangout` to create a hangout with this channels name",
            "\t`/horse hangout new` to create a hangout with a random name"
        ]

    names = [
        'alpha', 'bravo', 'charlie', 'delta', 'echo', 'foxtrot', 'golf',
        'hotel', 'india', 'juliet', 'kilo', 'lima', 'mike', 'november',
        'oscar', 'papa', 'quebec', 'romeo', 'sierra', 'tango', 'uniform',
        'victor', 'whiskey', 'xray', 'yankee', 'zulu'
    ]

    base_url = "https://plus.google.com/hangouts/_/{0}/".format(
        config.GOOGLE_APPS_DOMAIN
    )

    def execute(self, user, channel, operands):
        if len(operands) > 0 and operands[0] == 'new':
            url = self.base_url + "{0}-{1}-{2}".format(
                random.choice(self.names),
                random.choice(self.names),
                random.choice(self.names)
            )
        else:
            url = self.base_url + "slack-" + channel.name
        self.message(channel, "Hangout: %s" % url)
