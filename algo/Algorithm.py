from surprise import KNNBasic
import heapq
from collections import defaultdict
from operator import itemgetter
from surprise.model_selection import train_test_split
from surprise import accuracy
from data import Data

sim_options = {'name': 'cosine', 'user_based': True}


def GetAccuracy():
    d = Data()
    data = d.loadData()

    trainSet = data.build_full_trainset()

    _, testSet = train_test_split(data, test_size=.25, random_state=1)

    model = KNNBasic(sim_options=sim_options, verbose=False)
    model.fit(trainSet)
    predictions = model.test(testSet)


    mae = accuracy.mae(predictions, verbose=False)

    rmse = accuracy.rmse(predictions, verbose=False)

    return mae, rmse


def GetRecommendations(user='david'):
    d = Data()
    data = d.loadData()

    trainSet = data.build_full_trainset()

    model = KNNBasic(sim_options=sim_options, verbose=False)
    model.fit(trainSet)
    simsMatrix = model.compute_similarities()

    topN = defaultdict(list)
    k = 25
    uiid = trainSet.to_inner_uid(user)

    similarityRow = simsMatrix[uiid]

    similarUsers = []
    for innerID, score in enumerate(similarityRow):
        if (innerID != uiid):
            similarUsers.append((innerID, score))

    kNeighbors = heapq.nlargest(k, similarUsers, key=lambda t: t[1])

    candidates = defaultdict(float)
    for similarUser in kNeighbors:
        innerID = similarUser[0]
        userSimilarityScore = similarUser[1]
        theirRatings = trainSet.ur[innerID]
        for rating in theirRatings:
            candidates[rating[0]] += (rating[1] / 5.0) * userSimilarityScore

    watched = {}
    for itemID, rating in trainSet.ur[uiid]:
        watched[itemID] = 1

    pos = 0
    for itemID, ratingSum in sorted(candidates.items(), key=itemgetter(1), reverse=True):
        if not itemID in watched:
            businessID = trainSet.to_raw_iid(itemID)
            cats, hours = d.getBusinessData(businessID)
            topN[trainSet.to_raw_uid(uiid)].append((businessID, cats))
            pos += 1
            if (pos > 9):
                break

    return topN[user]
