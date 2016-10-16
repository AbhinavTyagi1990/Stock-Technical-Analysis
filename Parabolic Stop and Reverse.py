######################################################
# Stock Technical Analysis with Python               #
# Parabolic Stop and Reverse SAR(0.02,0.2)           #
######################################################

# 1. Packages and Data

# Packages Import
import numpy as np
import pandas as pd
import pandas.io.data as web
import datetime as dt
import matplotlib.pyplot as plt
import talib as ta
# Data Download
start = dt.datetime(2014, 10, 1)
end = dt.datetime(2015, 9, 30)
aapl = web.DataReader('AAPL', 'yahoo', start, end)

##########

# 2. Parabolic Stop and Reverse SAR(0.02,0.2) Calculation and Chart

# Technical Indicator Calculation
aapl['sar'] = ta.SAR(np.asarray(aapl['High']), np.asarray(aapl['Low']), acceleration=0.02, maximum=0.2)
# Technical Indicator Chart
aapl.plot(y=['Close'])
aapl.plot(y=['sar'], marker='o', linestyle='')
plt.title('Apple Close Prices & Parabolic Stop and Reverse SAR(0.02,0.2)')
plt.legend(loc='upper left')
plt.show()

##########

# 3. Stop and Reverse Trading Signals
# Previous Periods Data (avoid backtesting bias)
aapl['Close(-1)'] = aapl['Close'].shift(1)
aapl['sar(-1)'] = aapl['sar'].shift(1)
aapl['Close(-2)'] = aapl['Close'].shift(2)
aapl['sar(-2)'] = aapl['sar'].shift(2)
# Generate Trading Signals (buy=1 , sell=-1, do nothing=0)
aapl['sarsig'] = 0
sarsig = 0
for i, r in enumerate(aapl.iterrows()):
    if r[1]['Close(-2)'] < r[1]['sar(-2)'] and r[1]['Close(-1)'] > r[1]['sar(-1)']:
        sarsig = 1
    elif r[1]['Close(-2)'] > r[1]['sar(-2)'] and r[1]['Close(-1)'] < r[1]['sar(-1)']:
        sarsig = -1
    else:
        sarsig = 0
    aapl.iloc[i, 11] = sarsig
# Trading Signals Chart
plt.subplot(2, 1, 1)
plt.title('Apple Close Prices & Parabolic Stop and Reverse SAR(0.02,0.2)')
plt.gca().axes.get_xaxis().set_visible(False)
aapl.plot(y=['Close'])
aapl.plot(y=['sar'], marker='o', linestyle='')
plt.legend(loc='upper left')
plt.subplot(2, 1, 2)
aapl.plot(y=['sarsig'], marker='o', linestyle='')
plt.legend(loc='upper left')
plt.show()

##########

# 4. Stop and Reverse Trading Strategy
# Generate Trading Strategy (own stock=1 , not own stock=0, short-selling not available)
aapl['sarstr'] = 1
sarstr = 0
for i, r in enumerate(aapl.iterrows()):
    if r[1]['sarsig'] == 1:
        sarstr = 1
    elif r[1]['sarsig'] == -1:
        sarstr = 0
    else:
        sarstr = aapl['sarstr'][i-1]
    aapl.iloc[i, 12] = sarstr
# Trading Strategy Chart
plt.subplot(2, 1, 1)
plt.title('Apple Close Prices & Parabolic Stop and Reverse SAR(0.02,0.2)')
plt.gca().axes.get_xaxis().set_visible(False)
aapl.plot(y=['Close'])
aapl.plot(y=['sar'], marker='o', linestyle='')
plt.legend(loc='upper left')
plt.subplot(2, 1, 2)
aapl.plot(y=['sarstr'], marker='o', linestyle='')
plt.legend(loc='upper left')
plt.show()

##########

# 5. Stop and Reverse Strategy Performance Comparison

# 5.1. Strategies Daily Returns
# Stop and Reverse Strategy Without Trading Commissions
aapl['sardrt'] = ((aapl['Close']/aapl['Close'].shift(1))-1)*aapl['sarstr']
aapl.iloc[0, 13] = 0
# Stop and Reverse Strategy With Trading Commissions (1% Per Trade)
aapl['sarstr(-1)'] = aapl['sarstr'].shift(1)
aapl['sartc'] = aapl['sarsig']
sartc = 0
for i, r in enumerate(aapl.iterrows()):
    if (r[1]['sarsig'] == 1 or r[1]['sarsig'] == -1) and r[1]['sarstr'] != r[1]['sarstr(-1)']:
        sartc = 0.01
    else:
        sartc = 0.00
    aapl.iloc[i, 15] = sartc
aapl['sardrtc'] = (((aapl['Close']/aapl['Close'].shift(1))-1)-aapl['sartc'])*aapl['sarstr']
aapl.iloc[0, 16] = 0
# Buy and Hold Strategy
aapl['bhdrt'] = (aapl['Close']/aapl['Close'].shift(1))-1
aapl.iloc[0, 17] = 0

# 5.2. Strategies Cumulative Returns
# Cumulative Returns Calculation
aapl['sarcrt'] = np.cumprod(aapl['sardrt']+1)-1
aapl['sarcrtc'] = np.cumprod(aapl['sardrtc']+1)-1
aapl['bhcrt'] = np.cumprod(aapl['bhdrt']+1)-1
# Cumulative Returns Chart
aapl.plot(y=['sarcrt', 'sarcrtc', 'bhcrt'])
plt.title('Parabolic Stop and Reverse SAR(0.02,0.2) vs Buy & Hold')
plt.legend(loc='upper left')
plt.show()

# 5.3. Strategies Performance Metrics
# Annualized Returns
saryrt = aapl.iloc[251, 18]
saryrtc = aapl.iloc[251, 19]
bhyrt = aapl.iloc[251, 20]
# Annualized Standard Deviation
sarstd = np.std(aapl['sardrt'])*np.sqrt(252)
sarstdc = np.std(aapl['sardrtc'])*np.sqrt(252)
bhstd = np.std(aapl['bhdrt'])*np.sqrt(252)
# Annualized Sharpe Ratio
sarsr = saryrt/sarstd
sarsrc = saryrtc/sarstdc
bhsr = bhyrt/bhstd
# Summary Results Data Table
data = [{'0': '', '1': 'SAR(0.02,0.2)', '2': 'SAR(0.02,0.2)TC', '3': 'B&H'},
        {'0': 'Annualized Return', '1': saryrt, '2': saryrtc, '3': bhyrt},
        {'0': 'Annualized Standard Deviation', '1': sarstd, '2': sarstdc, '3': bhstd},
        {'0': 'Annualized Sharpe Ratio (Rf=0%)', '1': sarsr, '2': sarsrc, '3': bhsr}]
table = pd.DataFrame(data)
print(aapl)
print(table)
