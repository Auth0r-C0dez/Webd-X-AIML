import pandas as pd
from sentiment_analyzer import v2SentimentAnalyzer

# Instantiate analyzer
analyzer = v2SentimentAnalyzer()

# Sample test data (3 posts with different traits)
test_data = [
    {
        'text': "I'm super bullish on $AAPL, earnings were amazing! 🚀",
        'score': 30,
        'created_utc': "2025-04-10"
    },
    {
        'text': "Not sure about $TSLA, but it might recover soon.",
        'score': 12,
        'created_utc': "2025-04-11"
    },
    {
        'text': "Red day again... market looking weak 😞",
        'score': 8,
        'created_utc': "2025-04-12"
    },
    {
        'text': "Crypto is bouncing back! $BTC above $70k!",
        'score': 20,
        'created_utc': "2025-04-13"
    },
    {
        'text': "FOMC meeting coming up. Be careful.",
        'score': 5,
        'created_utc': "2025-04-14"
    },
    {
        'text': "Sold everything. Too risky to hold now.",
        'score': 18,
        'created_utc': "2025-04-15"
    },
    {
        'text': "Stocks finally green! Bull run incoming?",
        'score': 25,
        'created_utc': "2025-04-16"
    }
]


# Convert to DataFrame
df = pd.DataFrame(test_data)

# Step 1: Preprocess
df['text'] = df['text'].apply(analyzer.preProcess)

# Step 2: Remove low quality posts
filtered_df = analyzer.remove_low_posts(df)

# Step 3: Sentiment analysis on filtered posts
filtered_df['sentiment'] = filtered_df['text'].apply(analyzer.analyse_sentiment)

# Step 4: Predict market trend
result = analyzer.predict_market(filtered_df, window_size=3)

# Print all key results
print("=== Filtered Posts ===")
print(filtered_df[['created_utc', 'text', 'score', 'sentiment', 'quality_score']])
print("\n=== Daily Sentiment ===")
print(result['daily_sentiment'])
print("\n=== Moving Average ===")
print(result['moving_avg'])
print("\n=== Market Trend ===")
print(result['trend'])
print("\n=== Current Sentiment ===")
print(result['current_sentiment'])
