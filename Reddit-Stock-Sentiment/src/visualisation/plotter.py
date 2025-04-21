import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for saving plots
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from datetime import datetime, timedelta
import numpy as np
import os

class SentimentPlotter:
    def __init__(self):
        plt.style.use('seaborn-v0_8')  # updated for newer seaborn compatibility
        self.figsize = (12, 8)
    
    def plot_sentiment_trend(self, sentiment_result, title="Sentiment Trend"):
        """
        Plot daily sentiment and moving average trend.

        Parameters:
        - sentiment_result: dict returned from v2SentimentAnalyzer.predict_market()
        """
        daily_sentiment = sentiment_result.get('daily_sentiment')
        moving_avg = sentiment_result.get('moving_avg')

        if daily_sentiment is None or daily_sentiment.empty:
            fig, ax = plt.subplots(figsize=self.figsize)
            ax.text(0.5, 0.5, 'No sentiment data available',
                    horizontalalignment='center', verticalalignment='center')
            plt.title(title)
            return fig
        
        fig, ax = plt.subplots(figsize=self.figsize)
        ax.plot(daily_sentiment.index, daily_sentiment.values, label='Daily Sentiment', marker='o')
        if moving_avg is not None and not moving_avg.empty:
            ax.plot(moving_avg.index, moving_avg.values, label='Moving Average', color='orange', linewidth=2)
        ax.set_xlabel('Date')
        ax.set_ylabel('Sentiment Score')
        ax.legend()
        ax.set_title(title)
        fig.tight_layout()
        return fig
    
    def plot_sentiment_distribution(self, sentiment_scores, title="Sentiment Distribution"):
        """Plot distribution of sentiment scores"""
        plt.figure(figsize=self.figsize)
        if len(sentiment_scores) > 0:
            sns.histplot(sentiment_scores, kde=True)
        else:
            plt.text(0.5, 0.5, 'No sentiment data available',
                     horizontalalignment='center', verticalalignment='center')
        plt.title(title)
        plt.xlabel('Sentiment Score')
        plt.ylabel('Frequency')
        return plt.gcf()
    
    def plot_quality_scores(self, posts_df, title="Post Quality Distribution"):
        """Plot distribution of post quality scores"""
        plt.figure(figsize=self.figsize)
        if 'quality_score' in posts_df.columns and len(posts_df) > 0:
            sns.histplot(posts_df['quality_score'], kde=True)
        else:
            plt.text(0.5, 0.5, 'No quality score data available',
                     horizontalalignment='center', verticalalignment='center')
        plt.title(title)
        plt.xlabel('Quality Score')
        plt.ylabel('Frequency')
        return plt.gcf()
    
    def plot_sentiment_vs_price(self, sentiment_result, stock_data, title="Sentiment vs Stock Price"):
        """
        Plot moving average sentiment vs stock closing price

        Parameters:
        - sentiment_result: dict from predict_market()
        - stock_data: pandas DataFrame with at least a 'Close' column and datetime index
        """
        moving_avg = sentiment_result.get('moving_avg')

        plt.figure(figsize=self.figsize)

        if moving_avg is not None and not moving_avg.empty and not stock_data.empty:
            # Align index
            joined = pd.concat([moving_avg, stock_data['Close']], axis=1, join='inner').dropna()
            joined.columns = ['Sentiment', 'Close']

            plt.scatter(joined['Sentiment'], joined['Close'])

            # Add trend line
            try:
                z = np.polyfit(joined['Sentiment'], joined['Close'], 1)
                p = np.poly1d(z)
                plt.plot(joined['Sentiment'], p(joined['Sentiment']), "r--")
            except Exception as e:
                print(f"Error creating trend line: {str(e)}")

            plt.xlabel('Sentiment Score (Moving Average)')
            plt.ylabel('Stock Price')
            plt.title(title)
        else:
            plt.text(0.5, 0.5, 'Insufficient data for correlation plot',
                     horizontalalignment='center', verticalalignment='center')
            plt.title(title)

        return plt.gcf()
    
    def save_plot(self, fig, filename):
        """Save plot to file"""
        try:
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            fig.savefig(filename)
        except Exception as e:
            print(f"Error saving plot: {str(e)}")
        finally:
            plt.close(fig)
