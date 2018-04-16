import os

# Header Names
SYMBOL = 'Symbol'
TYPE = 'Type'
PRICE = 'Price'
RETURN = 'Return'
STATUS = 'Status'
PRICE_PAID = 'PricePaid'
UNITS = 'Units'
DATE_PURCH = 'DatePurchased'
N_HOLDINGS = 'N_Holdings'
PROBABILITY = 'Probability'
CHOICE_ORDER = 'ChoiceOrder'

# Holding Statuses
HELD = 'Held'
BUYING = 'Buying'
SELLING = 'Selling'

# Holding Types
STOCK = 'Stock'
ETF = 'ETF'
CRYPTO = 'Crypto'

# Alpha Vantage Configuration
AV_KEY = '15LQTAQTPS4DIS9G'
AV_SLEEP = 2

# Paths
DATA_DIR = 'data'
PRICE_FILE = os.path.join(os.path.dirname(__file__), os.pardir, DATA_DIR, 'price.csv')
HOLDINGS_FILE = os.path.join(os.path.dirname(__file__), os.pardir, DATA_DIR, 'holdings.csv')
SELL_FILE = os.path.join(os.path.dirname(__file__), os.pardir, DATA_DIR, 'sell.csv')
BUY_FILE = os.path.join(os.path.dirname(__file__), os.pardir, DATA_DIR, 'buy.csv')

# Http
HTTP_RETRIES = 15
HTTP_SLEEP = 1

# RobinHood
LOW_STOCK_PRICE = 5.0
