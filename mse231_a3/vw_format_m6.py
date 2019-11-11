#########################################################################################################
## Author: Michael Spencer, Andrew (Foster) Docherty, Jorge Nam Song
## Project: MS&E 231 A3
## Script Purpose: Formats tweet data into a readable format for Vowpal Wabbit.
## Notes: Good features may include hour of day, minute of hour, number of capital letters...
#########################################################################################################

# Libraries
import sys
import re
from datetime import datetime as dt

# Parameters
INDEX_WHO = 0
INDEX_DATETIME = 1
INDEX_TWEET = 2


def get_label(tweeter):
    if (tweeter == "Trump"):
        return str("1")
    else: 
        return str("-1")


def get_datetime_features(dt_info):
    dt_object = dt.strptime(dt_info, "%Y-%m-%d %H:%M:%S")
    return (" |clock hour_" + str(dt_object.hour))


# NOTE: Still need to implment tweet length
def get_stats_features(tweet_body):
    
    return (" |stats num_caps:" + count_char_type(tweet_body, "caps") 
            + " num_ats:" + count_char_type(tweet_body, "ats") 
            + " num_hash:" + count_char_type(tweet_body, "hash")
            + " has_https_" + str("https:" in tweet_body)
            + " is_retweet_" + str("\"@" in tweet_body)
            + " short_tweet_ " + str(len(tweet_body) < 75)
            + " long_tweet_ " + str(len(tweet_body) > 120))

def get_text_features(tweet_body):
    """Function to get the full tweet body, removing selected words as needed"""
    result = " |text "
    # If retweet, don't return text body (not checking Staff vs. Trump style)
    if (tweet_body.startswith("\"@")):
        return(result)
    else:
        # Make all characters lowercase
        tweet_body = tweet_body.lower()

        # Handle links that lack a leading space by adding one
        tweet_body = re.sub('[^\s]https', ' https', tweet_body)

        # Add dummys, 1st pass
        tweet_body = add_dummys(tweet_body)

        # Replace punctuation with empty string
        punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_|`~'''
        for x in tweet_body: 
            if x in punctuations: 
                tweet_body = tweet_body.replace(x, "") 

        # Add dummys, 2nd pass
        tweet_body = add_dummys(tweet_body)

        # Remove extra spaces
        tweet_body = tweet_body.replace("   ", " ") 
        tweet_body = tweet_body.replace("  ", " ")

        # Handle leading space
        if (tweet_body[0] == " "):
            tweet_body = tweet_body[1:]

        # Remove trailing newlines
        tweet_body = tweet_body.rstrip("\n\r")

        result += tweet_body
        return(result)


def add_dummys(tweet_body):
    """Function to add 'dummy' values for special words and characters"""
    split_text = tweet_body.split(" ")
    words_list = []
    for word in split_text:
        word_to_add = word
        if (word.startswith('@') or word.startswith('.@')):
            word_to_add = "mentiondummy"
        elif (word.startswith('https')):
            word_to_add = "linkdummy"
        elif (word == "a.m." or word == "p.m." or word == "pm" or word.endswith("pmE")):
            word_to_add = "timedummy"
        elif (word == "&amp;"):
            word_to_add = "ampdummy"
        elif (len(word) > 0 and word[0].isdigit()):
            word_to_add = "numberdummy"
        words_list.append(word_to_add)
    words_string = ' '.join(words_list)
    return(words_string)


def count_char_type(text, char = "caps"):
    count = 0
    
    for letter in text:
        if (char == "caps" and letter.isupper()):
            count += 1
        elif (char == "hash" and letter == "#"):
            count += 1
        elif (char == "at" and letter == "@"):
            count += 1
    
    return str(count)


for line in sys.stdin:
    
    tweet_info = line.split("\t")
    
    if (tweet_info[INDEX_WHO] not in ["Trump", "Staff"]):
        continue
    
    label = get_label(tweet_info[INDEX_WHO])
    time_features = get_datetime_features(tweet_info[INDEX_DATETIME])
    stats_features = get_stats_features(tweet_info[INDEX_TWEET])
    text_features = get_text_features(tweet_info[INDEX_TWEET])
    
    # Print out formatted information, features are below
    
    # label 
    # |time hour:[hour] min_of_hour:[min_of_hour]
    # |stats num_caps:[num_caps] num_ats:[num_ats] num_hash:[num_hash] link retweet stats_length:[stats_length]
    # |text text
    print(label + time_features + stats_features + text_features)