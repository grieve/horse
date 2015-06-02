import random
import requests
from datetime import datetime
from cStringIO import StringIO

import matplotlib.pyplot as plt

import horse.config
import horse.utils.imgur
from horse.bridles.base import CommandBridle


class ForecastIO(CommandBridle):

    class Meta(CommandBridle.Meta):
        command = 'weather'
        description = "Pulls and represents weather info from forecast.io"
        help_text = ["Usage: `/horse weather [location]`"]

        display_name = "Weather Forecast"
        display_icon = "http://ryangrieve.com/labs/slack_icons/weather.png"

    def __init__(self, jockey):
        super(ForecastIO, self).__init__(jockey)
        self.locations = {
            "belfast": "54.58970503,-5.92369347",
            "london": "51.52908935,-0.08757537"
        }

    def get_current_weather(self, location):
        coords = self.locations[location]
        url = "https://api.forecast.io/forecast/{0}/{1}?units=si".format(
            horse.config.FORECASTIO_API_TOKEN,
            coords
        )
        response = requests.get(url)
        if response.status_code == 200:
            forecast = response.json()
            return forecast
        else:
            return None

    def determine_location(self, operands):
        location = None
        for place in self.locations:
            if place in operands:
                location = place

        if not location:
            location = 'belfast'

        return location

    def execute(self, user, channel, operands):
        location = self.determine_location(operands)
        weather = self.get_current_weather(location)
        msg = "*%s*: _%s_, %.0fdeg\n%s %s %s" % (
            location.capitalize(),
            weather['currently']['summary'],
            weather['currently']['temperature'],
            weather['minutely']['summary'],
            weather['hourly']['summary'],
            weather['daily']['summary']
        )
        self.message(channel, msg)


class WeatherGraph(ForecastIO):

    class Meta(ForecastIO.Meta):
        _secret = True
        command = '_'

    def execute(self, user, channel, operands):
        location = self.determine_location(operands)
        weather = self.get_current_weather(location)
        data = self.get_data(weather, operands)
        plot = self.draw_plot(data, location)
        url = horse.utils.imgur.post_from_file(plot)
        self.message(channel, url)

    def get_data(self, weather):
        return []

    def get_title(self, location):
        return ""

    def draw_plot(self, data, location):
        output = StringIO()
        with plt.xkcd():
            plt.clf()
            plt.plot(*data, c=random.choice("bgrcmykw"))
            plt.gcf().autofmt_xdate()
            plt.title(self.get_title(location))
            plt.savefig(output, format="png")
        output.seek(0)
        return output


class RainGraph(WeatherGraph):

    class Meta(WeatherGraph.Meta):
        command = 'rain'

    def get_title(self, location):
        return "Rain intensity for the next 24 hours in {0}".format(
            location.capitalize()
        )

    def get_data(self, weather, operands):
        return (
            [
                datetime.fromtimestamp(d['time'])
                for d in weather['hourly']['data'][:24]
            ],
            [
                d['precipIntensity']
                for d in weather['hourly']['data'][:24]
            ]
        )


class TemperatureGraph(WeatherGraph):

    class Meta(WeatherGraph.Meta):
        command = 'temperature'

    def get_title(self, location):
        return "Temperature (C) for next 24 hours in {0}".format(
            location.capitalize()
        )

    def get_data(self, weather, operands):
        return (
            [
                datetime.fromtimestamp(d['time'])
                for d in weather['hourly']['data'][:24]
            ],
            [
                d['temperature']
                for d in weather['hourly']['data'][:24]
            ]
        )
