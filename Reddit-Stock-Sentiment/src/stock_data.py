import yfinance as yf
import time
from requests.exceptions import HTTPError

class StockDataFetcher:
    def get_StockData(self,stock_symbol,max_retries=3,retry_delay=5):
        for attempt in range(max_retries) :
            try :
                if attempt > 0:
                    time.sleep(retry_delay)
                stock= yf.Ticker(stock_symbol)
                try:
                    stock_info = stock.info  # <— safer to isolate this in try
                    if not isinstance(stock_info, dict):
                        raise ValueError(f"No valid info returned for {stock_symbol}")
                    current_price = stock.info.get('currentPrice')
                    if current_price is None:
                        raise ValueError(f"Data not found {stock_symbol}")
                    return {
                        'success':True,
                        'data': {
                            'current_price': current_price,
                            'currency': stock.info.get('currency','INR')
                        }
                    }
                    
                except HTTPError as e :
                    if e.response.status_code == 429:
                        print("max trials limit hit")
                        if attempt == max_retries -1:
                            raise ValueError("PLease try later")
                        continue
                    raise
                
            except Exception as e:
                print(f"error fetching data {str(e)}")
                if attempt == max_retries -1:
                    return {
                        'success' : False,
                        'error' : f"Failed to get data of {stock_symbol} : {str(e)}"
                    }
                continue    
            