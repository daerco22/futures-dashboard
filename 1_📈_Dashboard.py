# %%
import yaml
import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd
import plotly.express as px

from apps import get_data, symbols, trading_pairs, web_time, generate_excel_download_link, generate_html_download_link, get_coin_mc_data, url

# %%
st.set_page_config(page_title='Dashboard | BPF', page_icon=':cyclone:', layout='wide')

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
	st.title('Dashboard :chart_with_upwards_trend:')
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
	with st.expander(' Binance Perpetual Futures Momentum Scanner'):
		st.write("""
			What Are Perpetual Futures?
			\n- Perpetual Futures Contracts, as the name suggests, do not have an expiration date. Therefore, traders do not need to keep track of various delivery months, 
			unlike quarterly futures contracts. For instance, a trader can keep a short position to perpetuity, unless he gets liquidated.
		""")
		st.write("###")
		st.write("""
			What is RSI?
			\n- The Relative Strength Index (RSI), is a momentum oscillator that measures the speed and change of price movements. 
			The RSI oscillates between zero and 100. Traditionally the RSI is considered overbought when above 70 and oversold when below 30.
		""")
		st.write("###")
		st.write("""
			What does 52 week high/low indicate?
			\n- If you ever look for a particular coin's performance in the last one year, the lowest price that the coin hits is called the 52-week low, 
			while the highest price the coin hits is called the 52-week high.
		""")
		st.write("###")

	with st.container():
		if st.button('Get Data'):
			a_result = get_data(symbols)
			df = pd.DataFrame(a_result)
			type = [info['Type'] for info in trading_pairs]
			subtype = [info['Subtype'] for info in trading_pairs]
			subtypes = []
			for sublist in subtype: 
				for val in sublist: 
					subtypes.append(val)                
			df['Types'] = type
			df['Subtypes'] = subtypes
			fig = px.scatter(df, x='RSI', y='52wkRange', range_x=[0, 100], color='Subtypes', labels={'RSI': 'RSI Levels', '52wkRange': '52-Week Range'}, hover_data=['Symbol'], title=f'{web_time}')
			fig.update_layout(plot_bgcolor='#0e1117', paper_bgcolor='#0e1117', title_font_color='white', font_color='white')
			fig.add_hline(y=0.5, line_color='green', opacity=0.50)
			fig.add_vline(x=50, line_color='green', opacity=0.50)
			fig.update_xaxes(showgrid=False, zeroline=False, mirror=True, ticks='outside', showline=True)
			fig.update_yaxes(showgrid=False, zeroline=False, mirror=True, ticks='outside', showline=True)
			fig.add_shape(type='rect', x0=60, y0=0.6, x1=70, y1=1, line=dict(color='LightSeaGreen', width=1,), fillcolor='PaleTurquoise', opacity=0.3)
			fig.add_shape(type='rect', x0=30, y0=0.0, x1=40, y1=0.4, line=dict(color='Crimson', width=1,), fillcolor='LightPink', opacity=0.3)

			df1 = df[['RSI']]
			df2 = df[['Symbol','RSI']]
			fig1 = px.histogram(df1, x='RSI', text_auto=True, labels={'RSI': 'RSI Levels', 'count': 'RSI Count'}, title=f'{web_time}')
			fig1.update_layout(plot_bgcolor='#0e1117', bargap=0.2, paper_bgcolor='#0e1117', title_font_color='white', font_color='white')
			fig1.update_xaxes(showgrid=False, zeroline=False, mirror=True, ticks='outside', showline=True)
			fig1.update_yaxes(showgrid=False, zeroline=False, mirror=True, ticks='outside', showline=True)

			left_column, right_column = st.columns(2)
			with left_column:
				st.header('RSI Levels vs 52-Week Range :zap:')
				st.plotly_chart(fig, use_container_width=True)
			with right_column:
				st.header('RSI Distribution :bar_chart:')
				st.plotly_chart(fig1, use_container_width=True)

			with st.sidebar:
				st.subheader('How to read Binance Perpetual Futures Momentum Scanner:')
				st.write(
					'''
					- Scanner ONLY includes coins that are in Binance and has USDTPERP in their name
					- This plots the coins RSI Level against its 52-week Range
					- The upper right quadrant shows the Leaders while the lower left quadrant shows the Laggards
					- RSI Distribution shows the number of coins within a specified RSI Range
					- This helps us identify where majority of the coins are
					''')
				st.header('Downloads:')
				st.subheader('RSI Levels vs 52-Week Range Daily Data')
				generate_excel_download_link(df, 'RSI Levels vs 52-Week Range')
				generate_html_download_link(fig, 'RSI Levels vs 52-Week Range Daily')
				st.subheader('RSI Distribution Daily Data')
				generate_excel_download_link(df2, 'RSI Distribution Daily')
				generate_html_download_link(fig1, 'RSI Distribution Daily')
				st.info(
					'''
					Reminder: Always Download the Excel file and Plot html file.
					Once you click on a different page or after a certain period of time, the page will be reset.
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