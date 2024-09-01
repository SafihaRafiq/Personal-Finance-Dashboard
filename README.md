# Personal Finance Dashboard 

The goal of this Personal Finance Dashboard is to have a better understanding of spending habits and predict future spending on a monthly basis. As a result, the aim of this spending insight is to have more realistic budgets and reduce spending where possible.

## Background Info

I have created a Python based web application dashboard on Flask to gain better insight of my spending habits. This web app is using personal spending data that I have collected for 9 months to analyze and visualize spending patterns, as well as predict future spending. This dashboard connects to a backend database in Postgres which manages historical and new inputted data. As well it predicts average spending per month, based on a time series Prophet model, which allows the user to know if their spending is getting too high.   

## How it Works 
Step 1: Create database called spending_data in Postgres 
Step 2: Run db_script.py to load data into database (csvs must be in same path). This creates the historical records database
Step 3: Run app.py and run on localhost web path to view dashboard

<img width="835" alt="Screenshot 2024-01-08 at 5 42 30 PM" src="https://github.com/rxshmi-p/PersonalFinanceDash/assets/86248667/c70d7679-8060-42ef-b7fd-5cb3a16f3a6b">


## How to Run 
1. Clone the repositiory 
```
$ git clone git@github.com:rxshmi-p/PersonalFinanceDash
$ cd Dashboard
```
2. Install dependencies:
```
$ pip install -r requirements.txt
```
3. Start the application:
```
$ flask run app.py
```

## References 

Some Python codes and project structure was inspired by the resources below: 
https://www.statsmodels.org/dev/examples/notebooks/generated/exponential_smoothing.html
https://www.bounteous.com/insights/2020/09/15/forecasting-time-series-model-using-python-part-one/

