from Data.hydrator import hydrate_ids
from Data.twitter_filter import tweet_filter_senti
from Sentiment.senti_eval import senti_by_states
from Sentiment.word_cloud import word_cloud_generate
from Data.utils import date_convertor
from Data.list_monitor import find_new_list
import shutil
import time
import os

def now_time():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

def Sentiment_workflow(list_path='result/tweet_id_list/corona_tweets_389.csv',
                       cache_path = 'result/cache',
                       processed_path = 'result/processed_daily_tweets',):


    print('\n> {} <\nNew tweet id list detected: {}\nStart big data work flow...'.format(now_time(),list_path))

    # convert csv_id index into actual date stamp
    date_name = date_convertor(file_id=int(list_path.split('/')[-1].split('_')[-1].split('.')[0]))
    result_path = os.path.join('result/daily_senti_results',date_name)

    if not os.path.exists(cache_path):
        os.mkdir(cache_path)
    if not os.path.exists(result_path):
        os.mkdir(result_path)

    hydrated_dir = hydrate_ids(list_path = list_path,
                               save_path= cache_path,
                               split_thres=300000)


    tweet_json_path = tweet_filter_senti(src_path=hydrated_dir,
                                         save_path=processed_path,
                                         name = date_name)

    senti_by_states(date=date_name, tweet_json_path=tweet_json_path,
                    save_path=result_path,
                    neutral_thres=0.05,
                    senti_trend_path='./result/senti_trend.json')

    word_cloud_generate(tweet_json_path=tweet_json_path,
                        save_path=os.path.join(result_path,'word_cloud'))

    shutil.rmtree(cache_path) # delete all cached raw tweet data
    if os.path.exists('twarc.log'):
        os.remove('twarc.log')

    print('\n> {} <\nSentiment successfully updated!\nCached data is deleted.\n'.format(now_time()), flush=True)

if __name__ == '__main__':

    while True:
        id_list_path = 'result/tweet_id_list/'
        readed_files = 'result/utils/readed.txt'
        new_lists = find_new_list(id_list_path,readed_files)

        if new_lists is not False:
            for list_path in new_lists:
                Sentiment_workflow(list_path=list_path)

        time.sleep(10)


