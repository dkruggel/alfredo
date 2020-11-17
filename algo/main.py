from numpy.core.numeric import full
from surprise.model_selection.split import LeaveOneOut
from RecommenderMetrics import RecommenderMetrics
import os as os
from surprise import Reader
from surprise import Dataset
from surprise.model_selection import train_test_split
from surprise import SVD
from surprise import KNNBaseline

def DataLoader(index=0):
    # path to reviews file
    file_path = os.path.expanduser(
        '~/repos/alfredo/client/src/yelp_dataset/orig_reviews_' + str(index) + '.json')

    # create reader
    reader = Reader(line_format='user item rating timestamp', sep='\t')

    d = Dataset.load_from_file(file_path, reader=reader)

    return d

data = DataLoader(0)
fullTrainSet = data.build_full_trainset()
sim_options = {'name': 'pearson_baseline', 'user_based': False}
simsAlgo = KNNBaseline(sim_options=sim_options)
simsAlgo.fit(fullTrainSet)

trainSet, testSet = train_test_split(data, test_size=.25, random_state=1)

algo = SVD(random_state=10)
algo.fit(trainSet)

predictions = algo.test(testSet)

print("RMSE: ", RecommenderMetrics.RMSE(predictions))
print("MAE: ", RecommenderMetrics.MAE(predictions))

LOOCV = LeaveOneOut(n_splits=1, random_state=1)

for trainSet, testSet in LOOCV.split(data):
  algo.fit(trainSet)

  leftOutPredictions = algo.test(testSet)

  bigTestSet = trainSet.build_anti_testset()
  allPredictions = algo.test(bigTestSet)

  topNPredicted = RecommenderMetrics.GetTopN(allPredictions, n=10)

  print("\nHit Rate: ", RecommenderMetrics.HitRate(topNPredicted, leftOutPredictions))

  RecommenderMetrics.RatingHitRate(topNPredicted, leftOutPredictions)

algo.fit(fullTrainSet)
bigTestSet = fullTrainSet.build_anti_testset()
allPredictions = algo.test(bigTestSet)
topNPredicted = RecommenderMetrics.GetTopN(allPredictions, n=10)

print(topNPredicted)

print("\nUser coverage: ", RecommenderMetrics.UserCoverage(topNPredicted, fullTrainSet.n_users, ratingThreshold=4.0))

print("\nDiversity: ", RecommenderMetrics.Diversity(topNPredicted, simsAlgo))

print("\nNovelty (average popularity rank): ", RecommenderMetrics.Novelty(topNPredicted, rankings))