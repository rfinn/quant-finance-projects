# Goal

* The goal is to create a dashboard to view a stock's performance over time.




# Usage
In a terminal, type:

```
python ./dashboard.py
```
Then open a web browser and type `http://127.0.0.1:8050/` in the url address.

# Overview
* A `plotly` interactive plot will appear.
* The user can change the stock, start date, and end date.

# Modules
```
import yfinance as yf
import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
```
# Authors
* the code was created by chatgpt.
* significant debugging by R. Finn
