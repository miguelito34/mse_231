import sys
import json

print("date", "time", "username", "og_poster", sep = "\t")

for tweet in sys.stdin:
    obj = json.loads(tweet)
    
    # Use this to get date and time
    # Could consider using location data to identify timezone
    try:
        date = obj['created_at']
        time = obj['created_at']
    except:
        date = "NA"
        time = "NA"
    
    # Use to get "name"
    try:
        #username = obj['user']['name']
        username = obj['user']['screen_name']
    except:
        username = "NA"
    
    # Name of og poster if retweeted
    try:
        #og_poster = obj['retweeted_status']['user']['name']
        og_poster = obj['retweeted_status']['user']['screen_name']
    except:
        og_poster = "NA"
        
    # Prints relevant values in tab separated format
    print(date, time, username, og_poster, sep = "\t")