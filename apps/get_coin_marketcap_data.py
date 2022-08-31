# %%
from bs4 import BeautifulSoup
import requests
import streamlit as st
import re

# %%
@st.cache(ttl=300)
def get_coin_mc_data():
	url = "https://coinmarketcap.com/exchanges/binance/"

	result = requests.get(url)
	doc = BeautifulSoup(result.text, "html.parser")

	market_cap = doc.find_all(text="Market Cap")
	bin_vol = doc.find(class_="priceText")
	dom = doc.find_all(text="Dominance")
	btc = doc.find("p", color="neutral5", text=re.compile("BTC$"))

	mc_parent = market_cap[0].parent
	dom_parent = dom[0].parent

	mc_a = mc_parent.find("a")
	dom_a = dom_parent.find("a")

	return mc_a.text, bin_vol.text, dom_a.text, btc.text