import sys
import json

for tweet in sys.stdin:
    obj = json.loads(tweet)
    print(type(obj))
    print(obj['created_at'])
#     for key in obj.keys():
#         print(key)
#         print(obj[key])
    break