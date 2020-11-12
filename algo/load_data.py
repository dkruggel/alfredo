#!/usr/bin/env python3

import os as os
import pandas as pd
from surprise import Dataset
from surprise import Reader

def DataLoader(self, index):
    # path to reviews file
    file_path = os.path.expanduser(
        '~/repos/alfredo/client/src/yelp_dataset/reviews_{0}.json', index)

    # create reader
    reader = Reader(line_format='user item rating timestamp', sep='\t')

    d = Dataset.load_from_file(file_path, reader=reader)

    return d