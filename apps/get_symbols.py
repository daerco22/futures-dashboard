# %%
from .auth import client
from .clean_pairs import clean_trading_pairs

# %% GET SYMBOL FROM BINANCE
futures_exchange_info = client.futures_exchange_info()
trading_pairs = clean_trading_pairs(futures_exchange_info)
symbols = [info['Symbol']+'PERP' for info in trading_pairs]