"""
Unit tests for option Greeks calculations.
"""

import pytest
import numpy as np
from app.greeks import (
    delta, gamma, theta, vega, rho, calculate_all_greeks
)

def test_delta():
    """Test delta calculations."""
    S, K, T, r, q, sigma = 100, 100, 1, 0.05, 0, 0.2
    
    # Test call delta
    call_delta = delta(S, K, T, r, q, sigma, 'call')
    assert isinstance(call_delta, float)
    assert 0 <= call_delta <= 1  # Call delta should be between 0 and 1
    
    # Test put delta
    put_delta = delta(S, K, T, r, q, sigma, 'put')
    assert isinstance(put_delta, float)
    assert -1 <= put_delta <= 0  # Put delta should be between -1 and 0
    
    # Test put-call delta relationship
    assert abs(call_delta + put_delta - 1) < 1e-10

def test_gamma():
    """Test gamma calculations."""
    S, K, T, r, q, sigma = 100, 100, 1, 0.05, 0, 0.2
    
    gamma_val = gamma(S, K, T, r, q, sigma)
    
    assert isinstance(gamma_val, float)
    assert gamma_val > 0  # Gamma should be positive
    assert gamma_val < 1  # Gamma should be less than 1

def test_theta():
    """Test theta calculations."""
    S, K, T, r, q, sigma = 100, 100, 1, 0.05, 0, 0.2
    
    # Test call theta
    call_theta = theta(S, K, T, r, q, sigma, 'call')
    assert isinstance(call_theta, float)
    
    # Test put theta
    put_theta = theta(S, K, T, r, q, sigma, 'put')
    assert isinstance(put_theta, float)

def test_vega():
    """Test vega calculations."""
    S, K, T, r, q, sigma = 100, 100, 1, 0.05, 0, 0.2
    
    vega_val = vega(S, K, T, r, q, sigma)
    
    assert isinstance(vega_val, float)
    assert vega_val > 0  # Vega should be positive

def test_rho():
    """Test rho calculations."""
    S, K, T, r, q, sigma = 100, 100, 1, 0.05, 0, 0.2
    
    # Test call rho
    call_rho = rho(S, K, T, r, q, sigma, 'call')
    assert isinstance(call_rho, float)
    assert call_rho > 0  # Call rho should be positive
    
    # Test put rho
    put_rho = rho(S, K, T, r, q, sigma, 'put')
    assert isinstance(put_rho, float)
    assert put_rho < 0  # Put rho should be negative

def test_calculate_all_greeks():
    """Test calculation of all Greeks."""
    S, K, T, r, q, sigma = 100, 100, 1, 0.05, 0, 0.2
    
    greeks = calculate_all_greeks(S, K, T, r, q, sigma, 'call')
    
    assert isinstance(greeks, dict)
    assert all(greek in greeks for greek in ['delta', 'gamma', 'theta', 'vega', 'rho'])
    assert all(isinstance(value, float) for value in greeks.values())
    
    # Test with put option
    put_greeks = calculate_all_greeks(S, K, T, r, q, sigma, 'put')
    assert isinstance(put_greeks, dict)
    assert all(greek in put_greeks for greek in ['delta', 'gamma', 'theta', 'vega', 'rho'])
    assert all(isinstance(value, float) for value in put_greeks.values()) 