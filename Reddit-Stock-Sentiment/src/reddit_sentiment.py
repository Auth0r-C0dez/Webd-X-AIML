from dotenv import load_dotenv
import os
from pathlib import Path

# Determine project root (one level up from this file)
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)
print("DEBUG: REDDIT_CLIENT_ID =", os.getenv("REDDIT_CLIENT_ID"))
print("DEBUG: REDDIT_CLIENT_SECRET =", os.getenv("REDDIT_CLIENT_SECRET"))
print("DEBUG: REDDIT_USER_AGENT =", os.getenv("REDDIT_USER_AGENT"))



import praw
from datetime import datetime
import pandas as pd

# from dotenv import load_dotenv
from textblob import TextBlob
import re

# load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))
#load_dotenv()


from pathlib import Path

# Determine project root (one level up from this file)


# print("loaded successfully")

class RedditSentiment :
    def __init__(self):
        self.reddit = praw.Reddit(
            client_id = os.getenv('REDDIT_CLIENT_ID'),
            client_secret = os.getenv('REDDIT_CLIENT_SECRET'),
            user_agent = os.getenv('REDDIT_USER_AGENT')
        )
        
        
        
    def clean_text(self,text) :
        if not isinstance(text,str) :
            return ""
        text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
        
        text = re.sub(r'[^\w\s]', '', text)
        return text.strip()
    
    def fetch_sentiment_score(self,text):
        cleaned_text = self.clean_text(text)
        if not cleaned_text:
            return 0
        
        analysis = TextBlob(cleaned_text)
        return analysis.sentiment.polarity
    
    def fetch_reddit_posts(self,stock_symbol,limit =100):
        posts = []
        try :
            for post in self.reddit.subreddit('stocks+investing+wallstreetbets').search(
                f'{stock_symbol} stock', limit = limit, time_filter='month'
            ):
                full_text = f"{post.title} {post.selftext}"
                sentiment_score = self.fetch_sentiment_score(full_text)
                posts.append({
                    'title': post.title,
                    'text' : post.selftext,
                    'score' : post.score,
                    'sentiment': sentiment_score,
                    'created_utc': datetime.fromtimestamp(post.created_utc).strftime('%Y-%m-%D %H:%M:%S'),
                    'url': f'https://reddit.com{post.permalink}',
                    'subreddit' : post.subreddit.display_name
                })
                
        except Exception as e:
            print(f'error fetching data {str(e)}')
            
        return pd.DataFrame(posts)
    
    
    
    def analyze_sentiment(self,stock_symbol):
        posts_df = self.fetch_reddit_posts(stock_symbol)
        if len(posts_df) == 0 :
            return {
                'success' : False,
                'error' : f'No post of {stock_symbol}'
            }
            
        avg_sentiment = posts_df['sentiment'].mean()
        posts_df['sentiment_category'] = posts_df['sentiment'].apply(
            lambda x : 'positive' if x > 0 else ('negative' if x < 0 else 'neutral')
            
        )
        
        sentiment_counts = posts_df['sentiment_category'].value_counts().to_dict()
        
        top_posts= posts_df.nlargest(5,'score').to_dict('records')
        
        
        return {
            'success' :True,
            'average_sentiment': float(avg_sentiment),
            'post_count' : len(posts_df),
            'sentiment_distribution' : sentiment_counts,
            'top_posts' : top_posts
        }