try:
    from setuptools import setup
    # arguments that distutils doesn't understand
    setuptools_kwargs = {
        'install_requires': [
            'mrjob',
            'rtree',
            'pyfasta',
            'gff',
            'stats',
        ],
        'dependency_links': [
            'http://github.com/abuchanan/gff/tarball/master#egg=gff-0.1',
            'http://github.com/abuchanan/stats/tarball/master#egg=stats-0.1',
        ],
        'provides': ['odetta'],
        'tests_require': ['nose'],
    }
except ImportError:
    from distutils.core import setup
    setuptools_kwargs = {}

import odetta


setup(
    name='odetta',
    description='TODO',
    long_description=open('README.md').read(),
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
    **setuptools_kwargs
)
