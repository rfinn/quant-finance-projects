# Goal

* The goal is to create a dashboard to view a stock's performance over time.


# Overview
* A `plotly` interactive plot will appear in a web browser window.
  * price vs time
  * volume vs time
  * relative strength index vs time
* The user can change the stock, start date, and end date.


# Usage
In a terminal, type:

```
python ./dashboard.py
```
Then open a web browser and type `http://127.0.0.1:8050/` in the url address.

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

# TODO
* check statistics
* add option to compare multiple stocks
