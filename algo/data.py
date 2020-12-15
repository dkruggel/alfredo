from datetime import date, datetime
import os
import csv
import sys
import re

from surprise import Dataset
from surprise import Reader

from pymongo import MongoClient
from pprint import pprint

from collections import defaultdict
import pandas as pd

class Data:
  businessID_to_name = {}
  name_to_businessID = {}
  businessInfo = {}
  ratingsPath = '/home/davidkruggel/repos/alfredo/client/src/yelp_dataset/reviews.csv'
  businessesPath = '/home/davidkruggel/repos/alfredo/client/src/yelp_dataset/businesses.csv'

  def loadBusinessLatestSmall(self):
    os.chdir(os.path.dirname(sys.argv[0]))

    ratingsDataset = 0
    self.businessID_to_name = {}
    self.name_to_businessID = {}

    reader = Reader(line_format='user item rating timestamp', sep=',', skip_lines=1)

    ratingsDataset = Dataset.load_from_file(self.ratingsPath, reader=reader)

    with open(self.businessesPath, newline='', encoding='ISO-8859-1') as csvfile:
      businessReader = csv.reader(csvfile)
      next(businessReader)
      for row in businessReader:
        businessID = row[0]
        businessName = row[1]
        self.businessID_to_name[businessID] = businessName
        self.name_to_businessID[businessName] = businessID

    return ratingsDataset

  def loadData(self):
    client = MongoClient("mongodb+srv://admin:pTqU9VLb0BVCyhV1@cluster0.xbrpk.gcp.mongodb.net/alfredo-data?retryWrites=true&w=majority")
    db = client['alfredo-data']
    df = pd.DataFrame(list(db.reviews.find({}, {"UserID":1, "BusinessID":1, "Stars":1, "_id":0})))
    reader = Reader(line_format='user item rating', sep=',', skip_lines=1)

    ratingsDataset = Dataset.load_from_df(df, reader)

    df_b = list(db.businesses.find())

    for row in df_b:
      businessID = row["BusinessID"]
      businessName = row["Name"]
      self.businessInfo[businessID] = [businessName, row["Categories"], row["State"], row["Hours"]]
      self.businessID_to_name[businessID] = businessName
      self.name_to_businessID[businessName] = businessID

    return ratingsDataset


  def getUserRatings(self, user):
    userRatings = []
    hitUser = False
    with open(self.ratingsPath, newline='') as csvfile:
      ratingReader = csv.reader(csvfile)
      next(ratingReader)
      for row in ratingReader:
        userID = row[0]
        if (user == userID):
          businessID = row[1]
          rating = float(row[2])
          userRatings.append((businessID, rating))
          hitUser = True
        if (hitUser and (user != userID)):
          break

      return userRatings

  def getPopularityRanks(self):
    ratings = defaultdict(int)
    rankings = defaultdict(int)
    with open(self.ratingsPath, newline='') as csvfile:
      ratingReader = csv.reader(csvfile)
      next(ratingReader)
      for row in ratingReader:
        businessID = row[1]
        ratings[businessID] += 1
    rank = 1
    for businessID, ratingCount in sorted(ratings.items(), key=lambda x: x[1], reverse=True):
      rankings[businessID] = rank
      rank += 1
    return rankings

  def getBusinessName(self, businessID):
    if businessID in self.businessID_to_name:
      return self.businessID_to_name[businessID]
    else:
      return ''

  def getBusinessID(self, businessName):
    if businessName in self.name_to_businessID:
      return self.name_to_businessID[businessName]
    else:
      return 0

  def getBusinessData(self, business):
    business = self.businessInfo[business]
    cats = business[1]
    hours = business[3]
    if hours == 'ull':
      hours = ''
    return cats, hours
    # with open(self.businessesPath, newline='') as csvfile:
    #   businessReader = csv.reader(csvfile)
    #   next(businessReader)
    #   for row in businessReader:
    #     businessID = row[0]
    #     if (business == businessID):
    #       return row[2], row[4]

    return []