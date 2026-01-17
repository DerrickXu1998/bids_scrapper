import logging

from .driver import selenium_driver


def scrape_url(url: str, class_name: str, void: str) -> str:
    """Scrape a single URL."""
    driver = None
    try:
        driver = selenium_driver()
        resp = driver.get_element_by_class_name_from_url(
            url,
            class_name,
            void=void,
        )
        return resp.text if resp else ""
    except Exception as e:
        logging.error(f"Error scraping {url}: {e}")
        return ""
    finally:
        if driver is not None:
            try:
                driver.quit()
            except Exception as e:
                logging.warning(f"Error closing driver: {e}")
