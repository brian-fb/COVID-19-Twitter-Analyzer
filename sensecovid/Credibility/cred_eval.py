from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.metrics import classification_report,confusion_matrix
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from sklearn.calibration import CalibratedClassifierCV
import argparse
import numpy as np
import pickle
import itertools
import pandas as pd
import nltk
import re
#nltk.download('stopwords')

class Credibility_Analysis():
    
    def __init__(self, model_path = "Cred_Eval_model.pkl"):
        
        # Load Model from the given path
        pkl_filename = model_path
        with open(pkl_filename, 'rb') as file:
            self.Cred_Eval_model = pickle.load(file)
        # Set up stopwords
        self.stops = set(stopwords.words("english"))
    
    def cleantext(self, string):
        text = string.lower().split()
        text = " ".join(text)
        text = re.sub(r"http(\S)+",' ',text)    
        text = re.sub(r"www(\S)+",' ',text)
        text = re.sub(r"&",' and ',text)  
        tx = text.replace('&amp',' ')
        text = re.sub(r"[^0-9a-zA-Z]+",' ',text)
        text = text.split()
        text = [w for w in text if not w in self.stops]
        text = " ".join(text)
        return text

    def Evaluate(self,text, only_score = True):
        
        text = self.cleantext(text)
        confidence = self.Cred_Eval_model.predict_proba([text])[0]
        label = self.Cred_Eval_model.predict([text])[0]
        score = confidence[1]/(confidence[0]+confidence[1])

        if only_score:
            return score

        return label,score,(confidence[0],confidence[1])    
    

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description = 'Input the twitter text you want to evaluate')
    parser.add_argument('--text', type = str, help = 'path to csv file that contains twitter id list')
    parser.add_argument('--only_score', type = bool, help = 'True: only output credibility score, False: output label, credibility score, confidence', default = True)
    parser.add_argument('--model_path', type = str, help = 'path to the credibility model file', default = "Cred_Eval_model.pkl")
    args = parser.parse_args()
    
    Cred_Model = Credibility_Analysis(model_path = args.model_path)
    print(Cred_Model.Evaluate(text = args.text, only_score = args.only_score))
    