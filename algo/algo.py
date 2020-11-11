#!/usr/bin/env python3

from io import FileIO
from surprise import Reader
from load_data import d
from recommender import algo

trainingSet = d.build_full_trainset()

algo.fit(trainingSet)

f = open('~/repos/alfredo/client/src/yelp_dataset/reviews_1.json')

stream = FileIO.readlines(f)

for line in stream:
  reader = Reader(line_format='user item rating timestamp', sep='\t')
  user_id = reader.parse_line()[0]
  prediction = algo.predict('cvAPwZRWaDxSUudy8CR3Rw', 'Iq7NqQD-sESu3vr9iEGuTA')
  print(prediction.est)