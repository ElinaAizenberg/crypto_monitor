"""
Configuration for cryptocurrency price monitoring bot
"""

# Cryptocurrency configuration with realistic and optimistic price thresholds
CRYPTO_CONFIG = {
    "bitcoin": {
        "symbol": "BTC",
        "realistic_price": 120000,  # USD
        "optimistic_price": 122000,  # USD
        "coingecko_id": "bitcoin"
    },
    "ethereum": {
        "symbol": "ETH", 
        "realistic_price": 4700,   # USD
        "optimistic_price": 4800,  # USD
        "coingecko_id": "ethereum"
    },
    "ripple": {
        "symbol": "XPR",
        "realistic_price": 3.0,    # USD
        "optimistic_price": 3.03,   # USD
        "coingecko_id": "ripple"
    },
    "solana": {
        "symbol": "SOL",
        "realistic_price": 215,    # USD
        "optimistic_price": 216,   # USD
        "coingecko_id": "solana"
    },
    "litecoin": {
        "symbol": "LTC",
        "realistic_price": 115,     # USD
        "optimistic_price": 117,    # USD
        "coingecko_id": "litecoin"
    }
}

# API Configuration
COINGECKO_API_URL = "https://api.coingecko.com/api/v3/simple/price"

# Default check interval in minutes
DEFAULT_CHECK_INTERVAL = 5
