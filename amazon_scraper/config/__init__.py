"""
Configuration package for Amazon Best Sellers Scraper.
Contains credentials and configuration settings.
"""

from datetime import datetime

# Package metadata
__version__ = '1.0.0'
__author__ = 'Garv Haldia'
__created__ = '2024-12-17'
__updated__ = '2024-12-17 20:37:46'

# Make configuration variables available at package level
from .credentials import (
    AMAZON_CREDENTIALS,
    SELENIUM_CONFIG,
    SCRAPING_CONFIG,
    OUTPUT_CONFIG,
    CATEGORIES,
    BASE_URL,
    BESTSELLER_URL
)

__all__ = [
    'AMAZON_CREDENTIALS',
    'SELENIUM_CONFIG',
    'SCRAPING_CONFIG',
    'OUTPUT_CONFIG',
    'CATEGORIES',
    'BASE_URL',
    'BESTSELLER_URL'
]
