import logging

HOSTNAME = ''
DATABASE_URI = ''

SLACK_API_TOKEN = ''
FORECASTIO_API_TOKEN = ''
IMGUR_API_TOKEN = ''


BRIDLES = [
    'horse.bridles.core.help',
    'horse.bridles.core.uptime',
    'horse.bridles.core.weather',
]

logging.basicConfig(
    format='[%(asctime)s]: {%(threadName)s} (%(levelname)s) %(message)s',
    level=logging.DEBUG
)
