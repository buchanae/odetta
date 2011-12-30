# Odetta

Odetta contains tools for filtering paired-end Splat alignments.


## Installation

```$ pip install -r requirements.txt```

Odetta requires a couple python packages, mrjob and nose.
Using a [virtualenv](http://pypi.python.org/pypi/virtualenv) is recommended, of course.


## Usage

Using Odetta might look like this...

```$ python filter_complete_pair.py alignments.sam > incomplete_pairs.json```

Parse a SAM-formatted file, filter out alignments that are part of a complete pair.

```$ python split_splat.py splats.splat > split_splats.json```

Parse a Splat-formatted file, splitting read IDs into individual alignments.

```$ python filter_invalid_pairs.py --min-distance 100 --max-distance 1000 incomplete_pairs.json split_splats.json > valid_splats.json```

Filter the files from the previous two steps with criteria for valid pairs,
including chromosome, strand, distance, etc.

```$ python combine_splats.py valid_splats.json > valid.splat```

Combine the valid splats from the previous step, outputting a Splat-formatted file.


For more details, check out the [docs]().


## Configuration

You can set up a [mrjob configuration](http://packages.python.org/mrjob/configs.html).  For example...

__mrjob.conf__
```
runners:
  local:
    base_tmp_dir: /path/to/tmp/dir
      jobconf:
        mapreduce.job.maps: 8
        mapreduce.job.reduces: 7
```

Use the configuration with...

```$ python example.py --conf-path ./mrjob.conf input_file > output_file```

mapreduce.job.maps and mapreduce.job.reduces are particularly useful for utilizing all available processors when running locally (i.e. not Hadoop).

For all available options, see the [mrjob docs](http://packages.python.org/mrjob/configs.html).


## Development Notes

Odetta uses [mrjob](http://packages.python.org/mrjob/) for map/reduce processing.
Mrjob makes developing and running map/reduce easy, both locally and on Hadoop.

I have __not__ tested this on Hadoop.

[nose](http://readthedocs.org/docs/nose/) is used for unit testing.  You can run the tests using `$ nosetests tests/`.
