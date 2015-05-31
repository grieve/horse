from ..base import CommandBridle


# Inherit from CommandBridle class to implement a slash command bridle
# this command is executed using `/horse simple_test`
class SimpleCommand(CommandBridle):

    # Inherit from the parents Meta and add command word
    class Meta(CommandBridle.Meta):
        command = 'simple_test'

    # The execute function is called by the jockey when the command word
    # is used. The user and channel are passed to the function along with
    # any additional operands that were provided to the command.

    # For example, if this command was invoked like:
    #     `/horse simple_test 123 apples peach`
    # then operands would be:
    #     ["123", "apples", "peach"].

    # All operands are strings.
    def execute(self, user, channel, operands):
        # You can pass either the user or channel id to the `message` method
        # to reply publicly or in a PM
        self.message(channel, "Message visible in channel")
        self.message(user, "Message is PM'd to user")

        # Any string value returned by the method will be shown as a "gray"
        # message in the channel, and only visible to the user who invoked
        # the command.
        return 'Message in channel, but only visible to user'
