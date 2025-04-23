from reddit_sentiment import RedditSentiment  # assuming your file is named reddit_sentiment.py

# Step 1: Instantiate
rs = RedditSentiment()

print("\n====== Test 1: clean_text() ======")
sample_text = "Check this out: [amazing](http://link.com)! It's great."
cleaned = rs.clean_text(sample_text)
print("Original:", sample_text)
print("Cleaned :", cleaned)

print("\n====== Test 2: fetch_sentiment_score() ======")
sentiment = rs.fetch_sentiment_score(sample_text)
print("Sentiment Score:", sentiment)

print("\n====== Test 3: fetch_reddit_posts() ======")
stock_symbol = "AAPL"  # Change to something popular for more posts
posts_df = rs.fetch_reddit_posts(stock_symbol, limit=10)
print(f"Fetched {len(posts_df)} posts")
print(posts_df.head())  # Print top 5 rows

print("\n====== Test 4: analyze_sentiment() ======")
result = rs.analyze_sentiment(stock_symbol)
print("Sentiment Analysis Result:")
print(result)
