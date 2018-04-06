import sys

from lib import constants as C

import pandas as pd
import numpy as np


print('Start Buying Recommender\n')


# Load Prices and Holdings
price_df = pd.read_csv(C.PRICE_FILE)
holding_df = pd.read_csv(C.HOLDINGS_FILE)


# Read in budget
try:
    budget = float(sys.argv[1])
except:
    raise Exception('Need to pass in a budget!')


# Get Holding Counts
holding_counts = \
    holding_df\
        .groupby([C.SYMBOL, C.TYPE])\
        .agg({ C.DATE_PURCH: 'count' })\
        .reset_index()\
        .rename(columns={ C.DATE_PURCH: C.N_HOLDINGS })


# Combine with Prices
price_constrained = [C.STOCK, C.ETF] # Check if ETF and Crypto belong here
buy_merged = \
    price_df\
        [
            (
                (price_df[C.TYPE].isin(price_constrained)) &
                (price_df[C.PRICE] > C.LOW_STOCK_PRICE) & 
                (price_df[C.PRICE] <= budget)
            ) | (
                (~price_df[C.TYPE].isin(price_constrained))
            )
        ]\
        .merge(
            holding_counts,
            on=[C.SYMBOL, C.TYPE],
            how='left'
        ).fillna(0)

# Only buy when returns drop
buy_merged = buy_merged[buy_merged[C.RETURN] < 0]

buy_merged[C.PROBABILITY] = -buy_merged[C.RETURN] / (1 + buy_merged[C.N_HOLDINGS])
buy_merged[C.PROBABILITY].replace([np.inf, -np.inf], np.nan, inplace=True)
buy_merged[C.PROBABILITY].fillna(0.0, inplace=True)
buy_merged = buy_merged[buy_merged[C.PROBABILITY] > 0]

buy_merged[C.PROBABILITY] = buy_merged[C.PROBABILITY] / buy_merged[C.PROBABILITY].sum()


# Randomly Select Symbols proportional to their probability
choices = \
    np.random.choice(
        buy_merged[C.SYMBOL] + '_' + buy_merged[C.TYPE],
        p=buy_merged[C.PROBABILITY],
        size=len(buy_merged),
        replace=False
    )


# Put Choices into a dataframe
choice_syms, choice_types = list(zip(*map(lambda x: x.split('_'), choices.tolist())))
choices_df = \
    pd.DataFrame({
        C.SYMBOL: choice_syms,
        C.TYPE: choice_types
    })\
    .reset_index()\
    .rename(columns={ 'index': C.CHOICE_ORDER })


# Combine random choices with buy_merged and order by choice order
choices_merged = \
    buy_merged\
        .merge(
            choices_df,
            on=[C.SYMBOL, C.TYPE],
            how='inner'
        )\
        .sort_values(by=C.CHOICE_ORDER)


# Save Buy Recommendations
choices_merged.to_csv(C.BUY_FILE, index=False)


print('Done!')
