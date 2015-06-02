import os
import logging

HOSTNAME = os.getenv('VIRTUAL_HOST', '127.0.0.1:5000')
DATABASE_LOCATION = os.getenv('HORSE_DATABASE_PATH', '')

SLACK_API_TOKEN = os.getenv('SLACK_API_TOKEN', '')
FORECASTIO_API_TOKEN = os.getenv('FORECASTIO_API_TOKEN', '')
IMGUR_API_TOKEN = os.getenv('IMGUR_API_TOKEN', '')
GIPHY_API_TOKEN = os.getenv('GIPHY_API_TOKEN', '')

LASTFM_API_KEY = os.getenv('LASTFM_API_KEY', '')
LASTFM_API_SECRET = os.getenv('LASTFM_API_SECRET', '')
LASTFM_USERNAME = os.getenv('LASTFM_USERNAME', '')
LASTFM_PASSWORD = os.getenv('LASTFM_PASSWORD', '')

GAPI_API_TOKEN = os.getenv('GAPI_API_TOKEN', '')
GAPI_CLIENT_ID = os.getenv('GAPI_CLIENT_ID', '')
GAPI_CLIENT_SECRET = os.getenv('GAPI_CLIENT_SECRET', '')
GAPI_SCOPES = [
    'https://www.googleapis.com/auth/calendar',
    'https://www.googleapis.com/auth/drive'
]

GOOGLE_APPS_DOMAIN = os.getenv('GOOGLE_APPS_DOMAIN', '')

BRIDLES = [
    'horse.bridles.core.help',
    'horse.bridles.core.uptime',
    'horse.bridles.core.weather',
    'horse.bridles.fun.flashy',
    'horse.bridles.fun.gifs',
    'horse.bridles.fun.lastfm',
    'horse.bridles.fun.quotes',
    'horse.bridles.fun.sexypaddy',
    'horse.bridles.google.auth',
    'horse.bridles.google.drive',
    'horse.bridles.google.calendar',
    'horse.bridles.google.search',
    'horse.bridles.google.images',
    'horse.bridles.google.maps',
    'horse.bridles.google.hangouts',
]

logging.basicConfig(
    format='[%(asctime)s]: {%(threadName)s} (%(levelname)s) %(message)s',
    level=logging.DEBUG
)
