"""
Configuration constants for the quantitative pricing application.
"""

# Default risk-free rate (annual)
RISK_FREE_RATE = 0.05

# Default volatility
DEFAULT_VOLATILITY = 0.20

# Default time to maturity (in years)
DEFAULT_TIME_TO_MATURITY = 1.0

# Default number of time steps for numerical methods
DEFAULT_TIME_STEPS = 100

# Default number of price steps for numerical methods
DEFAULT_PRICE_STEPS = 100

# Default strike price
DEFAULT_STRIKE = 100.0

# Default spot price
DEFAULT_SPOT = 100.0

# Default dividend yield
DEFAULT_DIVIDEND_YIELD = 0.0

# Numerical precision for calculations
EPSILON = 1e-10

# Maximum iterations for numerical methods
MAX_ITERATIONS = 1000 