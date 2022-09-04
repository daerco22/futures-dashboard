# %%
from tradingview_ta import *
from .now_time import data_time
from .rank import percent_rank
import streamlit as st

@st.cache(ttl=3600)
def get_data(future_symbols):
	analysis_results = []
	column_name = ['Date-Time', 'Symbol', 'Close', '52wkHigh', '52wkLow', 'ATH', 'ATL', 'RSI', 'EMA20', 'EMA50', 'EMA100', 'change', 'volume']
	for i in future_symbols:
		coin = TA_Handler(
			symbol=i,
			screener = 'crypto',
			exchange = 'BINANCE',
			interval=Interval.INTERVAL_1_DAY,
			timeout=5
		)
		coin.add_indicators([
			'price_52_week_high',
			'price_52_week_low',
			'High.All',
			'Low.All'          
		])
		analysis = coin.get_analysis()
		results = {
			column_name[0]: data_time, 
			column_name[1]: analysis.symbol, 
			column_name[2]: analysis.indicators['close'], 
			column_name[3]: analysis.indicators['price_52_week_high'],
			column_name[4]: analysis.indicators['price_52_week_low'],
			column_name[5]: analysis.indicators['High.All'], 
			column_name[6]: analysis.indicators['Low.All'], 
			column_name[7]: analysis.indicators['RSI'],
			column_name[8]: analysis.indicators['EMA20'],
			column_name[9]: analysis.indicators['EMA50'],
			column_name[10]: analysis.indicators['EMA100'],
			column_name[11]: analysis.indicators['change'],
			column_name[12]: analysis.indicators['volume']
		}
		analysis_results.append(results)

	for r in analysis_results:
		h_wk52 = r['52wkHigh']
		l_wk52 = r['52wkLow']
		a_high = r['ATH']
		a_low = r['ATL']
		cl = r['Close']
		if h_wk52 is not None:
			hl_rank = percent_rank([h_wk52, l_wk52], cl)
		else:
			hl_rank = percent_rank([a_high, a_low], cl)
		r['52wkRange'] = hl_rank
	
	for c in analysis_results:
		round_change = round(c['change'], 2)
		volume = round(c['volume'], 2)
		c['change'] = round_change
		c['volume'] = volume
	return analysis_results

# %%
if __name__ == '__main__':
    get_data()