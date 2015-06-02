import random

import pylast
import sqlobject

from ... import config
from ..base import CommandBridle
from ..base import BridleModel


class MusicFavourite(BridleModel):
    artist = sqlobject.StringCol()
    title = sqlobject.StringCol()
    fav_count = sqlobject.IntCol(default=1)


class LastFM(CommandBridle):

    class Meta(CommandBridle.Meta):
        command = "music"
        display_name = "Belfast Music"
        display_icon = "http://ryangrieve.com/labs/slack_icons/music.png"
        description = "Gets info on music playing in Unit12 via LastFM"
        help_text = [
            "Usage:",
            "\t`/horse music current` to get the currently playing track",
            "\t`/horse music recent` to get a list of recent tracks",
            "\t`/horse music fav` to add current track to favourites",
            "\t`/horse music suggest` to have horse suggest a song"
        ]

    tips = [
        "Type `/horse music fav` to favourite it!",
        "You can find out recently played songs with `/horse music recent`."
    ]

    def __init__(self, jockey):
        self.jockey = jockey
        self.network = pylast.LastFMNetwork(
            api_key=config.LASTFM_API_KEY,
            api_secret=config.LASTFM_API_SECRET,
            username=config.LASTFM_USERNAME,
            password_hash=pylast.md5(config.LASTFM_PASSWORD)
        )
        self.user_details = pylast.User("rehab_belfast", self.network)

    def current(self):
        msg = "Not playing anything. *Get on it!*"

        track = self.user_details.get_now_playing()
        text_tip = random.choice(self.tips)
        if track:
            msg = "Now playing: {0}. {1}".format(
                "*{0}* - _\"{1}\"_".format(
                    track.artist.name,
                    track.title
                ),
                text_tip
            )

        return msg

    def favourite(self):
        track = self.user_details.get_now_playing()
        if track:
            exists = MusicFavourite.selectBy(
                artist=track.artist.name,
                title=track.title
            ).getOne(None)
            if exists:
                exists.set(fav_count=exists.fav_count + 1)
                msg = "*{0}* - _\"{1}\"_ favourited {2} times!".format(
                    track.artist.name,
                    track.title,
                    exists.fav_count
                )
            else:
                MusicFavourite(
                    artist=track.artist.name,
                    title=track.title
                )
                msg = "*{0}* - _\"{1}\"_ added to favourite songs!".format(
                    track.artist.name,
                    track.title
                )
        else:
            msg = "There is no song currently playing."
        return msg

    def suggest(self):
        suggestions = list(MusicFavourite.select())
        if len(suggestions) > 0:
            suggestion = random.choice(suggestions)
            msg = "How about *{0}* - _\"{1}\"_?".format(
                suggestion.artist,
                suggestion.title
            )
        else:
            msg = "You haven't favourited any songs yet!"

        return msg

    def recent(self, count=5):
        recent_played = self.user_details.get_recent_tracks(count)
        tracks = [
            "\n\t*{0}* - _\"{1}\"_".format(
                t.track.artist.name,
                t.track.title
            ) for t in recent_played
        ]
        msg = 'The most recent tracks were:'
        for track in tracks:
            msg += track
        return msg.decode('utf-8')

    def execute(self, user, channel, operands):
        if len(operands) == 0 or operands[0] == 'current':
            message = self.current()
            self.message(channel, message)

        elif operands[0] == 'recent':
            count = 5
            if len(operands) > 1:
                try:
                    count = int(operands[1])
                except ValueError:
                    pass

            message = self.recent(count)
            self.message(channel, message)

        elif operands[0] == 'suggest':
            message = self.suggest()
            self.message(channel, message)

        elif operands[0] == 'fav':
            message = self.favourite()
            self.message(channel, message)
