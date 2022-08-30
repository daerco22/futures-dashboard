# %%
from .now_time import file_time

# %%
def setup_screener(df, setup):
	# Bull
	if setup == 'Bullish_EMA_Alignment':
		df['Bullish_EMA_Alignment'] = (df.EMA20 > df.EMA50) & (df.EMA50 > df.EMA100) & (df.RSI > 50)
		aots = df[df['Bullish_EMA_Alignment'] == True]
		return aots
	if setup == 'Consolidation_at_High':
		df['Consolidation_at_High'] = (df.EMA20 > df.EMA50) & (df.EMA50 > df.EMA100) & (df.RSI > 70) & (df.RSI < 75)
		ch = df[df['Consolidation_at_High'] == True]
		return ch
	if setup == 'Modified_Consolidation_at_High':
		df['Modified_Consolidation_at_High'] = (df.EMA20 > df.EMA50) & (df.EMA50 > df.EMA100) & (df.RSI > 75)
		modch = df[df['Modified_Consolidation_at_High'] == True]
		return modch
	# Bear
	if setup == 'Bearish_EMA_Alignment':
		df['Bearish_EMA_Alignment'] = (df.EMA20 < df.EMA50) & (df.EMA50 < df.EMA100) & (df.RSI < 50)
		iaots = df[df['Bearish_EMA_Alignment'] == True]
		return iaots
	if setup == 'Consolidation_at_Low':
		df['Consolidation_at_Low'] = (df.EMA20 < df.EMA50) & (df.EMA50 < df.EMA100) & (df.RSI < 30) & (df.RSI > 25)
		cl = df[df['Consolidation_at_Low'] == True]
		return cl
	if setup == 'Modified_Consolidation_at_Low':
		df['Modified_Consolidation_at_Low'] = (df.EMA20 < df.EMA50) & (df.EMA50 < df.EMA100) & (df.RSI < 25)
		modcl = df[df['Modified_Consolidation_at_Low'] == True]
		return modcl

def download_screener_result(setup):
	file = 'BINANCE:'+setup[['Symbol']]
	return file.to_csv(index=False).encode('utf-8')

# f'AOTS-{file_time}.csv', 

# %%
if __name__ == '__main__':
	setup_screener()
	download_screener_result()