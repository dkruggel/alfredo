#!/usr/bin/env python3

from surprise import KNNWithMeans
from surprise import SVD

sim_options = {
    "name": "msd",
    "user_based": True,
    "min_support": 2
}
# algo = KNNWithMeans(sim_options=sim_options)
algo = SVD()