from surprise.model_selection import train_test_split, cross_validate
from surprise.model_selection import GridSearchCV
from surprise import SVD
from surprise.prediction_algorithms.knns import KNNBaseline
from RecommenderMetrics import RecommenderMetrics
from KNNBakeOff import KNNBakeOff
from data import Data
import sys
import Algorithm
import json
import datetime


def FitAndTest():
    sim_options = {
        'name': 'pearson', 'user_based': False
    }
    # algo = KNNWithMeans(k=20, min_k=1, sim_options=sim_options, verbose=True)
    algo = SVD()

    d = Data()
    data = d.loadData()

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


def SVDAlgo():
    d = Data()
    # Load the movielens-100k dataset (download it if needed),
    data = d.loadData()

    # param_grid = {'bsl_options': {'method': ['als', 'sgd'],
    #                           'reg': [1, 2]},
    #           'k': [2, 3],
    #           'sim_options': {'name': ['msd', 'cosine'],
    #                           'min_support': [1, 5],
    #                           'user_based': [True]}
    #           }

    param_grid = {'bsl_options': {'method': 'als', 'reg': [1, 2]},
                  'k': 2,
                  'sim_options': {'name': 'msd',
                                  'min_support': 5,
                                  'user_based': True}}
    gs = GridSearchCV(KNNBaseline, param_grid, measures=['rmse', 'mae'], cv=5)

    gs.fit(data)

    # best RMSE score
    print(gs.best_score['rmse'])
    print(gs.best_score['mae'])

    # We can now use the algorithm that yields the best rmse:
    algo = gs.best_estimator['rmse']
    trainSet = data.build_full_trainset()
    algo.fit(trainSet)

    predictions = algo.test(trainSet.build_testset())

    res = []
    for userName, itemID, r_ui, est, _ in predictions:
        res.append((userName, itemID, r_ui, est))
    res.sort(key=lambda x: x[3], reverse=True)
    print(res[:10])


def ThirdTimeIsTheCharm(user_name, measureAccuracy):
    if measureAccuracy == 'True':
        rmse, mae = Algorithm.GetAccuracy(user_name)
        res = json.dumps({'rmse': rmse, 'mae': mae})
        print(res)
    else:
        d = Data()
        recs = Algorithm.GetRecommendations(user_name)

        res = []
        for j, k in recs:
            res.append((d.getBusinessName(j), k))

        print(json.dumps(res))


user_name = ''
meas_acc = False
if len(sys.argv) > 1:
    user_name = sys.argv[1]
    meas_acc = sys.argv[2]
ThirdTimeIsTheCharm(user_name, meas_acc)
