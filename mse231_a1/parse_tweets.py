import sys
import json
import datetime

print("date", "time", "username", "og_poster", sep = "\t")

for tweet in sys.stdin:
    obj = json.loads(tweet)
    
    # Use this to get date and time
    # Could consider using location data to identify timezone
    try:
        dt = obj['created_at'].split(" ")
        dt_use = datetime.datetime.strptime(dt[1]+dt[2]+dt[5]+" "+dt[3], '%b%d%Y %H:%M:%S')
        
        # Round datetime to nearest 15 minutes
        seconds = (dt_use - dt_use.min).seconds
        rounded = (seconds+(60*15)/2) // (60*15) * (60*15)
        dt_use = dt_use + datetime.timedelta(0,rounded-seconds)
        
        date = dt_use.date()
        time = dt_use.time()
    except:
        date = "NA"
        time = "NA"
    
    # Use to get "name"
    try:
        username = obj['user']['screen_name']
    except:
        username = "NA"
    
    # Name of og poster if retweeted
    try:
        og_poster = obj['retweeted_status']['user']['screen_name']
    except:
        og_poster = "NA"
        
    # Prints relevant values in tab separated format
    print(date, time, username, og_poster, sep = "\t")