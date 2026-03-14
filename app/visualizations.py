"""
Visualization functions for option pricing analysis.
"""

import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from typing import Tuple, List, Dict
from .black_scholes import option_price
from .greeks import calculate_all_greeks

def plot_option_price_vs_stock(S_range: Tuple[float, float], K: float, T: float, r: float, q: float, 
                             sigma: float, option_type: str = 'call', num_points: int = 100) -> go.Figure:
    """
    Create an interactive plot of option price vs stock price.
    
    Args:
        S_range (Tuple[float, float]): (min_stock_price, max_stock_price)
        K (float): Strike price
        T (float): Time to maturity in years
        r (float): Risk-free interest rate
        q (float): Dividend yield
        sigma (float): Volatility
        option_type (str): 'call' or 'put'
        num_points (int): Number of points to plot
    
    Returns:
        go.Figure: Plotly figure object
    """
    S_min, S_max = S_range
    S = np.linspace(S_min, S_max, num_points)
    prices = [option_price(s, K, T, r, q, sigma, option_type) for s in S]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=S, y=prices, mode='lines', name='Option Price'))
    fig.add_trace(go.Scatter(x=S, y=np.maximum(S - K, 0) if option_type == 'call' else np.maximum(K - S, 0),
                            mode='lines', name='Intrinsic Value', line=dict(dash='dash')))
    
    fig.update_layout(
        title=f'{option_type.capitalize()} Option Price vs Stock Price',
        xaxis_title='Stock Price',
        yaxis_title='Option Price',
        showlegend=True
    )
    
    return fig

def plot_greeks_vs_stock(S_range: Tuple[float, float], K: float, T: float, r: float, q: float, 
                        sigma: float, option_type: str = 'call', num_points: int = 100) -> go.Figure:
    """
    Create an interactive plot of Greeks vs stock price.
    
    Args:
        S_range (Tuple[float, float]): (min_stock_price, max_stock_price)
        K (float): Strike price
        T (float): Time to maturity in years
        r (float): Risk-free interest rate
        q (float): Dividend yield
        sigma (float): Volatility
        option_type (str): 'call' or 'put'
        num_points (int): Number of points to plot
    
    Returns:
        go.Figure: Plotly figure object
    """
    S_min, S_max = S_range
    S = np.linspace(S_min, S_max, num_points)
    
    greeks_data = {
        'delta': [], 'gamma': [], 'theta': [], 'vega': [], 'rho': []
    }
    
    for s in S:
        greeks = calculate_all_greeks(s, K, T, r, q, sigma, option_type)
        for greek in greeks_data:
            greeks_data[greek].append(greeks[greek])
    
    fig = go.Figure()
    
    for greek, values in greeks_data.items():
        fig.add_trace(go.Scatter(x=S, y=values, mode='lines', name=greek.capitalize()))
    
    fig.update_layout(
        title=f'{option_type.capitalize()} Option Greeks vs Stock Price',
        xaxis_title='Stock Price',
        yaxis_title='Greek Value',
        showlegend=True
    )
    
    return fig

def plot_volatility_surface(K_range: Tuple[float, float], T_range: Tuple[float, float], 
                           S: float, r: float, q: float, sigma: float, option_type: str = 'call',
                           num_points: int = 50) -> go.Figure:
    """
    Create an interactive 3D plot of the volatility surface.
    
    Args:
        K_range (Tuple[float, float]): (min_strike, max_strike)
        T_range (Tuple[float, float]): (min_time, max_time)
        S (float): Current stock price
        r (float): Risk-free interest rate
        q (float): Dividend yield
        sigma (float): Volatility
        option_type (str): 'call' or 'put'
        num_points (int): Number of points in each dimension
    
    Returns:
        go.Figure: Plotly figure object
    """
    K_min, K_max = K_range
    T_min, T_max = T_range
    
    K = np.linspace(K_min, K_max, num_points)
    T = np.linspace(T_min, T_max, num_points)
    
    K, T = np.meshgrid(K, T)
    Z = np.zeros_like(K)
    
    for i in range(num_points):
        for j in range(num_points):
            Z[i, j] = option_price(S, K[i, j], T[i, j], r, q, sigma, option_type)
    
    fig = go.Figure(data=[go.Surface(x=K, y=T, z=Z)])
    
    fig.update_layout(
        title=f'{option_type.capitalize()} Option Price Surface',
        scene=dict(
            xaxis_title='Strike Price',
            yaxis_title='Time to Maturity',
            zaxis_title='Option Price'
        )
    )
    
    return fig

def plot_price_heatmap(S_range: Tuple[float, float], T_range: Tuple[float, float], 
                      K: float, r: float, q: float, sigma: float, option_type: str = 'call',
                      num_points: int = 50) -> go.Figure:
    """
    Create an interactive heatmap of option prices.
    
    Args:
        S_range (Tuple[float, float]): (min_stock_price, max_stock_price)
        T_range (Tuple[float, float]): (min_time, max_time)
        K (float): Strike price
        r (float): Risk-free interest rate
        q (float): Dividend yield
        sigma (float): Volatility
        option_type (str): 'call' or 'put'
        num_points (int): Number of points in each dimension
    
    Returns:
        go.Figure: Plotly figure object
    """
    S_min, S_max = S_range
    T_min, T_max = T_range
    
    S = np.linspace(S_min, S_max, num_points)
    T = np.linspace(T_min, T_max, num_points)
    
    S, T = np.meshgrid(S, T)
    Z = np.zeros_like(S)
    
    for i in range(num_points):
        for j in range(num_points):
            Z[i, j] = option_price(S[i, j], K, T[i, j], r, q, sigma, option_type)
    
    fig = go.Figure(data=go.Heatmap(
        z=Z,
        x=S[0, :],
        y=T[:, 0],
        colorscale='Viridis'
    ))
    
    fig.update_layout(
        title=f'{option_type.capitalize()} Option Price Heatmap',
        xaxis_title='Stock Price',
        yaxis_title='Time to Maturity'
    )
    
    return fig 