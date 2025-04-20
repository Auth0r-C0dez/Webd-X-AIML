import nltk
nltk.download('punkt_tab')

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import re
import nltk
# nltk.download('stopwords')
# print("al imported succesfully")

class v2SentimentAnalyzer:
    def __init__(self):
        self.sia = SentimentIntensityAnalyzer()
        self.vectorizer = TfidfVectorizer(max_features=1000)
        self.classifer = RandomForestClassifier(n_estimators=100)
        self.stop_words = set(stopwords.words('english'))
        self.quality_threshold = 0.5
        
    def preProcess(self,text):
        if not isinstance(text,str):
            return ""
        text = text.lower()
        text = re.sub(r'[^a-zA-Z\s]','',text) #for removing the random embdded letters in url
        tokens = word_tokenize(text)
        tokens = [word for word in tokens if word not in self.stop_words]
        return ' '.join(tokens)
    
    def calc_qualityScore(self,post):
        score = 0
        if len(post['text']) > 100:
            score +=0.3
        if post['score']>10:
            score+=0.3
            
        sentiment_scores = self.sia.polarity_scores(post['text'])
        score += abs(sentiment_scores['compound']) * 0.4 # for normalisation try not to mess with it 
        return score
    
    def remove_low_posts(self,posts_df):
        posts_df['quality_score'] = posts_df.apply(self.calc_qualityScore,axis=1)
        return posts_df[posts_df['quality_score']>self.quality_threshold]
    
    def analyse_sentiment(self,text):
        vader_sentiment = self.sia.polarity_scores(text)
        
        text_length = len(text)
        words_count = len(text.split())
        question = 1 if '?' in text else 0
        exclamation = 1 if '!' in text else 0
        
        sentiment_score =(vader_sentiment['compound']*0.7 + (text_length/1000)*0.1 + (question *-0.1 ) + (exclamation * 0.1))
        return sentiment_score
    
    def predict_market(self,posts_df,window_size=7):
        if len(posts_df) == 0:
            return {
                'trend': 'Neutral', #done
                'daily-sentiment' : pd.Series(), #dome
                'moving_avg' : pd.Series(), #dome
                'current_sentiment' : 0
            }
            
        posts_df['date'] = pd.to_datetime(posts_df['created_utc'])
        posts_df.set_index('date',inplace = True)
        
        daily_sentiment = posts_df['sentiment'].resample('D').mean()
        moving_avg = daily_sentiment.rolling(window=window_size).mean()
        
        trend='Neutral'
        if len(moving_avg) >0:
            if moving_avg.iloc[-1] >0.2:
                trend = 'Bullish'
            elif moving_avg.iloc[-1] <0.2:
                trend = 'Bearish'
        return {
            'trend' : trend,
            'daily_sentiment' : daily_sentiment,
            'moving_avg' : moving_avg,
            'current_sentiment' : moving_avg.iloc[-1] if len(moving_avg) > 0 else 0
            
        }
