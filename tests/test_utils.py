"""
Unit tests for utility functions.
"""

import pytest
from datetime import datetime, date, timedelta
from app.utils import (
    days_to_years,
    years_to_days,
    calculate_days_to_expiry,
    validate_inputs,
    calculate_implied_volatility
)

def test_days_to_years():
    """Test conversion from days to years."""
    assert days_to_years(365) == 1.0
    assert days_to_years(730) == 2.0
    assert days_to_years(180) == 0.5

def test_years_to_days():
    """Test conversion from years to days."""
    assert years_to_days(1.0) == 365
    assert years_to_days(2.0) == 730
    assert years_to_days(0.5) == 182  # Rounded down

def test_calculate_days_to_expiry():
    """Test calculation of days to expiry."""
    today = date.today()
    
    # Test with date object
    tomorrow = today + timedelta(days=1)
    assert calculate_days_to_expiry(tomorrow) == 1
    
    # Test with datetime object
    next_week = datetime.now() + timedelta(days=7)
    assert calculate_days_to_expiry(next_week) == 7
    
    # Test with string
    next_month = (today + timedelta(days=30)).strftime('%Y-%m-%d')
    assert calculate_days_to_expiry(next_month) == 30

def test_validate_inputs():
    """Test input validation."""
    # Valid inputs
    is_valid, error = validate_inputs(100, 100, 1, 0.05, 0, 0.2)
    assert is_valid
    assert error == ""
    
    # Invalid stock price
    is_valid, error = validate_inputs(-100, 100, 1, 0.05, 0, 0.2)
    assert not is_valid
    assert "Stock price must be positive" in error
    
    # Invalid strike price
    is_valid, error = validate_inputs(100, -100, 1, 0.05, 0, 0.2)
    assert not is_valid
    assert "Strike price must be positive" in error
    
    # Invalid time to maturity
    is_valid, error = validate_inputs(100, 100, -1, 0.05, 0, 0.2)
    assert not is_valid
    assert "Time to maturity must be positive" in error
    
    # Invalid volatility
    is_valid, error = validate_inputs(100, 100, 1, 0.05, 0, -0.2)
    assert not is_valid
    assert "Volatility must be positive" in error
    
    # Invalid risk-free rate
    is_valid, error = validate_inputs(100, 100, 1, -0.05, 0, 0.2)
    assert not is_valid
    assert "Risk-free rate cannot be negative" in error
    
    # Invalid dividend yield
    is_valid, error = validate_inputs(100, 100, 1, 0.05, -0.1, 0.2)
    assert not is_valid
    assert "Dividend yield cannot be negative" in error

def test_calculate_implied_volatility():
    """Test implied volatility calculation."""
    S, K, T, r, q = 100, 100, 1, 0.05, 0
    sigma = 0.2
    
    # Calculate option price with known volatility
    from app.black_scholes import option_price
    price = option_price(S, K, T, r, q, sigma, 'call')
    
    # Calculate implied volatility
    implied_vol = calculate_implied_volatility(price, S, K, T, r, q, 'call')
    
    assert abs(implied_vol - sigma) < 1e-5
    
    # Test with put option
    price = option_price(S, K, T, r, q, sigma, 'put')
    implied_vol = calculate_implied_volatility(price, S, K, T, r, q, 'put')
    assert abs(implied_vol - sigma) < 1e-5 