# %% 
import os
from dotenv import load_dotenv
from binance.client import Client
import streamlit as st

# %% LOAD CLIENT
load_dotenv()
api_key = os.environ.get('api_key')
api_secret = os.environ.get('api_secret')
client = Client(api_key, api_secret)
