"""
Black-Scholes option pricing model implementation.
"""

import numpy as np
from scipy.stats import norm
from . import config

def d1(S, K, T, r, q, sigma):
    """
    Calculate d1 parameter for Black-Scholes formula.
    
    Args:
        S (float): Current stock price
        K (float): Strike price
        T (float): Time to maturity in years
        r (float): Risk-free interest rate
        q (float): Dividend yield
        sigma (float): Volatility
    
    Returns:
        float: d1 parameter
    """
    return (np.log(S/K) + (r - q + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))

def d2(S, K, T, r, q, sigma):
    """
    Calculate d2 parameter for Black-Scholes formula.
    
    Args:
        S (float): Current stock price
        K (float): Strike price
        T (float): Time to maturity in years
        r (float): Risk-free interest rate
        q (float): Dividend yield
        sigma (float): Volatility
    
    Returns:
        float: d2 parameter
    """
    return d1(S, K, T, r, q, sigma) - sigma * np.sqrt(T)

def call_price(S, K, T, r, q, sigma):
    """
    Calculate European call option price using Black-Scholes formula.
    
    Args:
        S (float): Current stock price
        K (float): Strike price
        T (float): Time to maturity in years
        r (float): Risk-free interest rate
        q (float): Dividend yield
        sigma (float): Volatility
    
    Returns:
        float: Call option price
    """
    d1_val = d1(S, K, T, r, q, sigma)
    d2_val = d2(S, K, T, r, q, sigma)
    
    return S * np.exp(-q * T) * norm.cdf(d1_val) - K * np.exp(-r * T) * norm.cdf(d2_val)

def put_price(S, K, T, r, q, sigma):
    """
    Calculate European put option price using Black-Scholes formula.
    
    Args:
        S (float): Current stock price
        K (float): Strike price
        T (float): Time to maturity in years
        r (float): Risk-free interest rate
        q (float): Dividend yield
        sigma (float): Volatility
    
    Returns:
        float: Put option price
    """
    d1_val = d1(S, K, T, r, q, sigma)
    d2_val = d2(S, K, T, r, q, sigma)
    
    return K * np.exp(-r * T) * norm.cdf(-d2_val) - S * np.exp(-q * T) * norm.cdf(-d1_val)

def option_price(S, K, T, r, q, sigma, option_type='call'):
    """
    Calculate option price based on option type.
    
    Args:
        S (float): Current stock price
        K (float): Strike price
        T (float): Time to maturity in years
        r (float): Risk-free interest rate
        q (float): Dividend yield
        sigma (float): Volatility
        option_type (str): 'call' or 'put'
    
    Returns:
        float: Option price
    """
    if option_type.lower() == 'call':
        return call_price(S, K, T, r, q, sigma)
    elif option_type.lower() == 'put':
        return put_price(S, K, T, r, q, sigma)
    else:
        raise ValueError("option_type must be 'call' or 'put'") 