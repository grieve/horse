from ..base import Bridle


class Inventory(Bridle):

    class Meta(Bridle.Meta):
        command_word = 'inventory'
        display_name = 'Horse Help'
        display_icon = 'http://ryangrieve.com/labs/slack_icons/help.png'
        description = "Lists all bridles currently available."
        help_text = ["Usage: `/horse inventory`"]

    def handle_command(self, user, channel, operands):
        bridles = ", ".join(
            '_%s_' % x.Meta.command_word
            for x in self.jockey.bridles
            if not x.Meta.secret
            and x.Meta.command_word != ""
            and not x.Meta.command_word.startswith('_')
        )
        self.message(
            channel,
            "Horse has loaded the following bridles: %s" % bridles
        )


class Help(Bridle):

    class Meta(Bridle.Meta):
        command_word = 'help'
        display_name = 'Horse Help'
        display_icon = 'http://ryangrieve.com/labs/slack_icons/help.png'
        description = "Prints help and usage information on available bridles"
        help_text = ["Usage: `/horse help [bridle-name]`"]

    def handle_command(self, user, channel, operands):
        if len(operands) > 0:
            bridle_name = operands[0]
            bridle = None
            for m in self.jockey.bridles:
                if m.__class__.__name__ == bridle_name:
                    bridle = m
                elif m.Meta.command_word == bridle_name:
                    bridle = m
            if bridle:
                msg = "%s - %s" % (
                    bridle.__class__.__name__,
                    bridle.Meta.description
                )
                for line in bridle.Meta.help_text:
                    msg += "\n\t- %s" % line
                self.message(channel, msg)
            else:
                self.message(channel, "Bridle '%s' not found" % bridle_name)
        else:
            self.message(channel, self.Meta.help_text)
            self.message(
                channel,
                "(Hint - Try typing `/horse inventory` for a list of bridles)"
            )
