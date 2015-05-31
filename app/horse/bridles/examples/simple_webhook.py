from ..base import WebhookBridle


# Inherit from WebhookBridle if you want your code executed when a specific
# URL on the horse instance is requested. This is useful for tying in
# functionality from other services, like JIRA, Git or CI.
class SimpleWebhookBridle(WebhookBridle):

    # Inherit from parents Meta and provide path, and optionaly method. Method
    # can be 'GET' or 'POST', and defaults to 'GET' if it's missing.
    class Meta(WebhookBridle.Meta):
        path = 'testing'
        method = 'GET'

    # The execute function is called whenever the specified path is requested
    # via the specified method. It is passed the path and the parameters it
    # was requested with. Both form encoded and JSON parameters are supported
    # and automatically decoded.
    def execute(self, path, params):
        self.message('#horsebox', "webhooks!")
