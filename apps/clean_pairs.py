# %% CLEAN TICKERS FROM BINANCE
def clean_trading_pairs(futures_info):
    trading_pairs = []
    unwanted_symbols = {'BTCSTUSDT', 'BTCUSDT_220930', 'ETHUSDT_220930', 'INJUSDT', 'STGUSDT'}
    valid_busd = {'TRBUSDT'}
    column_name = ['Symbol', 'Type', 'Subtype']
    for info in futures_info['symbols']:
        pair = {
            column_name[0]: info['symbol'],
            column_name[1]: info['underlyingType'],
            column_name[2]: info['underlyingSubType']
        }
        if pair['Symbol'] not in unwanted_symbols:
            if pair['Symbol'].endswith('USDT'):
                trading_pairs.append(pair)
    return trading_pairs

# %%
if __name__ == '__main__':
    clean_trading_pairs()