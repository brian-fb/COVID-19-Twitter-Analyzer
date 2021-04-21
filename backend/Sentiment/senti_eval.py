import os
import json
import stanza
import pandas as pd
import numpy as np
from tqdm import tqdm
from textblob import TextBlob
#stanza.download('en')

def senti_by_states(date,tweet_json_path,save_path='place_senti.json',neutral_thres=0.05,senti_trend_path='senti_trend.json'):

    print('\nLoading sentiment model...\n',flush=True)
    model = senti_model()

    with open(tweet_json_path,'r') as f:
        tweet_json = json.load(f)
    f.close()
    place_senti_dict = dict()

    print('\nCalculating sentiment indexes by state:',flush=True)

    with tqdm(total=len(tweet_json),mininterval=0.5) as pbar:
        for state in tweet_json.keys():

            tweet_list = tweet_json[state]

            if place_senti_dict.get(state) is None:
                place_senti_dict[state] = dict()
                place_senti_dict[state]['tweet_num'] = 0
                place_senti_dict[state]['negative'] = 0
                place_senti_dict[state]['positive'] = 0
                place_senti_dict[state]['neutral'] = 0
                place_senti_dict[state]['overall_feel'] = 0

            for tweet in tweet_list:
                if len(tweet) > 0:
                    senti_score = model.evaluate(tweet_text=tweet)
                    if senti_score > neutral_thres:
                        place_senti_dict[state]['positive'] = place_senti_dict[state]['positive'] + 1
                    elif senti_score < -neutral_thres:
                        place_senti_dict[state]['negative'] = place_senti_dict[state]['negative'] + 1
                    else:
                        place_senti_dict[state]['neutral'] = place_senti_dict[state]['neutral'] + 1

                    place_senti_dict[state]['overall_feel'] = place_senti_dict[state]['overall_feel'] + senti_score
                    place_senti_dict[state]['tweet_num'] = place_senti_dict[state]['tweet_num'] + 1

            pbar.update(1)

    for state in place_senti_dict.keys():
        place_senti_dict[state]['negative'] = float(
            place_senti_dict[state]['negative'] / place_senti_dict[state]['tweet_num'])
        place_senti_dict[state]['positive'] = float(
            place_senti_dict[state]['positive'] / place_senti_dict[state]['tweet_num'])
        place_senti_dict[state]['neutral'] = float(
            place_senti_dict[state]['neutral'] / place_senti_dict[state]['tweet_num'])
        place_senti_dict[state]['overall_feel'] = float(
            place_senti_dict[state]['overall_feel'] / place_senti_dict[state]['tweet_num'])


    place_senti_percent_json = generate_senti_percent(place_senti_dict)
    place_senti_scaled_json = generate_scaled_senti(place_senti_dict)
    update_senti_trend(senti_trend_path=senti_trend_path,scaled_senti_list=place_senti_scaled_json,date=date)

    with open(os.path.join(save_path,'place_senti.json'), 'w') as f:
        json.dump(place_senti_dict, f)
    f.close()

    with open(os.path.join(save_path,'senti_percentage_by_state.json'), 'w') as f:
        json.dump(place_senti_percent_json, f)
    f.close()

    with open(os.path.join(save_path,'scaled_senti_by_state.json'), 'w') as f:
        json.dump(place_senti_scaled_json, f)
    f.close()



    print('\nSentiment result generated!\nResult file is saved at: {}\n'.format(save_path))

class senti_model():

    def __init__(self):
        self.TEXTBLOB = TextBlob
        self.STANZA = stanza.Pipeline(lang='en', processors='tokenize,sentiment')

    def evaluate(self, tweet_text, weight_S=0.8, weight_TB=0.2):
        record = self.STANZA(tweet_text).sentences
        score_S = np.mean([(i.sentiment - 1) for i in record])
        score_TB = self.TEXTBLOB(tweet_text).sentiment[1]
        return weight_S * score_S + weight_TB * score_TB

def generate_senti_percent(ori_json):

    state_conver = pd.read_csv('./Data/utils/states.csv', index_col=1)
    out_json = dict()
    for key in ori_json.keys():
        if len(key) < 3:
            try:
                state_full = state_conver.loc[key]['State']
                out_json[state_full] = dict()
                out_json[state_full]['positive'] = int(round(ori_json[key]['positive'], 2) * 100)
                out_json[state_full]['negative'] = int(round(ori_json[key]['negative'], 2) * 100)
                out_json[state_full]['neutral'] = 100 - (out_json[state_full]['positive'] + out_json[state_full]['negative'])
            except:
                pass
    return out_json

def generate_scaled_senti(ori_json, shift = 0):

    state_conver = pd.read_csv('./Data/utils/states.csv', index_col=1)
    out_json = list()
    for key in ori_json.keys():
        if len(key) < 3:
            try:
                state_full = state_conver.loc[key]['State']
                new = dict()
                new['name'] = state_full
                new['value'] = round(ori_json[key]['overall_feel'],2)*100 + shift
                out_json.append(new)
            except:
                pass

    return out_json

def update_senti_trend(senti_trend_path,scaled_senti_list,date):
    with open(senti_trend_path,'r') as f:
        senti_trend = json.load(f)
    f.close()
    senti_trend[str(date)] = dict()
    for datapoint in scaled_senti_list:
        senti_trend[str(date)][datapoint['name']] = datapoint['value']

    with open(senti_trend_path,'w') as f:
        json.dump(senti_trend,f)
    f.close()

    print('\n Sentiment Trend Updated! | {}\n'.format(date))

if __name__ == '__main__':

    save_path = '../result/daily_senti_results/2021-04-10/'

    with open('../result/daily_senti_results/2021-04-10/place_senti.json','r') as F:
        in_json = json.load(F)
    F.close()

    place_senti_percent_json = generate_senti_percent(in_json)

    with open(os.path.join(save_path, 'senti_percentage_by_state.json'), 'w') as f:
        json.dump(place_senti_percent_json, f)
    f.close()


