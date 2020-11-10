# load_data.py

import os as os
import pandas as pd
from surprise import Dataset
from surprise import Reader

# path to reviews file
file_path = os.path.expanduser('~/repos/alfredo/client/surc/yelp_dataset/reviews.json')

# create reader
reader = Reader(line_format='user business rating timestamp', sep=',')

d = Dataset.load_from_file(file_path, reader=reader)