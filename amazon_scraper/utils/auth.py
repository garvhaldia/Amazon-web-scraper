from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
from utils.helper import Helpers  # Match your file name (helper.py instead of helpers.py)

class AmazonAuth:
    def __init__(self, driver):
        self.driver = driver
        self.helpers = Helpers()

    def login(self, email, password):
        """Handle Amazon login process"""
        try:
            logging.info("Starting login process")
            
            # Check if credentials are available
            if not email or not password:
                logging.error("Missing login credentials")
                return False
                
            logging.info(f"Attempting to login with email: {email[:3]}...{email[-10:]}")
            
            # Navigate to Amazon
            self.driver.get('https://www.amazon.in')
            logging.info("Navigated to Amazon homepage")
            
            # Wait and click account button
            try:
                account_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.ID, 'nav-link-accountList'))
                )
                self.helpers.random_delay(1, 2)
                account_button.click()
                logging.info("Clicked account button")
            except Exception as e:
                logging.error(f"Failed to click account button: {str(e)}")
                self.driver.save_screenshot('login_error_1.png')
                return False

            # Enter email
            try:
                email_field = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.ID, 'ap_email'))
                )
                email_field.clear()
                self.helpers.random_delay(1, 2)
                email_field.send_keys(email)
                logging.info("Entered email")
                
                # Click continue
                continue_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.ID, 'continue'))
                )
                self.helpers.random_delay(1, 2)
                continue_button.click()
                logging.info("Clicked continue")
            except Exception as e:
                logging.error(f"Failed to enter email: {str(e)}")
                self.driver.save_screenshot('login_error_2.png')
                return False

            # Enter password
            try:
                password_field = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.ID, 'ap_password'))
                )
                password_field.clear()
                self.helpers.random_delay(1, 2)
                password_field.send_keys(password)
                logging.info("Entered password")
                
                # Click sign-in
                signin_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.ID, 'signInSubmit'))
                )
                self.helpers.random_delay(1, 2)
                signin_button.click()
                logging.info("Clicked sign-in button")
            except Exception as e:
                logging.error(f"Failed to enter password: {str(e)}")
                self.driver.save_screenshot('login_error_3.png')
                return False

            # Verify login success
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.ID, 'nav-link-accountList-nav-line-1'))
                )
                logging.info("Successfully logged in to Amazon")
                return True
            except Exception as e:
                logging.error(f"Failed to verify login: {str(e)}")
                self.driver.save_screenshot('login_error_4.png')
                return False

            
        except Exception as e:
            logging.error(f"Login failed: {str(e)}")
            # Take screenshot for debugging
            try:
                self.driver.save_screenshot('login_error.png')
                logging.info("Error screenshot saved as login_error.png")
            except:
                pass
            return False


    def check_login_status(self):
        """Check if currently logged in"""
        try:
            account_element = self.driver.find_element(By.ID, 'nav-link-accountList-nav-line-1')
            return 'Sign in' not in account_element.text
        except:
            return False
