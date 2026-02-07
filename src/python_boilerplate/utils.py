import logging

from selenium.webdriver.common.by import By

from .driver import selenium_driver


def scrape_url_text(url: str, class_name: str, void: str) -> str:
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


def scrape_url_by_attribute(url: str, class_name: str, void: str, attribute: str) -> str:
    """Scrape a single URL."""
    driver = None
    try:
        driver = selenium_driver()
        resp = driver.get_element_by_class_name_from_url(
            url,
            class_name,
            void=void,
        )
        if not resp:
            return ""
        value = resp.get_attribute(attribute)
        if attribute.lower() == attribute and not value:
            try:
                link = resp.find_element(By.CSS_SELECTOR, "a[href]")
                value = link.get_attribute(attribute)
            except Exception as e:
                logging.debug("No nested anchor href found for %s: %s", url, e)
        if value and value.startswith("./"):
            value = value[1:]
        return value or ""
    except Exception as e:
        logging.error(f"Error scraping {url}: {e}")
        return ""
    finally:
        if driver is not None:
            try:
                driver.quit()
            except Exception as e:
                logging.warning(f"Error closing driver: {e}")


def format_bids_url(url_template: str, index: int) -> str:
    """Format bids URL template with current date."""
    from datetime import datetime

    now = datetime.now()
    year_month = now.strftime("%Y%m")
    year_month_date = now.strftime("%Y%m%d")
    return url_template.format(
        year_month=year_month,
        year_month_date=year_month_date,
        index=index,
    )
