from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import os
import logging
from config.credentials import (
    AMAZON_CREDENTIALS,
    OUTPUT_CONFIG
)
from utils.auth import AmazonAuth
from utils.helper import Helpers
from scrapers.product_scraper import ProductScraper

class AmazonBestSellerScraper:
    def __init__(self):
        self.setup_driver()
        self.helpers = Helpers()
        self.auth = AmazonAuth(self.driver)
        self.scraper = ProductScraper(self.driver)

    def setup_driver(self):
        """Setup Chrome driver with options"""
        chrome_options = Options()
        
        # Basic options
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        
        # Handle WebGL and GPU errors
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-software-rasterizer')
        chrome_options.add_argument('--disable-webgl')
        chrome_options.add_argument('--enable-unsafe-swiftshader')
        
        # Handle SSL errors
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--ignore-ssl-errors')
        chrome_options.add_argument('--allow-insecure-localhost')
        
        # Other necessary options
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-notifications')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--start-maximized')
        
        # Set user agent
        chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        
        # Remove automation flags
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation', 'enable-logging'])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Initialize the driver
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )
        
        # Set timeouts
        self.driver.set_page_load_timeout(30)
        self.driver.implicitly_wait(10)
        
        # Delete cookies
        self.driver.delete_all_cookies()





    def run(self):
        """Main execution method"""
        try:
            # Create output directory if it doesn't exist
            os.makedirs(OUTPUT_CONFIG['directory'], exist_ok=True)
            
            # Setup logging
            self.helpers.setup_logging(
                os.path.join(OUTPUT_CONFIG['directory'], 'scraper.log')
            )
            
            logging.info("Starting Amazon Best Sellers scraper")
            
            # Initialize list for all products
            all_products = []
            
            # Login to Amazon
            if not self.auth.login(
                AMAZON_CREDENTIALS['email'],
                AMAZON_CREDENTIALS['password']
            ):
                logging.error("Failed to login. Exiting...")
                return
            
            # Get categories
            categories = self.scraper.get_categories()
            if not categories:
                logging.error("Failed to get categories. Exiting...")
                return
            
            # Scrape products from each category
            for category in categories:
                logging.info(f"Scraping category: {category['name']}")
                products = self.scraper.scrape_category(
                    category['url'],
                    max_products=50,  # Reduced for faster processing
                    min_discount=50
                )
                
                all_products.extend(products)
                
                # Save after each category
                self.helpers.save_to_csv(
                    all_products,
                    os.path.join(OUTPUT_CONFIG['directory'], OUTPUT_CONFIG['csv_file'])
                )
                
                logging.info(f"Found {len(products)} products in {category['name']}")
                self.helpers.random_delay(1, 2)
            
            logging.info(f"Scraping completed. Total products: {len(all_products)}")
            
        except Exception as e:
            logging.error(f"Scraper failed: {str(e)}")
            
        finally:
            self.driver.quit()
            logging.info("Scraper finished")


if __name__ == "__main__":
    scraper = AmazonBestSellerScraper()
    scraper.run()
