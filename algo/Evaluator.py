# -*- coding: utf-8 -*-
"""
Created on Thu May  3 10:22:34 2018

@author: Frank
"""
from EvaluationData import EvaluationData
from EvaluatedAlgorithm import EvaluatedAlgorithm

class Evaluator:
    
    algorithms = []
    
    def __init__(self, dataset, rankings):
        ed = EvaluationData(dataset, rankings)
        self.dataset = ed
        
    def AddAlgorithm(self, algorithm, name):
        alg = EvaluatedAlgorithm(algorithm, name)
        self.algorithms.append(alg)

    def GetBusinessName(business_id):
        with open('/home/davidkruggel/repos/alfredo/client/src/yelp_dataset/yelp_academic_dataset_business.json') as f:
            stream = f.readlines()
            for line in stream:
                b_id = line[16:38]
                b_name = line[line.find('name') + 7:line.find('address') - 3]
                if business_id == b_id:
                    return b_name
        
    def Evaluate(self, doTopN):
        results = {}
        for algorithm in self.algorithms:
            # print("Evaluating ", algorithm.GetName(), "...")
            results[algorithm.GetName()] = algorithm.Evaluate(self.dataset, doTopN)

        # Print results
        print("\n")
        
        if (doTopN):
            print("{:<10} {:<10} {:<10} {:<10} {:<10} {:<10} {:<10} {:<10} {:<10}".format(
                    "Algorithm", "RMSE", "MAE", "HR", "cHR", "ARHR", "Coverage", "Diversity", "Novelty"))
            for (name, metrics) in results.items():
                print("{:<10} {:<10.4f} {:<10.4f} {:<10.4f} {:<10.4f} {:<10.4f} {:<10.4f} {:<10.4f} {:<10.4f}".format(
                        name, metrics["RMSE"], metrics["MAE"], metrics["HR"], metrics["cHR"], metrics["ARHR"],
                                      metrics["Coverage"], metrics["Diversity"], metrics["Novelty"]))
        else:
            print("{:<10} {:<10} {:<10}".format("Algorithm", "RMSE", "MAE"))
            for (name, metrics) in results.items():
                print("{:<10} {:<10.4f} {:<10.4f}".format(name, metrics["RMSE"], metrics["MAE"]))
        
    def SampleTopNRecs(self, data, testSubject='david', k=10):
        
        for algo in self.algorithms:
            # print("\nUsing recommender ", algo.GetName())
            
            # print("\nBuilding recommendation model...")
            trainSet = self.dataset.GetFullTrainSet()
            algo.GetAlgorithm().fit(trainSet)
            
            # print("Computing recommendations...")
            testSet = self.dataset.GetAntiTestSetForUser(testSubject)
        
            predictions = algo.GetAlgorithm().test(testSet)
            
            recommendations = []
            
            print ("\nWe recommend:")
            for userID, businessID, actualRating, estimatedRating, _ in predictions:
                bName = data.getBusinessName(businessID)
                cats, hours = data.getBusinessData(businessID)
                recommendations.append((bName, estimatedRating, cats, hours))
            
            recommendations.sort(key=lambda x: x[1], reverse=True)

            return recommendations[:10]

            # for ratings in recommendations[:10]:
            #     # Return a dictionary with businessID, rating, categories, hours
            #     # and don't print the below line
            #     # Add data to MongoDB and change code to use the DB
            #     print(data.getBusinessName(ratings[0])) #, ratings[1]