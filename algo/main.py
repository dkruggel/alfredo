from surprise.model_selection import train_test_split, cross_validate
from surprise import KNNWithMeans
from surprise import SVD
from RecommenderMetrics import RecommenderMetrics
from KNNBakeOff import KNNBakeOff
from data import Data
import sys

def FitAndTest():
    sim_options = {
        'name': 'pearson', 'user_based': False
    }
    # algo = KNNWithMeans(k=20, min_k=1, sim_options=sim_options, verbose=True)
    algo = SVD()

    d = Data()
    data = d.loadData(1000)
    # data = d.loadBusinessLatestSmall()

    # Build full train set
    fullTrainSet = data.build_full_trainset()

    # Build anti test set
    fullAntiTestSet = fullTrainSet.build_anti_testset()

    # Build split train/test set for testing accuracy
    trainSet, testSet = train_test_split(data, test_size=.25, random_state=1)

    # Fit to train set
    algo.fit(trainSet)

    # Test test set
    predictions = algo.test(testSet)
    metrics = {}
    metrics["RMSE"] = RecommenderMetrics.RMSE(predictions)
    metrics["MAE"] = RecommenderMetrics.MAE(predictions)

    print("\nRMSE", metrics["RMSE"])
    print("MAE", metrics["MAE"])

    # Fit full train set
    algo.fit(fullTrainSet)

    # Predictions = Test anti test set
    final_preds = algo.test(fullAntiTestSet)

    # Parse top N
    recommendations = []

    for userID, businessID, actualRating, estimatedRating, _ in final_preds:
        bName = d.getBusinessName(businessID)
        cats, hours = d.getBusinessData(businessID)
        # recommendations.append((bName, estimatedRating, cats, hours))
        recommendations.append((bName, estimatedRating))

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


# FitAndTest()
user_name = sys.argv[1]
GetBusinesses(user_name)
