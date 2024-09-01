# %%
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime as dt
import streamlit as st
import plotly.graph_objects as go


# %%
# Page Configuration 
st.set_page_config(
    page_title = 'Financial Dashboard',
    layout = 'wide'
)

st.title('Financial Dashboard')
st.sidebar.success('Selection Panel')

# %%
### Importing Data
# must update total months and new dataset name 
names = ["Sept 2021.csv", 'Oct 2021.csv', 'Nov 2021.csv', 'Dec 2021.csv', 'Jan 2022.csv', 'Feb 2022.csv', 'March 2022.csv',
         'April 2022.csv']
path = '.../Projects/Budget files/Monthly Budget  - '

monthly  = []
for i in range(0,len(names)):
    monthly.append(pd.read_csv(path + names[i]))

#%%
### Cleaning Dataframes 

# drop unnecessary columns
cols = [1,5,6,7,8,9]
for dataset in monthly:
    dataset.drop(dataset.columns[cols], axis=1, inplace = True)
    dataset.dropna(inplace = True)

# %% 
# reformat date column to date datatype
months = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'June': 6, 'July': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}
year=0
for df in monthly:
    year+=1
    for i in range(0,len(df['Date '])):
        day=list(df['Date '].iloc[i].split('-'))
        for month,val in months.items():
            if month == day[1]:
                df['Date '].iloc[i] = day[0]+"/"+str(val)+"/"+names[year-1][-6:-4]


# %%
### Combine monthly datasets, convert to datetime, set date as index 
res = pd.concat(monthly)
res['Date ']= pd.to_datetime(res['Date '])
df = res.copy()
res = res.set_index('Date ').sort_index()
res = res.loc['2021-08-01':'2022-06-01']

if st.checkbox('Show model data'):
    st.subheader('Model data')
    st.write(res)

# %% 
# Plots  
st.subheader('Summary Plots')

col1, col2 = st.columns(2)

with col1:
    st.subheader("Total Amount Spent Over Time")
    st.line_chart(res['Amount Spent '], use_container_width=True)

with col2:
    st.header("Total Spending by Type")
    ty_plot = res['Type'].value_counts()
    st.bar_chart(ty_plot)


# %% 
### Selecting time period for monthly aggregation and reducing dataframe to df to prepare for time series model
spent_by_month = res['2021-07-01':'2022-05-30'].resample('M').sum()

# %%

df2 = df.groupby(['Date ','Type'], as_index=False)['Amount Spent '].sum()
df2.groupby([df2['Date '].dt.to_period('M'), 'Type']).sum().reset_index()

st.subheader("Spending Type Comparison")
clist = df2["Type"].unique().tolist()
types = st.multiselect("Select the types of spending you would like to compare", clist)
st.header("You selected: {}".format(", ".join(types)))      

dfs = {type: df2[df2["Type"] == type] for type in types}

fig = go.Figure()
for type, df2 in dfs.items():
    fig = fig.add_trace(go.Scatter(x=df2["Date "], y=df2["Amount Spent "], name=type))

st.plotly_chart(fig, use_container_width=True)

# graphs to show seasonal_decompose
# Examined model for patterns:
# Level (avg value in series) - increases and then drops  after a peak, seen pattern twice
# Trend (increases, decreases, stays same over time)
# Seasonal/Periodic
# Cyclical (increase/decrease non-seasonal related, like business cycles)
# Random/Irregular variations
