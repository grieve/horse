from ..base import EventBridle


# Inherit from EventBridle class to have your code executed when slack sends
# a specific event type via the realtime api. Event types are listed here:
#     https://api.slack.com/rtm

# To deal with 'message' type events, use the ListenerBridle instead.
class SimpleEventBridle(EventBridle):

    # Inherit from the parents Meta and add the event type you wish to act on
    class Meta(EventBridle.Meta):
        event = 'hello'

    # The execute function is called when the specific event type arrives.
    # The entirety of the event message is passed as a parameters to this
    # function. For more details on the data contents, see the Slack docs
    # linked above.
    def execute(self, data):
        self.message('#horsebox', "Horse is connected via web sockets!")
