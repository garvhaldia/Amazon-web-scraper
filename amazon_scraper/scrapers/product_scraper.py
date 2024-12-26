from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from utils.helper import Helpers
import logging
import time
from datetime import datetime
import os

class ProductScraper:
    def __init__(self, driver):
        try:
            self.driver = driver
            self.helpers = Helpers()
        except Exception as e:
            logging.error(f"Error initializing ProductScraper: {str(e)}")
            raise

    def get_categories(self, limit=10):
        """Get Amazon bestseller categories"""
        categories = []
        try:
            logging.info("Navigating to Best Sellers page")
            try:
                self.driver.get('https://www.amazon.in/gp/bestsellers')
                logging.info("Waiting for page to load completely")
                time.sleep(5)
            except WebDriverException as e:
                logging.error(f"Failed to navigate to Best Sellers page: {str(e)}")
                return []
            
            # Try to find categories in the main content
            try:
                category_headers = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_all_elements_located(
                        (By.CSS_SELECTOR, "div._p13n-zg-nav-tree-all_style_zg-browse-group__88fbz")
                    )
                )
                
                for header in category_headers[:limit]:
                    try:
                        link = header.find_element(By.TAG_NAME, "a")
                        name = self.helpers.clean_text(link.text)
                        url = link.get_attribute('href')
                        
                        if name and url and 'bestsellers' in url and name != "See More":
                            try:
                                category = {
                                    'name': name,
                                    'url': url
                                }
                                categories.append(category)
                                logging.info(f"Added category: {name}")
                            except Exception as e:
                                logging.error(f"Failed to add category: {str(e)}")
                                continue
                    except NoSuchElementException as e:
                        logging.error(f"Failed to find category elements: {str(e)}")
                        continue
                    except Exception as e:
                        logging.error(f"Failed to process category header: {str(e)}")
                        continue
                        
            except TimeoutException:
                logging.error("Timeout waiting for category headers")
            except Exception as e:
                logging.error(f"Failed to find categories in main content: {str(e)}")
                
                # Fallback: Try alternative selector
                try:
                    category_elements = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_all_elements_located(
                            (By.CSS_SELECTOR, "div[role='treeitem'] a")
                        )
                    )
                    
                    for element in category_elements[:limit]:
                        try:
                            name = self.helpers.clean_text(element.text)
                            url = element.get_attribute('href')
                            
                            if name and url and 'bestsellers' in url and name != "See More":
                                try:
                                    category = {
                                        'name': name,
                                        'url': url
                                    }
                                    categories.append(category)
                                    logging.info(f"Added category: {name}")
                                except Exception as e:
                                    logging.error(f"Failed to add category: {str(e)}")
                                    continue
                        except Exception as e:
                            logging.error(f"Failed to process category element: {str(e)}")
                            continue
                except Exception as e:
                    logging.error(f"Fallback category detection failed: {str(e)}")
            
            if not categories:
                logging.error("No categories found with any method")
                try:
                    self.driver.save_screenshot('categories_error.png')
                except Exception as e:
                    logging.error(f"Failed to save error screenshot: {str(e)}")
                return []
                
            logging.info(f"Successfully processed {len(categories)} categories")
            return categories
                
        except Exception as e:
            logging.error(f"Failed to get categories: {str(e)}")
            try:
                self.driver.save_screenshot('categories_error.png')
                logging.info("Error screenshot saved as categories_error.png")
            except Exception as screenshot_error:
                logging.error(f"Failed to save error screenshot: {str(screenshot_error)}")
            return []

    def scrape_category(self, category_url, max_products=1500, min_discount=50):
        """Scrape products from a category"""
        products = []
        page = 1
        
        while len(products) < max_products:
            try:
                url = f"{category_url}?pg={page}"
                logging.info(f"Scraping page {page} of category")
                
                try:
                    self.driver.get(url)
                except WebDriverException as e:
                    logging.error(f"Failed to load page {page}: {str(e)}")
                    break
                    
                self.helpers.random_delay(1, 2)
                
                # Wait for products to load
                logging.info("Waiting for products to load...")
                try:
                    WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-asin]"))
                    )
                except TimeoutException:
                    logging.error("Timeout waiting for products. Moving to next page.")
                    break
                
                # Get all product elements
                try:
                    product_elements = self.driver.find_elements(By.CSS_SELECTOR, "div[data-asin]")
                    logging.info(f"Found {len(product_elements)} products on page {page}")
                except NoSuchElementException:
                    logging.error("No product elements found")
                    break
                
                page_products = []  # Store products from current page
                
                for element in product_elements:
                    try:
                        # Skip empty elements
                        if not element.get_attribute('data-asin'):
                            continue
                        
                        product_data = {
                            'name': '',
                            'price': 0.0,
                            'rating': '',
                            'num_reviews': 0,
                            'discount': 0,
                            'asin': element.get_attribute('data-asin'),
                            'category': category_url.split('/')[-1],
                            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        }
                        
                        # Get product name
                        try:
                            name_element = element.find_element(By.CSS_SELECTOR, "span.a-text-normal")
                            product_data['name'] = self.helpers.clean_text(name_element.text)
                            logging.info(f"Found product: {product_data['name'][:50]}...")
                        except NoSuchElementException:
                            continue
                        
                        # Get price
                        try:
                            price_element = element.find_element(By.CSS_SELECTOR, "span.a-price-whole")
                            product_data['price'] = self.helpers.parse_price(price_element.text)
                            logging.info(f"Price: {product_data['price']}")
                        except NoSuchElementException:
                            pass
                        
                        # Get discount
                        try:
                            discount_element = element.find_element(By.CSS_SELECTOR, "span.a-savings")
                            product_data['discount'] = self.helpers.parse_discount(discount_element.text)
                            logging.info(f"Discount: {product_data['discount']}%")
                        except NoSuchElementException:
                            pass
                        
                        # Get rating
                        try:
                            rating_element = element.find_element(By.CSS_SELECTOR, "span.a-icon-alt")
                            product_data['rating'] = self.helpers.clean_text(rating_element.text)
                        except NoSuchElementException:
                            pass
                        
                        # Get number of reviews
                        try:
                            reviews_element = element.find_element(By.CSS_SELECTOR, "span.a-size-base")
                            product_data['num_reviews'] = self.helpers.parse_price(reviews_element.text)
                        except NoSuchElementException:
                            pass
                        
                        # Add product if it meets criteria
                        if product_data['name'] and product_data['price'] > 0:
                            try:
                                page_products.append(product_data)
                                logging.info(f"Added product to list")
                            except Exception as e:
                                logging.error(f"Failed to add product to list: {str(e)}")
                        
                    except Exception as e:
                        logging.error(f"Error processing product: {str(e)}")
                        continue
                
                # Add page products to main list
                try:
                    products.extend(page_products)
                    logging.info(f"Total products collected so far: {len(products)}")
                except Exception as e:
                    logging.error(f"Failed to add page products to main list: {str(e)}")
                
                # Save intermediate results
                if products:
                    try:
                        os.makedirs('output', exist_ok=True)
                        self.helpers.save_to_csv(products, 'output/output.csv')
                        logging.info(f"Saved {len(products)} products to CSV")
                    except Exception as e:
                        logging.error(f"Failed to save products to CSV: {str(e)}")
                
                # Check for next page
                try:
                    next_button = self.driver.find_element(By.CSS_SELECTOR, "li.a-last a")
                    if not next_button.is_enabled():
                        break
                    page += 1
                    logging.info(f"Moving to page {page}")
                except NoSuchElementException:
                    logging.info("No next page button found")
                    break
                except Exception as e:
                    logging.error(f"Error checking next page: {str(e)}")
                    break
                
            except Exception as e:
                logging.error(f"Error scraping page {page}: {str(e)}")
                break
        
        logging.info(f"Successfully scraped {len(products)} products from category")
        return products

    def get_detailed_info(self, product_url, product_data):
        """Get additional product details from product page"""
        try:
            try:
                self.driver.get(product_url)
            except WebDriverException as e:
                logging.error(f"Failed to load product page: {str(e)}")
                return
                
            self.helpers.random_delay(1, 2)

            # Get seller info
            try:
                merchant_info = self.driver.find_element(By.ID, 'merchant-info')
                product_data['sold_by'] = self.helpers.clean_text(merchant_info.text)
            except NoSuchElementException:
                pass
            except Exception as e:
                logging.error(f"Error getting seller info: {str(e)}")

            # Get description
            try:
                description = self.driver.find_element(By.ID, 'productDescription')
                product_data['description'] = self.helpers.clean_text(description.text)
            except NoSuchElementException:
                try:
                    description = self.driver.find_element(By.ID, 'feature-bullets')
                    product_data['description'] = self.helpers.clean_text(description.text)
                except NoSuchElementException:
                    pass
                except Exception as e:
                    logging.error(f"Error getting feature bullets: {str(e)}")
            except Exception as e:
                logging.error(f"Error getting product description: {str(e)}")

        except Exception as e:
            logging.error(f"Failed to get detailed product info: {str(e)}")
