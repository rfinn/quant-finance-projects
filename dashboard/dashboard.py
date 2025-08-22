#!/usr/bin/env python

"""
Creating a stock dashboard.  

Got the main code from chatgpt, then had to do a few hrs of debugging.
Still needs optimization, like option to enter multiple stocks.

"""

# stock_dashboard_advanced.py

import yfinance as yf
import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go

# === Helper functions for indicators ===
def calculate_indicators(df):
    # Use Adj Close if available, else fall back to Close
    if 'Adj Close' in df.columns:
        price = df['Adj Close']
    else:
        price = df['Close']
    
    df['Price'] = price

    # Moving Averages
    df['MA50'] = price.rolling(window=50, center=True).mean()
    df['MA200'] = price.rolling(window=200, center=True).mean()
    
    # Bollinger Bands (20-day)
    df['20d_ma'] = price.rolling(window=20, center=True).mean()
    df['20d_std'] = price.rolling(window=20, center=True).std()
    df['Upper'] = df['20d_ma'] + (df['20d_std'] * 2)
    df['Lower'] = df['20d_ma'] - (df['20d_std'] * 2)
    
    # Relative Strength Index (RSI, 14-day)
    delta = price.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    
    return df



# === Dash App ===
app = dash.Dash(__name__)
server = app.server

app.layout = html.Div([
    html.H1("Stock Price Analysis Dashboard", style={'textAlign': 'center'}),

    html.Div([
        html.Label("Stock ticker:"),
        dcc.Input(id='ticker-input', value='AAPL', type='text',debounce=True),   # only trigger callback when Enter is pressed or focus leaves),
    ], style={'width': '30%', 'display': 'inline-block'}),

    html.Div([
        html.Label("Select date range:"),
        dcc.DatePickerRange(
            id='date-range',
            min_date_allowed=pd.to_datetime('2010-01-01'),
            max_date_allowed=pd.to_datetime('today'),
            start_date=pd.to_datetime('2020-01-01').date(),
            end_date=pd.to_datetime('today').date(),
        )
    ], style={'width': '60%', 'display': 'inline-block', 'paddingLeft': '30px'}),

    dcc.Graph(id='price-chart'),
    dcc.Graph(id='volume-chart'),
    dcc.Graph(id='rsi-chart')
])


@app.callback(
    [Output('price-chart', 'figure'),
     Output('volume-chart', 'figure'),
     Output('rsi-chart', 'figure')],
    [Input('ticker-input', 'value'),
     Input('date-range', 'start_date'),
     Input('date-range', 'end_date')]
)
def update_charts(ticker, start_date, end_date):
    #print(f"trying to download {ticker}", start_date, end_date)
    
    try:
        #dat = yf.Ticker(ticker) # look at nvidia stock
        #df = dat.history(start=start_date, end=end_date)
        df = yf.download(ticker, start=start_date, end=end_date)
        #print(df.head)
        df = calculate_indicators(df)
        
    except Exception as e:
        print("problem downloading data")
        print(e)
        return go.Figure(), go.Figure(), go.Figure()
    print("updating charts...")
    #print(df.head)
    #################################################
    # === Price Chart with MAs + Bollinger Bands ===
    #################################################    
    price_fig = go.Figure()
    price_fig.add_trace(go.Scatter(x=df.index, y=df['Price'], mode='lines', name='Price'))
    price_fig.add_trace(go.Scatter(x=df.index, y=df['MA50'], mode='lines', name='MA50'))
    price_fig.add_trace(go.Scatter(x=df.index, y=df['MA200'], mode='lines', name='MA200'))
    price_fig.add_trace(go.Scatter(x=df.index, y=df['Upper'], mode='lines', line=dict(dash='dot'), name='Upper Band'))
    price_fig.add_trace(go.Scatter(x=df.index, y=df['Lower'], mode='lines', line=dict(dash='dot'), name='Lower Band'))
    price_fig.update_layout(title=f"{ticker} Stock Price with Indicators", xaxis_title="Date", yaxis_title="Price (USD)")

    #################################################
    # === Volume Chart ===
    #################################################    
    vol_fig = go.Figure()
    #print('First 10 values of Volume = ',df['Volume'][0:10])
    #print(df.columns)
    vol_fig.add_trace(go.Scatter(x=df.index, y=df['Volume'][ticker],name='Volume', mode='lines'))
    vol_fig.update_layout(title=f"{ticker} Trading Volume", xaxis_title="Date", yaxis_title="Volume")


    #################################################
    # === RSI Chart ===
    #################################################    
    rsi_fig = go.Figure()
    rsi_fig.add_trace(go.Scatter(x=df.index, y=df['RSI'], mode='lines', name='RSI'))
    rsi_fig.add_hline(y=70, line=dict(color='red', dash='dash'))
    rsi_fig.add_hline(y=30, line=dict(color='green', dash='dash'))
    rsi_fig.update_layout(title=f"{ticker} Relative Strength Index (RSI)", xaxis_title="Date", yaxis_title="RSI (14-day)")

    return price_fig, vol_fig, rsi_fig


if __name__ == "__main__":
    app.run(debug=True)
