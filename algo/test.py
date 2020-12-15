from data import Data
from surprise import KNNBasic
from surprise.model_selection import train_test_split

d = Data()
# get user/item rating matrix
data = d.loadData()

# build train and test sets
trainSet, testSet = train_test_split(data, test_size=.25, random_state=1)

# get user/user sim matrix
sim_options = {'name': 'pearson',
               'user_based': True
               }

model = KNNBasic(k=40, min_k=1, sim_options=sim_options, verbose=False)
model.fit(trainSet)

simMatrix = model.compute_similarities()

# look up similar users


print("Done")

# generate candidates
# score candidates
# filter candidates
# sort candidates
# return top n candidates