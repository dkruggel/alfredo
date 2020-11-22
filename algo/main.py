from KNNBakeOff import KNNBakeOff
import sys

user_name = sys.argv[1]

if len(user_name) > 0:
  rec = KNNBakeOff(user_name)
  rec.DoBakeOff()
else:
  print('Need argument with username.')