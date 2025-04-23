from stock_data import StockDataFetcher  # Replace with actual file/module name
import pprint

# Create instance
fetcher = StockDataFetcher()

# Test 1: Valid Stock Symbol (like Apple)
print("------ Test 1: Valid Symbol (AAPL) ------")
result = fetcher.get_StockData("AAPL")
pprint.pprint(result)

# Test 2: Valid Indian Symbol (e.g., INFY.BO for Infosys on BSE)
print("\n------ Test 2: Indian Stock Symbol (INFY.BO) ------")
result = fetcher.get_StockData("INFY.BO")
pprint.pprint(result)

# Test 3: Invalid Stock Symbol
print("\n------ Test 3: Invalid Symbol (FAKE123) ------")
result = fetcher.get_StockData("FAKE123")
pprint.pprint(result)

# Test 4: Simulate HTTPError - hard to do manually, so handled internally
# Normally this requires mocking. Skip for live testing unless API returns 429.

# You can add additional prints to inspect variables if needed
