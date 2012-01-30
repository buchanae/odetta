import os

from distutils.core import setup

import odetta


long_description = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

setup(
    name='odetta',
    description='TODO',
    long_description=long_description,
    version=odetta.__version__,
    author='Alex Buchanan',
    author_email='buchanae@gmail.com',
    license='Apache',
    classifiers=[],
    packages=['odetta',
              'odetta.jobs',
              'odetta.jobs.gff',
              'odetta.jobs.pairs',
              'odetta.jobs.parse'],
    package_data={'odetta': ['Makefile']},
    scripts=['scripts/odetta'],
)
