import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from  plotter import SentimentPlotter  # make sure this is the correct import path

# Create instance of SentimentPlotter
plotter = SentimentPlotter()

# ---------- Generate Fake Daily Sentiment & Moving Average ----------
dates = pd.date_range(datetime.today() - timedelta(days=9), periods=10)
daily_scores = np.random.uniform(-1, 1, size=10)
moving_avg_scores = pd.Series(daily_scores).rolling(3).mean()

sentiment_result = {
    "daily_sentiment": pd.Series(data=daily_scores, index=dates),
    "moving_avg": pd.Series(data=moving_avg_scores, index=dates)
}

# ---------- Generate Fake Sentiment Scores ----------
sentiment_scores = list(np.random.normal(loc=0, scale=0.5, size=100))

# ---------- Generate Fake Post Data with Quality Scores ----------
posts_df = pd.DataFrame({
    "post_id": [f"id_{i}" for i in range(100)],
    "quality_score": np.random.rand(100) * 10
})

# ---------- Generate Fake Stock Data ----------
stock_data = pd.DataFrame({
    "Close": np.random.uniform(100, 200, size=10)
}, index=dates)

# ---------- Run All Plot Functions ----------
print("Testing: plot_sentiment_trend")
fig1 = plotter.plot_sentiment_trend(sentiment_result, "Test Sentiment Trend")
plotter.save_plot(fig1, "plots/test_sentiment_trend.png")

print("Testing: plot_sentiment_distribution")
fig2 = plotter.plot_sentiment_distribution(sentiment_scores, "Test Sentiment Distribution")
plotter.save_plot(fig2, "plots/test_sentiment_distribution.png")

print("Testing: plot_quality_scores")
fig3 = plotter.plot_quality_scores(posts_df, "Test Quality Score Distribution")
plotter.save_plot(fig3, "plots/test_quality_scores.png")

print("Testing: plot_sentiment_vs_price")
fig4 = plotter.plot_sentiment_vs_price(sentiment_result, stock_data, "Test Sentiment vs Price")
plotter.save_plot(fig4, "plots/test_sentiment_vs_price.png")

print("✅ All plots generated and saved successfully.")
