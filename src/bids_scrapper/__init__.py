"""Top-level package for bids_scrapper."""

__author__ = """Derrick Xu"""
__email__ = "yufanx98@gmail.com"

__all__ = [
    "selenium_driver",
    "get_selenium_url",
    "is_running_in_docker",
    "ParallelExecutor",
    "scrape_url_text",
    "format_bids_url",
    "scrape_url_by_attribute",
]


def __getattr__(name: str):
    """Lazily expose public symbols to avoid heavy import side effects."""
    if name in {"selenium_driver", "get_selenium_url", "is_running_in_docker"}:
        from . import driver

        return getattr(driver, name)

    if name == "ParallelExecutor":
        from .parallel_execute import ParallelExecutor

        return ParallelExecutor

    if name in {"scrape_url_text", "format_bids_url", "scrape_url_by_attribute"}:
        from . import utils

        return getattr(utils, name)

    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
