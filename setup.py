"""A setuptools based setup module for horse.

https://github.com/grieve/horse
"""

from os import path
from codecs import open
from setuptools import setup

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'DESCRIPTION.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='horse',
    version='2.0.0',

    description='A chat bot framework for Slack',
    long_description=long_description,

    url='https://github.com/grieve/horse',

    author='Ryan Grieve',
    author_email='me@ryangrieve.com',

    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Communications :: Chat',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],

    keywords='chatbot slack chat bot communication',

    packages=['horse'],

    install_requires=[
        'websocket-client',
        'requests',
        'sqlobject',
        'flask',
    ],

    extras_require={
        'dev': [],
        'test': [],
    },

    package_data={},
    data_files=[],
    entry_points={},
)
