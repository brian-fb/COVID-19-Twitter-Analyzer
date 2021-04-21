import os
import json
import nltk
import stanza
import pandas as pd
import numpy as np
import collections
from tqdm import tqdm
from wordcloud import WordCloud
import matplotlib.pyplot as plt
#you may want run following command lines is there's a missing dependecy during execution
#nltk.download('punkt')
#stanza.download('en')

def word_cloud_generate(tweet_json_path,save_path):

    if not os.path.exists(save_path):
        os.mkdir(save_path)

    mask_shape = plt.imread('./Data/utils/US_mask.png').astype(np.uint8)*255
    state_conver = pd.read_csv('./Data/utils/states.csv', index_col=1)
    stop_word_bag = ['No', 'no', 'not', 'me', 'us', 'off', 'out', 'New', 'new']
    S = stanza_model()

    with open(tweet_json_path, 'r') as f:
        tweet_json = json.load(f)
    f.close()

    print('\nStart Generating word clouds...', flush=True)

    with tqdm(total=len(tweet_json)) as pbar:
        for state in tweet_json.keys():
            if len(state) < 3:  # Ensure State isn't Unknown
                try:
                    state_full_name = state_conver.loc[state]['State']
                    text = str()
                    for tweet in tweet_json[state]:
                        text = text + ' ' + tweet

                    word_list = nltk.word_tokenize(text)

                    subj_list = []
                    thres = 0.02

                    for word in word_list:
                        senti = S.evaluate(word)
                        if senti > thres:
                            subj_list.append(word)
                        if senti < -thres:
                            subj_list.append(word)

                    if len(subj_list) == 0:   #if no useable words in a state, output Error on its word cloud
                        subj_list = ['Error']

                    word_counts = collections.Counter(subj_list)
                    word_counts_top = dict(word_counts.most_common(200))
                    for word in stop_word_bag:
                        try:
                            del word_counts_top[word]
                        except:
                            pass

                    wordcloud = WordCloud(background_color=None,
                                          max_words=50,
                                          width=1000,
                                          height=860,
                                          margin=2,
                                          mask=mask_shape,
                                          colormap='Pastel2',
                                          mode='RGBA'
                                          ).generate_from_frequencies(word_counts_top)

                    plt.axis("off")
                    plt.imshow(wordcloud)
                    plt.title(state_full_name, fontsize=30, color='white')
                    plt.savefig(os.path.join(save_path, (state_full_name + '.png')), format='png', transparent=True,
                                bbox_inches='tight')
                    plt.clf()
                except:
                    pass
            pbar.update(1)

class stanza_model():

    def __init__(self):
        self.STANZA = stanza.Pipeline(lang='en', processors='tokenize,sentiment')

    def evaluate(self, tweet_text):
        record = self.STANZA(tweet_text).sentences
        score_S = np.mean([(i.sentiment - 1) for i in record])
        return score_S

if __name__ == '__main__':
    word_cloud_generate('../Data/data/303/hydrated/place_tweet.json','world_cloud')

