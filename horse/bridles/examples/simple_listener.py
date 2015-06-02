from ..base import ListenerBridle


# Inherit from ListenerBridle to listen for specific text patterns in user
# messages. This will only work for public channels, or groups that Horse (or
# rather, the api key owner) is a member of.
class SimpleListenerBridle(ListenerBridle):

    # Inherit from parents Meta and add regex pattern to match
    class Meta(ListenerBridle.Meta):
        regex = 'test(ing)?'

    # The execute function is called when a message matches the provided regex
    # pattern. It is passed the user, the channel, the re.MatchObject of the
    # match, and the context (the full text of the message).
    def execute(self, user, channel, match, context):
        self.message(channel, "You said: {0}".format(match.group()))
