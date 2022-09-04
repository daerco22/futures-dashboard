# %%
import yaml
import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd
import plotly.express as px

from apps import setup_screener, download_screener_result, get_data, symbols, web_time, file_time, get_coin_mc_data, url

# %%
st.set_page_config(page_title='Screener | BPF', page_icon=':cyclone:', layout='wide')

# %% USER AUTHENTICATION
with open('config.yaml') as file:
    config = yaml.load(file, Loader=yaml.SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status == False:
    st.error("Username/password is incorrect")

if authentication_status == None:
    st.warning("Please enter your username and password")


# %%
if authentication_status:
	st.title('Screener :game_die:')
	mc, dom, ex_name, ex_vol = get_coin_mc_data(url)
	col1, col2, col3 = st.columns([4,4,4])
	col1.write(':rocket: Crypto Total Market Cap')
	col1.markdown(f'<font color=DeepSkyBlue>{mc}</font>', unsafe_allow_html=True)
	col2.write(':signal_strength: BTC and ETH Dominance')
	col2.markdown(f'<font color=DeepSkyBlue>{dom}</font>', unsafe_allow_html=True)
	col3.write(f':moneybag: {ex_name} 24h Vol')
	col3.markdown(f'<font color=DeepSkyBlue>{ex_vol}</font>', unsafe_allow_html=True)
	#col4.metric(label='', value='', delta=btc, delta_color="off")
	#col4.write(':large_orange_diamond: Binance BTC')
	st.write('---')
	with st.expander('Technical Indicators'):
		st.write("""
			What is EMA?
			\n- Exponential Moving Average (EMA) is a type of weighted moving average (WMA) that gives more weighting or importance to recent price data.
		""")
		st.write("###")
		st.write("""
			What is RSI?
			\n- The Relative Strength Index (RSI), is a momentum oscillator that measures the speed and change of price movements. 
			The RSI oscillates between zero and 100. Traditionally the RSI is considered overbought when above 70 and oversold when below 30.
		""")
		st.write("###")

	# %%
	option = st.selectbox(
		'Trading Setup:',
		('Bullish EMA Alignment', 'Consolidation at High', 'Modified Consolidation at High', 'Bearish EMA Alignment', 'Consolidation at Low', 'Modified Consolidation at Low'))

	# %%
	with st.container():
		if st.button('Get Data'):
			a_result = get_data(symbols)
			df = pd.DataFrame(a_result)
			
			if option == 'Bullish EMA Alignment':
				setup = setup_screener(df, 'Bullish_EMA_Alignment')
			if option == 'Consolidation at High':
				setup = setup_screener(df, 'Consolidation_at_High')
			if option == 'Modified Consolidation at High':
				setup = setup_screener(df, 'Modified_Consolidation_at_High')
			if option == 'Bearish EMA Alignment':
				setup = setup_screener(df, 'Bearish_EMA_Alignment')
			if option == 'Consolidation at Low':
				setup = setup_screener(df, 'Consolidation_at_Low')
			if option == 'Modified Consolidation at Low':
				setup = setup_screener(df, 'Modified_Consolidation_at_Low')

			fig = px.scatter(setup, x='RSI', y='52wkRange', range_x=[0, 100], color='Symbol', labels={'RSI': 'RSI Levels', '52wkRange': '52-Week Range'}, hover_data=['Symbol'], title=f'{web_time}')
			fig.update_layout(plot_bgcolor='#0e1117', paper_bgcolor='#0e1117', title_font_color='white', font_color='white')
			fig.add_hline(y=0.5, line_color='green', opacity=0.50)
			fig.add_vline(x=50, line_color='green', opacity=0.50)
			fig.update_xaxes(showgrid=False, zeroline=False, mirror=True, ticks='outside', showline=True)
			fig.update_yaxes(showgrid=False, zeroline=False, mirror=True, ticks='outside', showline=True)
			fig.add_shape(type='rect', x0=60, y0=0.6, x1=70, y1=1, line=dict(color='LightSeaGreen', width=1,), fillcolor='PaleTurquoise', opacity=0.3)
			fig.add_shape(type='rect', x0=30, y0=0.0, x1=40, y1=0.4, line=dict(color='Crimson', width=1,), fillcolor='LightPink', opacity=0.3)

			left_column, right_column = st.columns(2)
			with left_column:
				st.header('RSI Levels vs 52-Week Range :zap:')
				st.plotly_chart(fig, use_container_width=True)
			with right_column:
				if option == 'Bullish EMA Alignment':
					st.header('Bullish EMA Alignment Filter :dart:')
					st.write("""
						\n- EMA20 is above EMA50
						\n- EMA50 is above EMA100
						\n- RSI14 is above 50
					""")
					st.write("###")
					st.warning('The page will reset once the Download List button was click.')
					setup_data = download_screener_result(setup)
					st.download_button(
						label="Download List",
						data=setup_data,
						file_name=f'{option}-{file_time}.csv',
						mime='text/csv',
					)
				if option == 'Consolidation at High':
					st.header('Consolidation at High Filter :dart:')
					st.write("""
						\n- EMA20 is above EMA50
						\n- EMA50 is above EMA100
						\n- RSI14 is above 70 but below 75
					""")
					st.write("###")
					st.warning('The page will reset once the Download List button was click.')
					setup_data = download_screener_result(setup)
					st.download_button(
						label="Download List",
						data=setup_data,
						file_name=f'{option}-{file_time}.csv',
						mime='text/csv',
					)				
				if option == 'Modified Consolidation at High':
					st.header('Modified Consolidation at High Filter :dart:')
					st.write("""
						\n- EMA20 is above EMA50
						\n- EMA50 is above EMA100
						\n- RSI14 is above 75
					""")
					st.write("###")
					st.warning('The page will reset once the Download List button was click.')
					setup_data = download_screener_result(setup)
					st.download_button(
						label="Download List",
						data=setup_data,
						file_name=f'{option}-{file_time}.csv',
						mime='text/csv',
					)
				if option == 'Bearish EMA Alignment':
					st.header('Bearish EMA Alignment Filter :dart:')
					st.write("""
						\n- EMA20 is below EMA50
						\n- EMA50 is below EMA100
						\n- RSI14 is below 50
					""")
					st.write("###")
					st.warning('The page will reset once the Download List button was click.')
					setup_data = download_screener_result(setup)
					st.download_button(
						label="Download List",
						data=setup_data,
						file_name=f'{option}-{file_time}.csv',
						mime='text/csv',
					)
				if option == 'Consolidation at Low':
					st.header('Consolidation at Low Filter :dart:')
					st.write("""
						\n- EMA20 is below EMA50
						\n- EMA50 is below EMA100
						\n- RSI14 is below 30 but above 25
					""")
					st.write("###")
					st.warning('The page will reset once the Download List button was click.')
					setup_data = download_screener_result(setup)
					st.download_button(
						label="Download List",
						data=setup_data,
						file_name=f'{option}-{file_time}.csv',
						mime='text/csv',
					)
				if option == 'Modified Consolidation at Low':
					st.header('Modified Consolidation at Low Filter :dart:')
					st.write("""
						\n- EMA20 is below EMA50
						\n- EMA50 is below EMA100
						\n- RSI14 is below 25
					""")
					st.write("###")
					st.warning('The page will reset once the Download List button was click.')
					setup_data = download_screener_result(setup)
					st.download_button(
						label="Download List",
						data=setup_data,
						file_name=f'{option}-{file_time}.csv',
						mime='text/csv',
					)

			st.dataframe(setup)

			with st.sidebar:
				st.subheader('Trading Setups:')
				st.write(
					"""
					- Bullish EMA Alignment
					- Consolidation at High
					- Modified Consolidation at High
					- Bearish EMA Alignment
					- Consolidation at Low
					- Modified Consolidation at Low
					""")
				st.info(
					'''
					Download List button: Download a csv file that you can import to TradingView.
					''')
	authenticator.logout("Logout", "sidebar")

	st.write('---')
	buy_me_a_coffee = '<a href="https://www.buymeacoffee.com/greaterthantrde" target="_blank"><b>:coffee: Buy me a coffee :question:</b></a>'
	st.markdown(buy_me_a_coffee, unsafe_allow_html=True)

# %%
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)