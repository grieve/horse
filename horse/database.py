import logging

import sqlobject
from sqlobject.dberrors import OperationalError

import horse.config
import horse.models


def configure():
    db = sqlobject.connectionForURI(horse.config.DATABASE_URI)
    sqlobject.sqlhub.processConnection = db
    for model in [horse.models.User, horse.models.Channel]:
        try:
            model.createTable()
        except OperationalError, err:
            logging.debug(err)
            logging.info('\t{0} table already exists'.format(model.__name__))
        else:
            logging.info('\t{0} table created'.format(model.__name__))


def verify_models(bridle_models):
    logging.info('Verifying DB tables for loaded models')
    for model in bridle_models:
        try:
            model.createTable()
        except OperationalError, err:
            logging.debug(err)
            logging.info('\t{0} table already exists'.format(model.__name__))
        else:
            logging.info('\t{0} table created'.format(model.__name__))
