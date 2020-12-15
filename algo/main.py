from data import Data
import sys
import Algorithm
import json


def ThirdTimeIsTheCharm(user_name, measureAccuracy):
    if measureAccuracy == 'True':
        rmse, mae = Algorithm.GetAccuracy()
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
