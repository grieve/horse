import os
import importlib

import horse.config
import horse.jockey
import horse.ext  # NOQA


def run(**kwargs):
    config_path = os.getenv('HORSE_CONFIG_MODULE', None)
    if config_path is None:
        raise Exception(
            'No configuration set. Use enviroment variable HORSE_CONFIG_MODULE'
        )
    config_module = importlib.import_module(config_path)
    horse.config.__dict__.update(config_module.__dict__)
    jockey = horse.jockey.Jockey()
    jockey.start()
