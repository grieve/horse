import logging

import sqlobject
from sqlobject.dberrors import OperationalError

from . import config


def configure():
    db = sqlobject.sqlite.builder()(config.DATABASE_LOCATION)
    sqlobject.sqlhub.processConnection = db


def verify_models(models):
    logging.info('Verifying DB tables for loaded models')
    for model in models:
        try:
            model.createTable()
        except OperationalError:
            logging.info('\t{0} table already exists'.format(model.__name__))
        else:
            logging.info('\t{0} table created'.format(model.__name__))
