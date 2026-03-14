"""
Unit tests for Black-Scholes option pricing functions.
"""

import pytest
import numpy as np
from app.black_scholes import (
    d1, d2, call_price, put_price, option_price
)

def test_d1_d2():
    """Test d1 and d2 calculations."""
    S, K, T, r, q, sigma = 100, 100, 1, 0.05, 0, 0.2
    
    d1_val = d1(S, K, T, r, q, sigma)
    d2_val = d2(S, K, T, r, q, sigma)
    
    assert isinstance(d1_val, float)
    assert isinstance(d2_val, float)
    assert d2_val == d1_val - sigma * np.sqrt(T)

def test_call_price():
    """Test call option pricing."""
    S, K, T, r, q, sigma = 100, 100, 1, 0.05, 0, 0.2
    
    price = call_price(S, K, T, r, q, sigma)
    
    assert isinstance(price, float)
    assert price > 0
    assert price < S  # Call price should be less than stock price

def test_put_price():
    """Test put option pricing."""
    S, K, T, r, q, sigma = 100, 100, 1, 0.05, 0, 0.2
    
    price = put_price(S, K, T, r, q, sigma)
    
    assert isinstance(price, float)
    assert price > 0
    assert price < K  # Put price should be less than strike price

def test_option_price():
    """Test generic option pricing function."""
    S, K, T, r, q, sigma = 100, 100, 1, 0.05, 0, 0.2
    
    call_price_val = option_price(S, K, T, r, q, sigma, 'call')
    put_price_val = option_price(S, K, T, r, q, sigma, 'put')
    
    assert call_price_val == call_price(S, K, T, r, q, sigma)
    assert put_price_val == put_price(S, K, T, r, q, sigma)
    
    with pytest.raises(ValueError):
        option_price(S, K, T, r, q, sigma, 'invalid')

def test_put_call_parity():
    """Test put-call parity relationship."""
    S, K, T, r, q, sigma = 100, 100, 1, 0.05, 0, 0.2
    
    call = call_price(S, K, T, r, q, sigma)
    put = put_price(S, K, T, r, q, sigma)
    
    # Put-Call Parity: C - P = S*e^(-qT) - K*e^(-rT)
    lhs = call - put
    rhs = S * np.exp(-q * T) - K * np.exp(-r * T)
    
    assert abs(lhs - rhs) < 1e-10 