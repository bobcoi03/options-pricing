import streamlit as st
import yfinance as yf
from models import black_scholes_option_price, monte_carlo_pricing
from enum import Enum

st.set_option('deprecation.showPyplotGlobalUse', False)

class MODELS(Enum):
    BLACK_SCHOLES = "Black Scholes"
    MONTE_CARLO = "Monte Carlo"
    BINOMIAL = "Binomial"

st.sidebar.title("Option Pricing Models")
model = st.sidebar.radio("", options=[model.value for model in MODELS])

st.subheader(model)

option_type = st.selectbox("Option type", ["call", "put"])
spot_price = st.number_input("Spot price", min_value=0.01)
strike_price = st.number_input("Strike price", min_value=0.01)
risk_free_rate = st.number_input("Risk free rate (%)")
t = st.number_input("Time to maturity (in years)", min_value=0.00001)
sigma = st.number_input("Volatility (%)")

if model == MODELS.BLACK_SCHOLES.value:
    dividend_yield = st.number_input("Dividend yield (%)")

    option_price = black_scholes_option_price(spot_price, strike_price, risk_free_rate, t, sigma, dividend_yield, option_type)

    st.write(f"BSM {option_type} price: ", option_price)

    st.header("Compare with real option chain")
    user_input = st.text_input("Ticker symbol")
    chain_type = st.selectbox("Option chain type", ["calls", "puts"])

    ticker = yf.Ticker(user_input)
    option_chain = ticker.option_chain()

    hist = ticker.history()
    st.write("Close", hist["Close"][0])

    if (chain_type == "calls"):
        st.dataframe(option_chain.calls)
    else:
        st.dataframe(option_chain.puts)
elif model == MODELS.MONTE_CARLO.value:
    number_of_simulations = st.slider('Number of simulations: ', 10, 100000, 50)
    num_of_movements = st.slider('Number of price movement simulations: ', 0, int(number_of_simulations/10), 10)
    MC = monte_carlo_pricing(spot_price, strike_price, int(t*365), risk_free_rate, sigma, int(number_of_simulations))
    MC.simulate_prices()
    MC.plot_simulation_results(num_of_movements)
    st.pyplot()

    st.write(f"Call option price: ", MC._calculate_call_option_price())
    st.write(f"Put option price: ", MC._calculate_put_option_price())






