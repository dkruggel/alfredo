from KNNBakeOff import KNNBakeOff
import sys

def GetBusinesses(user_name):
  if len(user_name) > 0:
    rec = KNNBakeOff(user_name)
    res = rec.DoBakeOff()
    print(res)
    return res
  else:
    print('Need argument with username.')
    return 'No results'
    
user_name = sys.argv[1]
GetBusinesses(user_name)