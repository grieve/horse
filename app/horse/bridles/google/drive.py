import httplib2

from apiclient.discovery import build

from horse import config
from horse.bridles.base import CommandBridle

from .auth import GoogleAuthMixin


class GoogleDrive(CommandBridle, GoogleAuthMixin):

    class Meta(CommandBridle.Meta):

        command = "drive"
        description = (
            "Use Google Drive API to search shared documents. "
            "Requires Google Auth."
        )
        help_text = [
            "Usage:",
            "\t`/horse drive search <terms>`",
            "\t_Please ensure you authenticate with Google using "
            "`/horse gauth` before using this._"
        ]

        display_name = "Google Drive"
        display_icon = (
            "http://home.lps.org/training/files/2009"
            "/10/product256.png"
        )

    default_query = "title contains '{0}' or fullText contains '{0}'"

    def execute(self, user, channel, operands):
        if len(operands) == 0:
            return "Hmm, try `/horse help drive`"

        if operands[0] == 'search':
            return self.search_drive(user, channel, operands)

    def search_drive(self, user, channel, operands):
        credentials = self.get_credentials(user)
        if not credentials:
            return "You are not yet authorized. Please check PMs"

        self.message(
            channel,
            "Searching for *{0}*...".format(" ".join(operands[1:]))
        )

        http = httplib2.Http()
        http = credentials.authorize(http)

        service = build(
            serviceName='drive',
            version='v2',
            http=http,
            developerKey=config.GAPI_CLIENT_ID
        )

        query = ''
        for term in operands[1:]:
            if not query:
                query = self.default_query.format(term)
            else:
                query += " or " + self.default_query.format(term)
        try:
            results = service.files().list(q=query, maxResults=10).execute()
        except Exception, e:
            return e
            self.message(channel, "Something went wrong")
        else:
            output = ""
            for item in results['items']:
                output += '\n<{0}|{1}> _created by {3} on {2}_'.format(
                    item['alternateLink'],
                    item['title'],
                    item['createdDate'][:10],
                    ", ".join(item['ownerNames'])
                )

            self.message(channel, output)
