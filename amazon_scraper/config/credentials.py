import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Amazon login credentials
AMAZON_CREDENTIALS = {
    'email': os.getenv('AMAZON_EMAIL'),
    'password': os.getenv('AMAZON_PASSWORD')
}

# Selenium Configuration
SELENIUM_CONFIG = {
    'implicit_wait': 10,
    'page_load_timeout': 30,
    'headless': False,  # Changed to False for debugging
    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

# URLs
BASE_URL = 'https://www.amazon.in'
BESTSELLER_URL = f'{BASE_URL}/gp/bestsellers'

# Categories to scrape (can be modified as needed)
CATEGORIES = [
    'Electronics',
    'Computers & Accessories',
    'Kitchen & Home',
    'Books',
    'Beauty',
    'Toys & Games',
    'Clothing',
    'Sports & Outdoors',
    'Health & Personal Care',
    'Home & Kitchen'
]

# Scraping Configuration
SCRAPING_CONFIG = {
    'max_products_per_category': 1500,
    'min_discount': 50,
    'delay_range': (2, 5)  # Random delay between requests (min, max) in seconds
}

# Output Configuration
OUTPUT_CONFIG = {
    'directory': 'output',
    'csv_file': 'output.csv',
    'json_file': 'output.json'
}
