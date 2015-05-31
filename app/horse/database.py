import logging

import sqlobject
from sqlobject.dberrors import OperationalError

from . import config
from . import models


def configure():
    db = sqlobject.connectionForURI(
        'sqlite:{0}'.format(config.DATABASE_LOCATION)
    )
    sqlobject.sqlhub.processConnection = db
    for model in [models.User, models.Channel]:
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
