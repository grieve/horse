import os
import logging


SLACK_API_TOKEN = os.getenv('SLACK_API_TOKEN', '')
DATABASE_LOCATION = os.getenv('HORSE_DATABASE_PATH', '')

BRIDLES = [
    'horse.bridles.core.uptime',
    'horse.bridles.core.admin_commands'
]

logging.basicConfig(
    format='[%(asctime)s]: (%(levelname)s) %(message)s',
    level=logging.DEBUG
)
