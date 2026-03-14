"""
Utility functions for the quantitative pricing application.
"""

import numpy as np
from datetime import datetime, date
from typing import Union, Tuple

def days_to_years(days: int) -> float:
    """
    Convert number of days to years.
    
    Args:
        days (int): Number of days
    
    Returns:
        float: Number of years
    """
    return days / 365.0

def years_to_days(years: float) -> int:
    """
    Convert number of years to days.
    
    Args:
        years (float): Number of years
    
    Returns:
        int: Number of days
    """
    return int(years * 365)

def calculate_days_to_expiry(expiry_date: Union[date, datetime, str]) -> int:
    """
    Calculate days until expiry from today.
    
    Args:
        expiry_date (Union[date, datetime, str]): Expiry date
    
    Returns:
        int: Number of days until expiry
    """
    if isinstance(expiry_date, str):
        expiry_date = datetime.strptime(expiry_date, '%Y-%m-%d').date()
    elif isinstance(expiry_date, datetime):
        expiry_date = expiry_date.date()
    
    today = date.today()
    return (expiry_date - today).days

def validate_inputs(S: float, K: float, T: float, r: float, q: float, sigma: float) -> Tuple[bool, str]:
    """
    Validate input parameters for option pricing.
    
    Args:
        S (float): Current stock price
        K (float): Strike price
        T (float): Time to maturity in years
        r (float): Risk-free interest rate
        q (float): Dividend yield
        sigma (float): Volatility
    
    Returns:
        Tuple[bool, str]: (is_valid, error_message)
    """
    if S <= 0:
        return False, "Stock price must be positive"
    if K <= 0:
        return False, "Strike price must be positive"
    if T <= 0:
        return False, "Time to maturity must be positive"
    if sigma <= 0:
        return False, "Volatility must be positive"
    if r < 0:
        return False, "Risk-free rate cannot be negative"
    if q < 0:
        return False, "Dividend yield cannot be negative"
    return True, ""

def calculate_implied_volatility(price: float, S: float, K: float, T: float, r: float, q: float, 
                               option_type: str = 'call', tolerance: float = 1e-5, max_iter: int = 100) -> float:
    """
    Calculate implied volatility using Newton-Raphson method.
    
    Args:
        price (float): Market price of the option
        S (float): Current stock price
        K (float): Strike price
        T (float): Time to maturity in years
        r (float): Risk-free interest rate
        q (float): Dividend yield
        option_type (str): 'call' or 'put'
        tolerance (float): Convergence tolerance
        max_iter (int): Maximum number of iterations
    
    Returns:
        float: Implied volatility
    """
    from .black_scholes import option_price
    from .greeks import vega
    
    # Initial guess
    sigma = 0.5
    
    for i in range(max_iter):
        price_est = option_price(S, K, T, r, q, sigma, option_type)
        diff = price_est - price
        
        if abs(diff) < tolerance:
            return sigma
            
        vega_val = vega(S, K, T, r, q, sigma)
        if vega_val == 0:
            raise ValueError("Vega is zero, cannot calculate implied volatility")
            
        sigma = sigma - diff/vega_val
        
        if sigma <= 0:
            sigma = 0.0001
            
    raise ValueError("Failed to converge to implied volatility") 