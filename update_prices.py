from lib import symbols, price_apis, constants as C

import pandas as pd
import numpy as np


print('Starting to update prices')


# Load Last Price File
price_prev_df = pd.read_csv(C.PRICE_FILE)


# Read new price data
price_new_df = pd.concat([
    price_apis.crypto_compare(symbols.RH_CRYPTO, C.CRYPTO),
    price_apis.alpha_vantage(symbols.RH_ETF, C.ETF),
    price_apis.alpha_vantage(symbols.NASDAQ + symbols.SNP, C.STOCK),
]).reset_index(drop=True)


# Create Todays Price DF
prices_merged = \
    price_new_df\
        .merge(
            price_prev_df.drop(C.RETURN, axis=1),
            on=[C.SYMBOL, C.TYPE],
            how='left',
            suffixes=['', '_old']
        ).sort_values(by=C.SYMBOL).reset_index(drop=True)


# Calculate Return
prices_merged[C.RETURN] = prices_merged[C.PRICE] / prices_merged[C.PRICE + '_old'] - 1
prices_merged[C.RETURN] = prices_merged[C.RETURN].replace([np.inf, -np.inf], np.nan).fillna(0.0)
prices_merged.drop(C.PRICE + '_old', axis=1, inplace=True)


# Save New Price File
prices_merged\
    [[C.SYMBOL, C.TYPE, C.PRICE, C.RETURN]]\
    .to_csv(C.PRICE_FILE, index=False)


print('Done!')
