#Black Scholes Pricing model; python repl application, takes in 5 inputs to an option prices; 1 volatility 2 stock price; Current Asset Prices
# 3 strike price 4 time to maturity (Years) 5 Risk free interest rate 
# -> spits out both a call and a put value.
#Add an interacive GUI layer, use streamlit ; spit out heatmap , call / put price given the inputs 
# then add heatmap parameters such as min/max spot price and min / max volatility for heatmap 
#green values reflect higher numbers, red values reflect lower numbers 
# add a purchase price for the call and purchase price for the put ; then you will have a PnL for the call/ put 
# then you can have a heatmap displaying the pnL of the call / put given the inputs and the purchase prices, green for +ve PnL and red for -ve Pnl

import math
import numpy as np
import streamlit as st
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import norm

#Definition of Options Class
class Option: 
    def __init__(
        self,  #all parameters should be floats 
        Volatility,
        StockPrice,
        StrikePrice,
        TimeToMaturity,
        InterestRate
    ):
        self.Volatility = Volatility
        self.StockPrice = StockPrice
        self.StrikePrice = StrikePrice
        self.TimeToMaturity = TimeToMaturity
        self.InterestRate = InterestRate

    def pricing(self):
        d1 = (math.log(self.StockPrice / self.StrikePrice) + (self.InterestRate + ((self.Volatility ** 2) / 2)) * self.TimeToMaturity) / (self.Volatility * math.sqrt(self.TimeToMaturity))
        d2 = d1 - self.Volatility * math.sqrt(self.TimeToMaturity)
        CallPrice = (norm.cdf(d1) * self.StockPrice) - (norm.cdf(d2) * self.StrikePrice * math.exp(-self.InterestRate * self.TimeToMaturity))
        PutPrice = (self.StrikePrice * math.exp(-self.InterestRate * self.TimeToMaturity) * norm.cdf(-d2)) - (self.StockPrice * norm.cdf(-d1))
        return CallPrice, PutPrice 

#option = Option(Volatility=0.2, StockPrice=100, StrikePrice=105, TimeToMaturity=1, InterestRate=0.05)
#call, put = option.pricing()
#print(f"Call Option Price: {call}")
#print(f"Put Option Price: {put}")

def create_heatmaps(min_spot, max_spot, min_vol, max_vol, strike, time, rate, call, put):
    #spot_prices = np.linspace(min_spot, max_spot, 100)
    #vol_range = np.linspace(min_vol, max_vol, 100)
    call_prices = np.zeros((len(vol_range), len(spot_prices)))
    put_prices = np.zeros((len(vol_range), len(spot_prices)))
    pnl_call = np.zeros((len(vol_range), len(spot_prices)))
    pnl_put = np.zeros((len(vol_range), len(spot_prices)))

    for i, vol in enumerate(vol_range):
        for j, spot in enumerate(spot_prices):
            option = Option(Volatility=vol, StockPrice=spot, StrikePrice=strike, TimeToMaturity=time, InterestRate=rate)
            call_price, put_price = option.pricing()
            call_prices[i, j] = call_price
            put_prices[i, j] = put_price
            pnl_call[i, j] = call_price - call
            pnl_put[i, j] = put_price - put

    return spot_prices, vol_range, call_prices, put_prices, pnl_call, pnl_put

#establish side GUI and st title
st.title("Nico's Options Pricer with HeatMap")
st.info("+ve P&L vs -ve PNL display")

with st.sidebar:
    st.title("Options Pricing Parameter Sliders")
    curr = st.number_input("Current Asset Price", value=100)
    strike = st.number_input("Strike Price", value=100)
    time = st.number_input("Time to Maturity (Years)", value=1.0)
    rate = st.number_input("Risk-free Interest Rate", value=0.05)
    volatility = st.number_input("Volatility (σ)", value=0.2)

    min_spot = st.number_input("Min Spot Price", min_value=0.01,  value=curr * 0.8, step=0.1)
    max_spot = st.number_input("Max Spot Price", min_value=0.01, value=curr * 1.2, step =0.1)
    min_vol = st.slider("Min Volatility", min_value=0.01, max_value=1.0, value=volatility*0.5, step=0.01)
    max_vol = st.slider("Max Volatility", min_value=0.01, max_value=1.0, value=volatility*1.5, step=0.01)
    call = st.number_input("Call Option Purchase Price", min_value=0.0, value=20.0)
    put = st.number_input("Put Option Purchase Price", min_value=0.0, value=20.0)
    spot_prices = np.linspace(min_spot, max_spot, 10)
    vol_range = np.linspace(min_vol, max_vol, 10)

spot_prices, vol_range, call_prices, put_prices, pnl_call, pnl_put = create_heatmaps(min_spot, max_spot, min_vol, max_vol, strike, time, rate, call, put)


st.subheader("Call Option Price Heatmap")
fig, ax = plt.subplots(figsize=(10,8))
sns.heatmap(call_prices, cmap='RdYlGn', xticklabels=np.round(spot_prices, 2), yticklabels=np.round(vol_range, 2), annot=True, fmt=".2f", ax=ax)
ax.set_xlabel('Spot Price')
ax.set_ylabel('Volatility')
st.pyplot(fig)

# Display Put Price Heatmap
st.subheader("Put Option Price Heatmap")
fig, ax = plt.subplots(figsize=(10,8))
sns.heatmap(put_prices, cmap='RdYlGn', xticklabels=np.round(spot_prices, 2), yticklabels=np.round(vol_range, 2), annot=True, fmt=".2f", ax=ax)
ax.set_xlabel('Spot Price')
ax.set_ylabel('Volatility')
st.pyplot(fig)

# Display Call PnL Heatmap
st.subheader("Call Option PnL Heatmap")
fig, ax = plt.subplots(figsize=(10,8))
sns.heatmap(pnl_call, cmap='RdYlGn', xticklabels=np.round(spot_prices, 2), yticklabels=np.round(vol_range, 2), annot=True, fmt=".2f", ax=ax)
ax.set_xlabel('Spot Price')
ax.set_ylabel('Volatility')
st.pyplot(fig)

# Display Put PnL Heatmap
st.subheader("Put Option PnL Heatmap")
fig, ax = plt.subplots(figsize=(10,8))
sns.heatmap(pnl_put, cmap='RdYlGn', xticklabels=np.round(spot_prices, 2), yticklabels=np.round(vol_range, 2), annot=True, fmt=".2f", ax=ax)
ax.set_xlabel('Spot Price')
ax.set_ylabel('Volatility')
st.pyplot(fig)



