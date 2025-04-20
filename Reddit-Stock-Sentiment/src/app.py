from flask import Flask, render_template, request, jsonify

from reddit_sentiment import RedditSentiment
from stock_data import StockDataFetcher

import os

from dotenv import load_dotenv
load_dotenv()

app = Flask (__name__)

sentiment_analyzer = RedditSentiment()
stock_fetcher = StockDataFetcher()

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze() :
    try :
        #stock_symbol = request.form.get('stock_symbol', '').upper()
        stock_symbol = request.form.get("stock_symbol", "").strip().upper()
        


        sentiment_data = sentiment_analyzer.analyze_sentiment(stock_symbol)
        stock_data = stock_fetcher.get_StockData(stock_symbol)
        
        result = {
            'stock_symbol' : stock_symbol,
            'sentiment': sentiment_data,
            'stock_data' : stock_data
        }
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'oops error': str(e)}),500
    
if __name__ == '__main__':
    app.run(debug=True)
