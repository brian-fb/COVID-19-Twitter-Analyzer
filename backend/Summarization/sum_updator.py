from pyspark import SparkContext, SparkConf
from pyspark.sql.session import SparkSession
from sum_model import Summary_Generator
import pandas as pd
import numpy as np
import json
import time
import os
import re

TEXT_CLEANING_RE = "@\S+|https?:\S+|http?:\S|[^A-Za-z0-9]+"

conf = SparkConf().setAppName('convert_parquet')
sc = SparkContext('local', 'test', conf=conf)
spark = SparkSession(sc)

def get_by_time(dir_path, reverse=True):          
    file_paths = os.listdir(dir_path)
    if len(file_paths) <= 1:
        return []
    else:
        sorted_file_list = sorted(file_paths, key=lambda x: time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.path.getctime(os.path.join(dir_path,x)))), reverse=reverse)
        sorted_file_list_filtered = []
        for i in range(len(sorted_file_list)):
            file = sorted_file_list[i]
            if file[0:4] == 'part':
                sorted_file_list_filtered.append(file)
        return sorted_file_list_filtered[1:]
    
def get_latest_tweets(parc_path = './parc', del_used = True):
    parquetFile_list = get_by_time(parc_path)
    all_tweet = pd.DataFrame(columns=['word'])
    for parquetFile in parquetFile_list:
        raw_data = spark.read.parquet(os.path.join(parc_path,parquetFile))
        all_tweet = all_tweet.append(raw_data.toPandas())
        if del_used:
            os.remove(os.path.join(parc_path,parquetFile))
    return all_tweet

def concat_tweets(all_tweet):
    text = str(); thres = np.minimum(32,len(all_tweet))
    for i,row in all_tweet[0:thres].iterrows():
        filtered_text = re.sub(TEXT_CLEANING_RE, ' ', str(row['word']).lower()).strip()
        text = text+filtered_text
    return text

def sum_updator():
    update_path = '../result/sum_updates/'
    if not os.path.exists(update_path):
        os.mkdir(update_path)
    update_path_sum = os.path.join(update_path, 'latest_sum.json')
    sumarizer = Summary_Generator()
    print('Summarizer Model Successfully Loaded!\n')

    while True:
        time.sleep(30)
        latest_sum = dict()
        all_tweet = get_latest_tweets(parc_path='../result/spark_cache/parc')
        if len(all_tweet) < 1:
            print('No new tweets for update! {}\n'.format(time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime())))
        else:
            tweet_list = list(all_tweet['word'][0:np.minimum(30,len(all_tweet))])
            text = concat_tweets(all_tweet)
            sum_bart = sumarizer.bart(text)
            sum_T5 = sumarizer.T5(text)
            latest_sum['News'] = sum_bart
            latest_sum['Opinions'] = sum_T5
            latest_sum['Tweets'] = tweet_list
            with open(update_path_sum, 'w') as f:
                json.dump(latest_sum, f)
            f.close()
            print('Summarization Updated! {}\n'.format(time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime())))

if __name__ == '__main__':
    
    sum_updator()