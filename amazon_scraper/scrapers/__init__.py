"""
Scrapers package for Amazon Best Sellers Scraper.
Contains scraping logic for Amazon products and categories.
"""

from .product_scraper import ProductScraper

__all__ = ['ProductScraper']

from datetime import datetime

# Package metadata
__version__ = '1.0.0'
__created__ = '2024-12-17'
__updated__ = '2024-12-17 20:37:46'

# Import main scraper class
from .product_scraper import ProductScraper

__all__ = [
    'ProductScraper'
]
