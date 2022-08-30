# %%
from datetime import datetime

# %% DATETIME
now = datetime.now()
data_time = now.strftime('%d-%m-%y-%H:%M')
web_time = now.strftime('%A, %B %d, %Y')
file_time = now.strftime('%d-%m-%y-%H-%M')