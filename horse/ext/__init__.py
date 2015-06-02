import sys


class HorseExtensions(object):

    def __getattr__(self, value):
        import importlib
        try:
            return importlib.import_module('horse_' + value)
        except ImportError:
            raise ImportError(
                "Cannot find horse extension 'horse.ext.{0}'".format(
                    value
                )
            )


sys.modules[__name__] = HorseExtensions()
