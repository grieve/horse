import os
import logging

DATABASE_LOCATION = os.getenv('HORSE_DATABASE_PATH', '')

SLACK_API_TOKEN = os.getenv('SLACK_API_TOKEN', '')
FORECASTIO_API_TOKEN = os.getenv('FORECASTIO_API_TOKEN', '')
IMGUR_API_TOKEN = os.getenv('IMGUR_API_TOKEN', '')
GIPHY_API_TOKEN = os.getenv('GIPHY_API_TOKEN', '')

LASTFM_API_KEY = os.getenv('LASTFM_API_KEY', '')
LASTFM_API_SECRET = os.getenv('LASTFM_API_SECRET', '')
LASTFM_USERNAME = os.getenv('LASTFM_USERNAME', '')
LASTFM_PASSWORD = os.getenv('LASTFM_PASSWORD', '')

BRIDLES = [
    'horse.bridles.core.help',
    'horse.bridles.core.uptime',
    'horse.bridles.core.weather',
    'horse.bridles.fun.flashy',
    'horse.bridles.fun.gifs',
    'horse.bridles.fun.lastfm'
]

logging.basicConfig(
    format='[%(asctime)s]: {%(threadName)s} (%(levelname)s) %(message)s',
    level=logging.DEBUG
)
