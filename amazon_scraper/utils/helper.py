import time
import random
import json
import pandas as pd
import os
import logging
from datetime import datetime

class Helpers:
    @staticmethod
    def setup_logging(log_file):
        """Setup logging configuration"""
        try:
            # Create directory for log file if it doesn't exist
            os.makedirs(os.path.dirname(log_file), exist_ok=True)
            
            # Configure logging
            logging.basicConfig(
                level=logging.INFO,
                format='%(asctime)s [%(levelname)s] %(message)s',
                handlers=[
                    logging.FileHandler(log_file),
                    logging.StreamHandler()
                ]
            )
            logging.info("Logging setup completed")
        except Exception as e:
            print(f"Error setting up logging: {str(e)}")

    @staticmethod
    def random_delay(min_seconds=1, max_seconds=2):
        """Add random delay to avoid detection"""
        time.sleep(random.uniform(min_seconds, max_seconds))
    
    @staticmethod
    def parse_price(price_str):
        """Convert price string to float"""
        try:
            return float(''.join(filter(str.isdigit, price_str)))
        except:
            return 0.0
    
    @staticmethod
    def parse_discount(discount_str):
        """Extract discount percentage"""
        try:
            return int(''.join(filter(str.isdigit, discount_str)))
        except:
            return 0
    
    @staticmethod
    def clean_text(text):
        """Clean and standardize text"""
        if not text:
            return ""
        return ' '.join(text.strip().split())
    
    @staticmethod
    def save_to_json(data, filename):
        """Save data to JSON file"""
        try:
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            logging.info(f"Successfully saved data to JSON: {filename}")
        except Exception as e:
            logging.error(f"Error saving to JSON: {str(e)}")
    
    @staticmethod
    def save_to_csv(data, filename):
        """Save data to CSV file"""
        try:
            # Create output directory if it doesn't exist
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            
            # Convert data to DataFrame
            df = pd.DataFrame(data)
            
            # Check if file exists
            file_exists = os.path.isfile(filename)
            
            # Save to CSV
            if file_exists:
                # Append without header
                df.to_csv(filename, mode='a', header=False, index=False)
            else:
                # Create new file with header
                df.to_csv(filename, index=False)
                
            logging.info(f"Successfully saved {len(data)} products to {filename}")
        except Exception as e:
            logging.error(f"Error saving to CSV: {str(e)}")
    
    @staticmethod
    def get_timestamp():
        """Get current timestamp"""
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    @staticmethod
    def is_valid_product(product_data):
        """Validate product data"""
        required_fields = ['name', 'price', 'asin']
        return all(field in product_data and product_data[field] for field in required_fields)
