# %% 
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from prophet import Prophet
import warnings
from prophet.plot import add_changepoints_to_plot
warnings.filterwarnings("ignore")

import db_script as db

# %% Read table from database
table = db.read_fulltable('postgres', 'localhost', 'spending_db')

# %%
df = pd.DataFrame(table, columns =['index','Date', 'Description', 'Type','Amount_Spent', 'Credit/Debit'])
df = df.iloc[:,1:]
df.set_index('Date', inplace=True)
df.sort_index(inplace=True)

# %% Inital Plot 
plt.plot(df.index, df['Amount_Spent'])
plt.xlabel('Date')
plt.ylabel('Amount Spent')
plt.title('Spending Over Time')

# %% 
monthly_aggregated = df.resample('M').sum().reset_index()

plt.plot(monthly_aggregated['Date'], monthly_aggregated['Amount_Spent'])

# %% Prophet Model 
monthly_aggregated['ds'] = pd.to_datetime(monthly_aggregated['Date'])
monthly_aggregated['y'] = monthly_aggregated['Amount_Spent'].astype(float)

# %% 
m = Prophet() #default trend= piece-wise linear models
            # default include weekly and yearly seasonalities 

#m.add_seasonality(name='monthly', period=30.5, fourier_order=10)
#Fit with default settings
m.fit(monthly_aggregated)
#Dataframe with forecasting steps
future = m.make_future_dataframe(periods=1)
#Forecast
forecast = m.predict(future)
forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()
fig = m.plot(forecast)
a = add_changepoints_to_plot(fig.gca(), m, forecast)

fig1 = m.plot(forecast)

fig2 = m.plot_components(forecast)

exp_spending = forecast[-1:]['yhat']
 

# %% plots 

# fig1 = m.plot(forecast)

# fig2 = m.plot_components(forecast)
# # %% Expected spending this month 
# exp = forecast[-1:]['yhat']

# # %%
