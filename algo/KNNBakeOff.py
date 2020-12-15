from datetime import datetime
from surprise import Reader
from surprise import Dataset
from surprise import KNNBasic
from surprise import SVD
from surprise import NormalPredictor
from Evaluator import Evaluator
import os as os
from data import Data

import random
import numpy as np

class KNNBakeOff:

  def __init__(self, user):
    self.user = user
  
  def LoadMovieLensData(self):
    d = Data()
    # data = d.loadBusinessLatestSmall()
    data = d.loadData()
    # rankings = d.getPopularityRanks()
    rankings = []
    return (d, data, rankings)

  def DoBakeOff(self):
    np.random.seed(0)
    random.seed(0)

    # Load up common data set for the recommender algorithms
    (d, evaluationData, rankings) = self.LoadMovieLensData()

    # Construct an Evaluator to, you know, evaluate them
    evaluator = Evaluator(evaluationData, rankings)

    # SVD
    S = SVD()
    evaluator.AddAlgorithm(S, "SVD")

    # Item-based KNN
    # ItemKNN = KNNBasic(sim_options = {'name': 'cosine', 'user_based': False})
    # evaluator.AddAlgorithm(ItemKNN, "Item KNN")

    # Fight!
    # evaluator.Evaluate(True)

    return evaluator.SampleTopNRecs(d, testSubject=self.user)
