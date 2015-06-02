import sqlobject

from ..base import CommandBridle
from ..base import BridleModel


# Any classes that inherit from BridleModel will automatically handled by
# jockey and equivalent tables made in the managed database. These classes
# are derived from sqlobject.SQLObject.
class SimpleCounter(BridleModel):
    user = sqlobject.StringCol()
    channel = sqlobject.StringCol()


class PersistCommand(CommandBridle):

    class Meta(CommandBridle.Meta):
        command = 'persist'

    def execute(self, user, channel, operands):
        # create an instance of the class to save a record to the database
        SimpleCounter(user=user, channel=channel)

        # query the database for num records, see sqlobject docs for usage
        num_records = SimpleCounter.select().count()
        self.message(channel, "This has been called {0} time(s)".format(
            num_records
        ))
