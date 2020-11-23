from surprise.model_selection import train_test_split, cross_validate
from surprise import KNNWithMeans
from surprise import accuracy
from KNNBakeOff import KNNBakeOff
import sys
from data import Data
from pymongo import MongoClient
from pprint import pprint

# client = MongoClient('')
# db = client.admin

def FitAndTest():
    sim_options = {
        'name': 'pearson', 'user_based': False
    }
    algo = KNNWithMeans(k=40, min_k=1, sim_options=sim_options, verbose=True)

    d = Data()
    data = d.loadBusinessLatestSmall()
    fullTrainSet = data.build_full_trainset()

    results = cross_validate(
        algo=algo, data=data, measures=['RMSE'],
        cv=5, return_train_measures=True
    )

    print(results['test_rmse'].mean())

    algo.fit(fullTrainSet)

    testSet = data.GetAntiTestSetForUser('david')

    predictions = algo.GetAlgorithm().test(testSet)

    recommendations = []

    for userID, businessID, actualRating, estimatedRating, _ in predictions:
        bName = data.getBusinessName(businessID)
        cats, hours = data.getBusinessData(businessID)
        recommendations.append((bName, estimatedRating, cats, hours))

        recommendations.sort(key=lambda x: x[1], reverse=True)

        print(recommendations[:10])


def GetBusinesses(user_name):
    if len(user_name) > 0:
        rec = KNNBakeOff(user_name)
        res = rec.DoBakeOff()
        print(res)
        return res
    else:
        return 'No results'


FitAndTest()
# user_name = sys.argv[1]
# GetBusinesses(user_name)
