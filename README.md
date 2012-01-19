# Odetta

Odetta is a set of tools for discovering and analyzing novel transcript isoforms using paired-end RNA-Seq data.

External software is used at various points in the pipeline:
* CASHX is used for sequence alignment.
* multisplat is used to discover splice junctions.
* GMB is used to discover novel gene models.


## Installation

```pip install -r requirements.txt```

Odetta requires a couple python packages, [mrjob](http://packages.python.org/mrjob/) 
and [nose](http://readthedocs.org/docs/nose/).

TODO note about rtree

Using a [virtualenv](http://pypi.python.org/pypi/virtualenv) is recommended, of course.


## Usage

Using Odetta might look like this...

TODO

## Configuration

You can set up a [mrjob configuration](http://packages.python.org/mrjob/configs.html).  For example...

__mrjob.conf__

    runners:
      local:
        base_tmp_dir: /path/to/tmp/dir
          jobconf:
            mapreduce.job.maps: 8
            mapreduce.job.reduces: 7

Use the configuration with...

```python example.py --conf-path ./mrjob.conf input_file > output_file```

_mapreduce.job.maps_ and _mapreduce.job.reduces_ are particularly useful for utilizing all available processors when running locally (i.e. not Hadoop).

The [mrjob docs](http://packages.python.org/mrjob/configs.html) describe all available
options.


## Development Notes

Odetta uses [mrjob](http://packages.python.org/mrjob/) for map/reduce processing.
mrjob makes developing and running map/reduce easy, both locally and on Hadoop.

I have __not__ tested this on Hadoop.

[nose](http://readthedocs.org/docs/nose/) is used for unit testing.  You can run the tests using `nosetests tests/`.
