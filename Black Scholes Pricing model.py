#Black Scholes Pricing model; python repl application, takes in 5 inputs to an option prices; 1 volatility 2 stock price; Current Asset Prices
# 3 strike price 4 time to maturity (Years) 5 Risk free interest rate 
# -> spits out both a call and a put value.
#Add an interacive GUI layer, use streamlit ; spit out heatmap , call / put price given the inputs 
# then add heatmap parameters such as min/max spot price and min / max volatility for heatmap 
#green values reflect higher numbers, red values reflect lower numbers 
# add a purchase price for the call and purchase price for the put ; then you will have a PnL for the call/ put 
# then you can have a heatmap displaying the pnL of the call / put given the inputs and the purchase prices, green for +ve PnL and red for -ve Pnl

import math
from scipy.stats import norm

#Definition of Options Class
class Option: 
    def __init__(
        self,
        Volatility: float,
        StockPrice: float,
        StrikePrice: float,
        TimeToMaturity: float,
        InterestRate: float
    ):
        self.Volatility = Volatility
        self.StockPrice = StockPrice
        self.StrikePrice = StrikePrice
        self.TimeToMaturity = TimeToMaturity
        self.InterestRate = InterestRate

    def run(self):
        d1 = (math.log(self.StockPrice / self.StrikePrice) + (self.InterestRate + ((self.Volatility ** 2) / 2)) * self.TimeToMaturity) / (self.Volatility * math.sqrt(self.TimeToMaturity))
        d2 = d1 - self.Volatility * math.sqrt(self.TimeToMaturity)
        CallPrice = (norm.cdf(d1) * self.StockPrice) - (norm.cdf(d2) * self.StrikePrice * math.exp(-self.InterestRate * self.TimeToMaturity))
        PutPrice = (self.StrikePrice * math.exp(-self.InterestRate * self.TimeToMaturity) * norm.cdf(-d2)) - (self.StockPrice * norm.cdf(-d1))
        return CallPrice, PutPrice 

option = Option(Volatility=0.2, StockPrice=100, StrikePrice=105, TimeToMaturity=1, InterestRate=0.05)
call, put = option.run()

print(f"Call Option Price: {call}")
print(f"Put Option Price: {put}")