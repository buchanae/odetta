# Odetta

Odetta contains tools for filtering paired-end Splat alignments.


## Installation

```pip install -r requirements.txt```

Odetta requires a couple python packages, [mrjob](http://packages.python.org/mrjob/) 
and [nose](http://readthedocs.org/docs/nose/).

Using a [virtualenv](http://pypi.python.org/pypi/virtualenv) is recommended, of course.


## Usage

Using Odetta might look like this...

1.  Parse a SAM-formatted file, filter out alignments that are part of a complete pair.

    ```python filter_complete_pair.py alignments.sam > incomplete_pairs.json```

2.  Parse a Splat-formatted file, splitting read IDs into individual alignments.

    ```python split_splat.py splats.splat > split_splats.json```

3.  Filter the data from the previous two steps with criteria for valid pairs,
    including chromosome, strand, distance, etc.

    ```python filter_invalid_pairs.py --min-distance 100 --max-distance 1000 
       incomplete_pairs.json split_splats.json > valid_splats.json```

4.  Combine the valid splats from the previous step, outputting a Splat-formatted file.

    ```python combine_splats.py valid_splats.json > valid.splat```


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
