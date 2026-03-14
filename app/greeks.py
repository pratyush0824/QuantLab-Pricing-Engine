"""
Greek calculations for options using Black-Scholes model.
"""

import numpy as np
from scipy.stats import norm
from .black_scholes import d1, d2

def delta(S, K, T, r, q, sigma, option_type='call'):
    """
    Calculate option delta.
    
    Args:
        S (float): Current stock price
        K (float): Strike price
        T (float): Time to maturity in years
        r (float): Risk-free interest rate
        q (float): Dividend yield
        sigma (float): Volatility
        option_type (str): 'call' or 'put'
    
    Returns:
        float: Option delta
    """
    d1_val = d1(S, K, T, r, q, sigma)
    if option_type.lower() == 'call':
        return np.exp(-q * T) * norm.cdf(d1_val)
    else:  # put
        return np.exp(-q * T) * (norm.cdf(d1_val) - 1)

def gamma(S, K, T, r, q, sigma):
    """
    Calculate option gamma.
    
    Args:
        S (float): Current stock price
        K (float): Strike price
        T (float): Time to maturity in years
        r (float): Risk-free interest rate
        q (float): Dividend yield
        sigma (float): Volatility
    
    Returns:
        float: Option gamma
    """
    d1_val = d1(S, K, T, r, q, sigma)
    return np.exp(-q * T) * norm.pdf(d1_val) / (S * sigma * np.sqrt(T))

def theta(S, K, T, r, q, sigma, option_type='call'):
    """
    Calculate option theta (time decay).
    
    Args:
        S (float): Current stock price
        K (float): Strike price
        T (float): Time to maturity in years
        r (float): Risk-free interest rate
        q (float): Dividend yield
        sigma (float): Volatility
        option_type (str): 'call' or 'put'
    
    Returns:
        float: Option theta (per year)
    """
    d1_val = d1(S, K, T, r, q, sigma)
    d2_val = d2(S, K, T, r, q, sigma)
    
    if option_type.lower() == 'call':
        return (-S * sigma * np.exp(-q * T) * norm.pdf(d1_val) / (2 * np.sqrt(T)) -
                r * K * np.exp(-r * T) * norm.cdf(d2_val) +
                q * S * np.exp(-q * T) * norm.cdf(d1_val))
    else:  # put
        return (-S * sigma * np.exp(-q * T) * norm.pdf(d1_val) / (2 * np.sqrt(T)) +
                r * K * np.exp(-r * T) * norm.cdf(-d2_val) -
                q * S * np.exp(-q * T) * norm.cdf(-d1_val))

def vega(S, K, T, r, q, sigma):
    """
    Calculate option vega.
    
    Args:
        S (float): Current stock price
        K (float): Strike price
        T (float): Time to maturity in years
        r (float): Risk-free interest rate
        q (float): Dividend yield
        sigma (float): Volatility
    
    Returns:
        float: Option vega
    """
    d1_val = d1(S, K, T, r, q, sigma)
    return S * np.sqrt(T) * np.exp(-q * T) * norm.pdf(d1_val)

def rho(S, K, T, r, q, sigma, option_type='call'):
    """
    Calculate option rho.
    
    Args:
        S (float): Current stock price
        K (float): Strike price
        T (float): Time to maturity in years
        r (float): Risk-free interest rate
        q (float): Dividend yield
        sigma (float): Volatility
        option_type (str): 'call' or 'put'
    
    Returns:
        float: Option rho
    """
    d2_val = d2(S, K, T, r, q, sigma)
    if option_type.lower() == 'call':
        return K * T * np.exp(-r * T) * norm.cdf(d2_val)
    else:  # put
        return -K * T * np.exp(-r * T) * norm.cdf(-d2_val)

def calculate_all_greeks(S, K, T, r, q, sigma, option_type='call'):
    """
    Calculate all Greeks for an option.
    
    Args:
        S (float): Current stock price
        K (float): Strike price
        T (float): Time to maturity in years
        r (float): Risk-free interest rate
        q (float): Dividend yield
        sigma (float): Volatility
        option_type (str): 'call' or 'put'
    
    Returns:
        dict: Dictionary containing all Greeks
    """
    return {
        'delta': delta(S, K, T, r, q, sigma, option_type),
        'gamma': gamma(S, K, T, r, q, sigma),
        'theta': theta(S, K, T, r, q, sigma, option_type),
        'vega': vega(S, K, T, r, q, sigma),
        'rho': rho(S, K, T, r, q, sigma, option_type)
    } 