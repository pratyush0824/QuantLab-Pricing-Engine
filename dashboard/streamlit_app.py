"""
Streamlit dashboard for quantitative pricing application.
"""

import streamlit as st
import numpy as np
from datetime import datetime, timedelta
import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.black_scholes import option_price
from app.greeks import calculate_all_greeks
from app.utils import validate_inputs, days_to_years
from app.visualizations import (
    plot_option_price_vs_stock,
    plot_greeks_vs_stock,
    plot_volatility_surface,
    plot_price_heatmap
)

# Page config
st.set_page_config(
    page_title="Quantitative Pricing Dashboard",
    page_icon="📈",
    layout="wide"
)

# Title
st.title("Quantitative Pricing Dashboard")
st.markdown("""
This dashboard provides interactive tools for option pricing and analysis using the Black-Scholes model.
""")

# Sidebar inputs
st.sidebar.header("Option Parameters")

# Option type
option_type = st.sidebar.selectbox("Option Type", ["call", "put"])

# Stock price
S = st.sidebar.number_input("Stock Price ($)", value=100.0, min_value=0.1, step=1.0)

# Strike price
K = st.sidebar.number_input("Strike Price ($)", value=100.0, min_value=0.1, step=1.0)

# Time to maturity
T = st.sidebar.number_input("Time to Maturity (years)", value=1.0, min_value=0.01, step=0.1)

# Risk-free rate
r = st.sidebar.number_input("Risk-free Rate (%)", value=5.0, min_value=0.0, step=0.1) / 100

# Dividend yield
q = st.sidebar.number_input("Dividend Yield (%)", value=0.0, min_value=0.0, step=0.1) / 100

# Volatility
sigma = st.sidebar.number_input("Volatility (%)", value=20.0, min_value=0.1, step=0.1) / 100

# Validate inputs
is_valid, error_message = validate_inputs(S, K, T, r, q, sigma)
if not is_valid:
    st.error(error_message)
    st.stop()

# Calculate option price and Greeks
price = option_price(S, K, T, r, q, sigma, option_type)
greeks = calculate_all_greeks(S, K, T, r, q, sigma, option_type)

# Display results
col1, col2 = st.columns(2)

with col1:
    st.subheader("Option Price")
    st.write(f"${price:.4f}")

with col2:
    st.subheader("Greeks")
    for greek, value in greeks.items():
        st.write(f"{greek.capitalize()}: {value:.4f}")

# Visualization section
st.header("Visualizations")

# Tabs for different plots
tab1, tab2, tab3, tab4 = st.tabs([
    "Price vs Stock", "Greeks vs Stock", "Volatility Surface", "Price Heatmap"
])

with tab1:
    S_range = (S * 0.5, S * 1.5)
    fig1 = plot_option_price_vs_stock(S_range, K, T, r, q, sigma, option_type)
    st.plotly_chart(fig1, use_container_width=True)

with tab2:
    fig2 = plot_greeks_vs_stock(S_range, K, T, r, q, sigma, option_type)
    st.plotly_chart(fig2, use_container_width=True)

with tab3:
    K_range = (K * 0.8, K * 1.2)
    T_range = (0.1, T * 1.5)
    fig3 = plot_volatility_surface(K_range, T_range, S, r, q, sigma, option_type)
    st.plotly_chart(fig3, use_container_width=True)

with tab4:
    fig4 = plot_price_heatmap(S_range, T_range, K, r, q, sigma, option_type)
    st.plotly_chart(fig4, use_container_width=True)

# Additional information
st.sidebar.markdown("---")
st.sidebar.markdown("""
### About
This dashboard implements the Black-Scholes model for European option pricing.
- Supports both call and put options
- Calculates all major Greeks
- Provides interactive visualizations
- Updates in real-time as parameters change
""") 