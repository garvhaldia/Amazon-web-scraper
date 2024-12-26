"""
Utility package for Amazon Best Sellers Scraper.
Contains helper functions and authentication utilities.
"""

from datetime import datetime

# Package metadata
__version__ = '1.0.0'
__created__ = '2024-12-17'
__updated__ = '2024-12-17 20:37:46'

# Import main utility classes
from .auth import AmazonAuth
from .helpers import Helpers

__all__ = [
    'AmazonAuth',
    'Helpers'
]
