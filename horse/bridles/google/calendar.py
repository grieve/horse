import datetime
import httplib2

from apiclient.discovery import build

from horse import config
from horse.bridles.base import CommandBridle

from .auth import GoogleAuthMixin


class MeetingRooms(CommandBridle, GoogleAuthMixin):

    class Meta(CommandBridle.Meta):
        command = "rooms"
        display_name = "Meeting Rooms"
        display_icon = (
            "http://icons.iconarchive.com/icons/marcus-roberto/google-play"
            "/256/Google-Calendar-icon.png"
        )
        description = (
            "Use Google Calendar API to determine status of meetings rooms "
            "in Belfast. Requires Google Auth."
        )
        help_text = [
            "Usage:",
            "\t`/horse rooms`",
            "\t_Please ensure you authenticate with Google using "
            "`/horse gauth` before using this._"
        ]

    rooms = {
        'booth@rehabstudio.com': 'Unit 12 Skype Booth',
        'u12@rehabstudio.com': 'Unit 12 Meeting Room',
        'u13@rehabstudio.com': 'Unit 13 Meeting Room'
    }

    def execute(self, user, channel, operands):
        credentials = self.get_credentials(user)
        if not credentials:
            return "You are not yet authorized. Please check PMs"

        http = httplib2.Http()
        http = credentials.authorize(http)

        service = build(
            serviceName='calendar',
            version='v3',
            http=http,
            developerKey=config.GAPI_CLIENT_ID
        )

        date_min = datetime.datetime.now().strftime('%Y-%m-%dT00:00:00+0100')
        date_max = datetime.datetime.now().strftime('%Y-%m-%dT23:59:59+0100')

        todays_events = {}

        def add_event(calendar_id, evt):
            now = datetime.datetime.now()
            end = datetime.datetime.strptime(
                evt['end']['dateTime'],
                '%Y-%m-%dT%H:%M:%S+01:00'
            )
            start = datetime.datetime.strptime(
                evt['start']['dateTime'],
                '%Y-%m-%dT%H:%M:%S+01:00'
            )

            current = False

            if end < now:
                return

            if end > now and now > start:
                current = True

            todays_events[calendar_id].append({
                'summary': evt['summary'],
                'creator': evt['creator'],
                'start': start,
                'end': end,
                'current': current
            })

        for calendar_id in self.rooms.keys():
            try:
                events = service.events().list(
                    calendarId=calendar_id,
                    maxResults=100,
                    timeMin=date_min,
                    timeMax=date_max
                ).execute()
            except Exception, e:
                print e
            else:
                todays_events[calendar_id] = []
                for evt in events['items']:
                    if 'recurrence' in evt:
                        instances = service.events().instances(
                            calendarId=calendar_id,
                            eventId=evt['id'],
                            timeMax=date_max,
                            timeMin=date_min
                        ).execute()
                        for item in instances['items']:
                            add_event(calendar_id, item)
                    else:
                        add_event(calendar_id, evt)

        output = ""
        for room in todays_events.keys():
            output += '\n*{0}*: '.format(self.rooms[room])
            if len(todays_events[room]) == 0:
                output += '\n\t_Free all day_'
            else:
                sub_output = ''
                current = False
                for event in todays_events[room]:
                    if event['current']:
                        current = True
                    sub_output += "\n\t*{0}*, {1} - {2}".format(
                        event['summary'],
                        event['start'].strftime('%H:%M'),
                        event['end'].strftime('%H:%M')
                    )
                if current:
                    output += '\n\t_Currently occupied_'
                output += sub_output

        self.message(channel, output)
