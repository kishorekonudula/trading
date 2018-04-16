from lib import constants as C

import pandas as pd


print('Starting Sell Recommender\n')


# Load Prices and Holdings
price_df = pd.read_csv(C.PRICE_FILE)
holding_df = pd.read_csv(C.HOLDINGS_FILE)


# Merge current price on owned holdings
holdings_merged = \
    holding_df\
        [holding_df[C.STATUS] == C.HELD]\
        .merge(
            price_df,
            on=[C.SYMBOL, C.TYPE],
            how='left'
        )


# Calculate Returns on Each Holding
holdings_merged[C.RETURN] = \
    holdings_merged[C.PRICE] / holdings_merged[C.PRICE_PAID] - 1


# Save Sorted Holdings
holdings_merged\
    [[
        C.DATE_PURCH, C.SYMBOL, C.TYPE, C.UNITS, C.PRICE_PAID, C.PRICE, C.RETURN, 
    ]]\
    .sort_values(by=C.RETURN)\
    .to_csv(C.SELL_FILE, index=False)


print('Done!')
