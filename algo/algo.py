#!/usr/bin/env python3

from io import FileIO
from sys import stdout
from surprise import Dataset
from surprise import Reader
from surprise import BaselineOnly
from surprise.model_selection import cross_validate
import os as os
from operator import itemgetter
from recommender import algo

business_id = 'Iq7NqQD-sESu3vr9iEGuTA'

def DataLoader(index):
    # path to reviews file
    file_path = os.path.expanduser(
        '~/repos/alfredo/client/src/yelp_dataset/orig_reviews_' + index + '.json')

    # create reader
    reader = Reader(line_format='user item rating timestamp', sep='\t')

    d = Dataset.load_from_file(file_path, reader=reader)

    return d

def Train(index):
  data = DataLoader(str(index))
  trainingSet = data.build_full_trainset()

  algo.fit(trainingSet)
  # cross_validate(BaselineOnly(), data, verbose=True)
  
  preds = []

  with open('/home/davidkruggel/repos/alfredo/client/src/yelp_dataset/yelp_academic_dataset_business.json') as f:
    stream = f.readlines()
    for line in stream:
      b_id = line[16:38]
      prediction = algo.predict('cvAPwZRWaDxSUudy8CR3Rw', b_id)
      if prediction.est != 3.7492:
        preds.append([b_id, prediction.est])

  top_ten = sorted(preds, key=itemgetter(1), reverse=True)[:10]
  return top_ten

def GetBusinessName(business_id):
  with open('/home/davidkruggel/repos/alfredo/client/src/yelp_dataset/yelp_academic_dataset_business.json') as f:
      stream = f.readlines()
      for line in stream:
        b_id = line[16:38]
        b_name = line[line.find('name') + 7:line.find('address') - 3]
        if business_id == b_id:
          return b_name

sum = []
total = 2
for i in range(total):
  sum.append(Train(i))

for b in sum:
  for i in range(len(b)):
    print(GetBusinessName(b[i][0]) + ': ' + str(b[i][1]))