"""Console script for bids_scrapper."""

import logging
from datetime import datetime
from zoneinfo import ZoneInfo

from ..constants import dfgg_url_collection, zygg_url_collection
from ..parallel_execute import ParallelExecutor
from ..utils import scrape_url_by_attribute, scrape_url_text
from .constant import ANCHOR_DFGG, ANCHOR_ZYGG

STATE_LEVEL_TARGET_ELEMENT = "vF_detail_content_container"
STATE_LEVEL_VOID_CONDITION = "错误页面！中国政府采购网"

ACHOR_BID_TARGET_ELEMENT = "c_list_bid"


class BidScraper:
    def scrape_bids(self, starting_index: int, ending_index: int) -> list[str]:
        url_candidates = self._populate_url_candidate(starting_index, ending_index)
        with ParallelExecutor(max_workers=5) as executor:
            results = executor.execute(
                scrape_url_text, url_candidates, STATE_LEVEL_TARGET_ELEMENT, STATE_LEVEL_VOID_CONDITION
            )

        valid_scraped = [result for result in results if result]
        logging.info("Finished scraping for %s urls and found %s valid ones", len(url_candidates), len(valid_scraped))
        return valid_scraped

    def _populate_url_candidate(self, starting_index: int, ending_index: int) -> list[str]:
        today = datetime.now(ZoneInfo("Asia/Shanghai"))
        year_month = today.strftime("%Y%m")
        year_month_date = today.strftime("%Y%m%d")
        logging.info("Starting to populate urls for state level bids from index %s to %s", starting_index, ending_index)
        urls = []
        # Create list of URLs
        for index in range(starting_index, ending_index + 1):
            for url in zygg_url_collection:
                urls.append(url.format(year_month=year_month, year_month_date=year_month_date, index=index))
            for url in dfgg_url_collection:
                urls.append(url.format(year_month=year_month, year_month_date=year_month_date, index=index))
        logging.info("Total urls to scrape at state level bids: %s", len(urls))
        return urls

    def anchor_index(self) -> str:
        """Get the current maximum index scraped."""
        # Placeholder implementation; in a real scenario, this might query a database or a file
        achor_url_candidate = [ANCHOR_DFGG, ANCHOR_ZYGG]
        anchor_target_attribute = "href"

        # We would expect mutiple matching element, but scrape_url_text return the first one found, which is the first
        # so it is good enough. Might be problematic if the website structure changes
        # and the first one is no longer the anchor element, but we can fix it when that happens.
        output = []
        for url in achor_url_candidate:
            logging.info("Scraping anchor url candidate: %s", url)
            result = scrape_url_by_attribute(
                url, ACHOR_BID_TARGET_ELEMENT, STATE_LEVEL_VOID_CONDITION, anchor_target_attribute
            )
            output.append(result)
        anchor_index = self._process_anchors(output)
        sting_anchor_index = str(int(anchor_index))

        logging.info("Found string anchor index for scraping: %s", sting_anchor_index)
        return sting_anchor_index

    def _process_anchors(self, anchor_urls: list[str]) -> float:
        """Process the anchor URLs to extract bid information."""
        # we want the largest anchor value
        largest_anchor = float("-inf")
        for url in anchor_urls:
            anchor_from_parsed_url = url.rsplit("_", 1)[-1].split(".")[0]
            largest_anchor = (
                float(anchor_from_parsed_url) if float(anchor_from_parsed_url) > largest_anchor else largest_anchor
            )
        return largest_anchor
