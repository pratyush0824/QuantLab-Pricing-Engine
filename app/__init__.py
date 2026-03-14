"""
Quantitative pricing application package.
"""

from .black_scholes import option_price, call_price, put_price
from .greeks import calculate_all_greeks, delta, gamma, theta, vega, rho
from .utils import (
    days_to_years,
    years_to_days,
    calculate_days_to_expiry,
    validate_inputs,
    calculate_implied_volatility
)
from .visualizations import (
    plot_option_price_vs_stock,
    plot_greeks_vs_stock,
    plot_volatility_surface,
    plot_price_heatmap
)

__version__ = '0.1.0' 