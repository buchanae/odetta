import logging
import os.path
import unittest


def filepath(name):
    return open(os.path.join(os.path.dirname(__file__), 'files', name))


def disable_mrjob_loggers():
    logging.getLogger('mrjob.local').setLevel(100)
    logging.getLogger('mrjob.runner').setLevel(100)
    logging.getLogger('mrjob.conf').setLevel(100)
