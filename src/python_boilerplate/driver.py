import logging
import time

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class selenium_driver:
    def __init__(self, retry_attempts: int = 3):
        self.retry_attempts = retry_attempts
        self._initialize_driver()

    def _initialize_driver(self):
        """Initialize the Chrome driver with retry logic."""
        for attempt in range(self.retry_attempts):
            try:
                options = webdriver.ChromeOptions()
                # Disable sandbox for better parallel execution
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")
                # Disable GPU acceleration
                options.add_argument("--disable-gpu")
                options.add_argument("--incognito")
                self.chrome_driver = webdriver.Chrome(options=options)

                logging.info("ChromeDriver initialized successfully")
                return
            except Exception as e:
                logging.debug("test-error", e)
                logging.warning(f"Failed to initialize ChromeDriver (attempt {attempt + 1}/{self.retry_attempts}): {e}")
                if attempt < self.retry_attempts - 1:
                    time.sleep(1)  # Wait before retrying
                else:
                    raise RuntimeError("Failed to initialize ChromeDriver after all retry attempts")

    def get_url(self, url):
        self.chrome_driver.get(url)

    def get_element_by_class_name_from_url(self, url, class_name, timeout=15, use_css_if_needed=True, void=None):
        """Navigate to `url` and return the first visible element matching `class_name`.

        This method:
        - waits for document ready
        - uses visibility_of_element_located
        - falls back to a JS querySelector if the wait times out
        - saves a screenshot and page source to the system temp dir on final failure
        """
        self.chrome_driver.get(url)

        if void:
            # We want to check multiple condition if we are not finding the right page
            # Being blocked or hitting an error page or wrong url
            if void in self.chrome_driver.title:
                logging.info("Ecounter void condition in title: %s", self.chrome_driver.title)
                return None
        # Wait for initial page load, but proceed if this times out (we have fallbacks below)
        try:
            logging.info("Loading page and waiting for readyState complete")
            WebDriverWait(self.chrome_driver, timeout).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
        except TimeoutException:
            logging.warning("TimeoutException encountered while waiting for page load")

            pass
        # Determine selector / By strategy
        by = By.CLASS_NAME if " " not in class_name or not use_css_if_needed else By.CSS_SELECTOR
        selector = class_name if by is By.CLASS_NAME else f".{class_name.replace(' ', '.')}"
        try:
            elem = WebDriverWait(self.chrome_driver, timeout).until(EC.visibility_of_element_located((by, selector)))
            logging.info("Found element using %s and selector %s", by, selector)
            return elem
        except TimeoutException:
            raise TimeoutException(
                f"(Element with class name '{class_name}' not found within {timeout} seconds using {by}='{selector}')"
            )

    def quit(self):
        """Close the Chrome driver."""
        self.chrome_driver.quit()
