from functools import wraps
import logging
import os.path
import unittest


def dummy(name):
    return open(os.path.join(os.path.dirname(__file__), 'dummies', name))

def run_dummy(job, dummy_name):
    f = dummy(dummy_name)
    j = job.sandbox(f)
    j.run_job()
    return j.parse_output(j.OUTPUT_PROTOCOL)

def dummytest(job, dummy_name):
    def wrap(f):
        @wraps(f)
        def wrap_f(*args, **kwargs):
            return f(run_dummy(job, dummy_name), *args, **kwargs)
        return wrap_f
    return wrap

def disable_mrjob_loggers():
    logging.getLogger('mrjob.local').setLevel(100)
    logging.getLogger('mrjob.runner').setLevel(100)
    logging.getLogger('mrjob.conf').setLevel(100)
