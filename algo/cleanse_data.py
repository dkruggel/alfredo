import os
import json

file_path = os.path.expanduser('~/repos/alfredo/client/src/yelp_dataset/reviews.json')

f = open(file_path)

data = json.load(f)

print(data['reviews'])

f.close()