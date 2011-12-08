TODO

```
$ filter_complete_pair.py  alignments.sam > incomplete_pairs.pickle
$ split_splat.py splats.splat > split_splats.pickle
$ filter_invalid_pairs.py incomplete_pairs.pickle split_splats.pickle > valid_splats.pickle
$ combine_splats.py valid_splats.pickle > valid.splat
```
