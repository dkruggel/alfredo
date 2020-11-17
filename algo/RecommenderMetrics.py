import itertools

from operator import itemgetter, truediv
from surprise import accuracy
from collections import defaultdict

class RecommenderMetrics:

  def MAE(predictions):
    return accuracy.mae(predictions, verbose=False)

  def RMSE(predictions):
    return accuracy.rmse(predictions, verbose=False)

  def ReturnTopN(predictions, n=10, minRating=4.0):
    top_n = defaultdict(list)

    for userID, businessID, actualStars, estimatedStars, _ in predictions:
      if (estimatedStars >= actualStars):
        top_n[int(userID)].append((int(businessID), estimatedStars))
        
    for userID, stars in top_n.items():
      stars.sort(key=itemgetter(1), reverse=True)
      top_n[int(userID)] = stars[:n]
    
    return top_n

  def HitRate(topNPredicted, leftOutPredictions):
    hits = 0
    total = 0

    for leftOut in leftOutPredictions:
      userID = leftOut[0]
      leftOutBusinessID = leftOut[1]
      hit = False
      for businessID, predictedRating in topNPredicted[int(userID)]:
        if (int(leftOutBusinessID) == int(businessID)):
          hit = True
          break
      if (hit):
        hits += 1

      total += 1

    return hits/total

  def CumulativeHitRate(topNPredicted, leftOutPredictions, ratingCutoff=0):
    hits = 0
    total = 0

    for userID, leftOutBusinessID, actualStars, estimatedStars, _ in leftOutPredictions:
      if (actualStars >= ratingCutoff):
        hit = False
        for businessID, predictedStars in topNPredicted[int(userID)]:
          if (int(leftOutBusinessID) == businessID):
            hit = True
            break
        if (hit):
          hits += 1

        total += 1

    return hits/total

  def RatingHitRate(topNPredicted, leftOutPredictions):
    hits = defaultdict(float)
    total = defaultdict(float)

    for userID, leftOutBusinessID, actualStars, estimatedStars, _ in leftOutPredictions:
      hit = False
      for businessID, predictedStars in topNPredicted[int(userID)]:
        if (int(leftOutBusinessID) == businessID):
          hit = True
          break
      if (hit):
        hits += 1

      total += 1

    return hits/total

  def AverateReciprocalHitRank(topNPredicted, leftOutPredictions):
    summation = 0
    total = 0

    for userID, leftOutBusinessID, actualStars, estimatedStars, _ in leftOutPredictions:
      hitRank = 0
      rank = 0
      for businessID, predictedStars in topNPredicted[int(userID)]:
        rank = rank + 1
        if (int(leftOutBusinessID) == businessID):
          hitRank = rank
          break
      if (hitRank > 0):
        summation += 1.0 / hitRank

      total += 1

    return summation / total

  def UserCoverage(topNPredicted, numUsers, ratingThreshold=0):
    hits = 0
    for userID in topNPredicted.keys():
      hit = False
      for businessID, predictedStars in topNPredicted[userID]:
        if (predictedStars >= ratingThreshold):
          hit = True
          break
      if (hit):
        hits += 1

    return hits / numUsers

  def Diversity(topNPredicted, simsAlgo):
    n = 0
    total = 0
    simsMatrix = simsAlgo.compute_similarities()
    for userID, in topNPredicted.keys():
      pairs = itertools.combinations(topNPredicted[userID], 2)
      for pair in pairs:
        business1 = pair[0][0]
        business2 = pair[1][0]
        innerID1 = simsAlgo.trainset.to_inner_iid(str(business1))
        innerID2 = simsAlgo.trainset.to_inner_iid(str(business2))
        similarity = simsMatrix[innerID1][innerID2]
        total += similarity
        n += 1

    S = total / n
    return (1-S)

  def Novelty(topNPredicted, rankings):
    n = 0
    total = 0
    for userID in topNPredicted.keys():
      for rating in topNPredicted[userID]:
        businessID = rating[0]
        rank = rankings[businessID]
        total += rank
        n += 1

    return total / n