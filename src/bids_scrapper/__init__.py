"""Top-level package for bids_scraper."""

__author__ = """Derrick Xu"""
__email__ = "yufanx98@gmail.com"

from .driver import get_selenium_url, is_running_in_docker, selenium_driver
from .parallel_execute import ParallelExecutor
from .utils import format_bids_url, scrape_url_by_attribute, scrape_url_text

__all__ = [
    "selenium_driver",
    "get_selenium_url",
    "is_running_in_docker",
    "ParallelExecutor",
    "scrape_url_text",
    "format_bids_url",
    "scrape_url_by_attribute",
]
