 Python web scraper that extracts information about best-selling products from Amazon India, focusing on products with significant discounts.


Features

Scrapes Amazon's Best Sellers section
Authenticates using Amazon credentials
Collects product information including:
Product Name
Price
Discount
Rating
Number of Reviews
ASIN (Amazon Standard Identification Number)
Category
Saves data in CSV format
Handles pagination
Includes error handling and logging

Prerequisites
Python 3.7+
Chrome browser
ChromeDriver

Installation

Clone the repository:
git clone <repository-url>
cd amazon_scraper

Install required packages:
pip install -r requirements.txt

Create a .env file in the root directory with your Amazon credentials:


AMAZON_EMAIL=your_amazon_email@example.com
AMAZON_PASSWORD=your_amazon_password

Important: Replace your_amazon_email@example.com and your_amazon_password with your actual Amazon login credentials.

output/output.csv: Contains scraped product data
output/scraper.log: Contains detailed logging information

Last Updated
2024-12-22 03:29:37

