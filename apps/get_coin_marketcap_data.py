# %%
from bs4 import BeautifulSoup
import requests
import streamlit as st

url = "https://coinmarketcap.com/rankings/exchanges/derivatives/"

# %%
@st.cache(ttl=300)
def get_coin_mc_data(url):
	result = requests.get(url)
	doc = BeautifulSoup(result.text, "html.parser")
	
	market_cap = doc.find_all(text="Market Cap")
	dom = doc.find_all(text="Dominance")
	mc_parent = market_cap[0].parent
	dom_parent = dom[0].parent
	mc_a = mc_parent.find("a")
	dom_a = dom_parent.find("a")

	table = doc.find('table', class_='cmc-table')
	tr = table.tbody.find('tr')
	name = tr.find('p', text='Binance')
	td = tr.find('td', style='text-align:end')
	div = td.find('div')
	vol_24hr = td.text.replace(div.text, "")

	return mc_a.text, dom_a.text, name.text, vol_24hr
