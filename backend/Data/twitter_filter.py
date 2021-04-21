import jsonlines
import json
import pandas as pd
from tqdm import tqdm
import os
import re
from Data.utils import find_state_abbrev,len_jsonl
TEXT_CLEANING_RE = "@\S+|https?:\S+|http?:\S|[^A-Za-z0-9]+"

def tweet_filter_senti(src_path,save_path,name):

    """
    tweet data filter for sentiment analysis
    Args:
        src_path:
        save_path:
    Returns:

    """

    print('\nStart filtering latest tweets...\n',flush=True)
    convert_to_csv(src_path)
    merge_csv(src_path)
    tweet_json_path = merged_csv_to_json(src_path, save_path, name)
    print('\nAll tweets are processed! \nFiltered json is saved at: {}'.format(save_path),flush=True)

    return tweet_json_path

def merged_csv_to_json(src_path,save_path,name='merged'):
    state_abbrev = pd.read_csv('./Data/utils/states.csv', index_col=0)
    tweet_df = pd.read_csv(os.path.join(src_path,'merged.csv'), index_col=0)
    tweet_df = tweet_df.sort_values(by=['tweet_retwt_count'], ascending=False).reset_index(drop=True) # rank by number of retweets

    place_tweet_dict = dict()

    print('\nStart converting merged.csv to sorted json dic...',flush=True)
    with tqdm(total=len(tweet_df), mininterval=0.5) as pbar:
        for idx, row in tweet_df.iterrows():
            try:
                place_info = eval(row['tweet_place'])
                country = place_info.get('country_code')
                if country == 'US':
                    state = find_state_abbrev(place_info,state_abbrev)
                    if place_tweet_dict.get(state) is None:
                        place_tweet_dict[state] = list()
                    processed_text = re.sub(TEXT_CLEANING_RE, ' ', str(row['tweet_text']).lower()).strip()
                    place_tweet_dict[state].append(processed_text)
            except:
                pass
            pbar.update(1)

    with open(os.path.join(save_path,(name+'.json')), 'w') as f:
        json.dump(place_tweet_dict, f)
    f.close()

    return os.path.join(save_path,(name+'.json'))

def merge_csv(src_path):
    filelist = []
    for file in os.listdir(src_path):
        if file[-4:] == '.csv':
            filelist.append(file)
    all_data = pd.read_csv(os.path.join(src_path,filelist[0]), index_col=0)
    for file in filelist[1:]:
        try:
            new_csv = pd.read_csv(os.path.join(src_path,file), index_col=0)
            all_data = all_data.append(new_csv).reset_index(drop=True)
        except:
            pass
    all_data.to_csv(os.path.join(src_path,'merged.csv'))

def convert_to_csv(src_path):
    jsonl_files = os.listdir(src_path)
    for file in jsonl_files:
        if file[-6:] == '.jsonl' and file[:4] == 'coro':
            jsonl_to_csv_filter(os.path.join(src_path,file))

def jsonl_to_csv_filter(filename):
    print('Processing file: {}'.format(filename),flush=True)
    total_len = len_jsonl(filename)
    print('Total number of tweets: {}'.format(total_len),flush=True)

    TWEETS_DF = pd.DataFrame(
        columns=['tweet_id', 'tweet_created', 'tweet_text', 'tweet_coord', 'tweet_place', 'tweet_fav_count',
                 'tweet_retwt_count', 'user_id', 'user_created', 'user_verified', 'user_statuses', 'user_fav_count',
                 'user_followers', 'user_friends', 'user_location'])

    with tqdm(total=total_len,mininterval=0.5) as pbar:
        with jsonlines.open(filename) as reader:
            for line in reader:

                tweet_id = line.get('id')
                tweet_created = line.get('created_at')  # UTC time when this Tweet was created
                tweet_text = line.get('full_text')  # The actual UTF-8 text of the status update.
                tweet_coord = line.get('coordinates')  # Nullable. Represents the geographic location of this Tweet as reported by the user or client application. The inner coordinates array is formatted as geoJSON (longitude first, then latitude).
                tweet_place = line.get('place')  # Nullable When present, indicates that the tweet is associated (but not necessarily originating from) a Place .
                tweet_fav_count = line.get('favorite_count')  # Nullable. Indicates approximately how many times this Tweet has been liked by Twitter users.
                tweet_retwt_count = line.get('retweet_count')  # Number of times this Tweet has been retweeted.

                user_dic = line.get('user')
                user_id = user_dic.get('id')
                user_created = user_dic.get('created_at')  # The UTC datetime that the user account was created on Twitter.
                user_verified = user_dic.get('verified')  # When true, indicates that the user has a verified account.
                user_statuses = user_dic.get('statuses_count')  # The number of Tweets (including retweets) issued by the user.
                user_fav_count = user_dic.get('favourites_count')  # The number of Tweets this user has liked in the account’s lifetime.
                user_followers = user_dic.get('followers_count')  # The number of followers this account currently has.
                user_friends = user_dic.get('friends_count')  # The number of users this account is following (AKA their “followings”).
                user_location = user_dic.get('location')  # The user-defined location for this account’s profile. Not necessarily a location, nor machine-parseable.

                if tweet_place is not None:  # True
                    NEW = {'tweet_id': tweet_id, 'tweet_created': tweet_created, 'tweet_text': tweet_text,
                           'tweet_coord': tweet_coord,
                           'tweet_place': tweet_place, 'tweet_fav_count': tweet_fav_count,
                           'tweet_retwt_count': tweet_retwt_count,
                           'user_id': user_id, 'user_created': user_created, 'user_verified': user_verified,
                           'user_statuses': user_statuses,
                           'user_fav_count': user_fav_count, 'user_followers': user_followers,
                           'user_friends': user_friends, 'user_location': user_location}

                    TWEETS_DF = TWEETS_DF.append(NEW, ignore_index=True)
                pbar.update(1)

    TWEETS_DF.to_csv(filename[:-6] + '.csv')

if __name__ == '__main__':
    tweet_filter_senti('data/303/hydrated','data/303/hydrated')