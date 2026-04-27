"""Console script for bids_scrapper."""

import logging
import time
from datetime import datetime
from zoneinfo import ZoneInfo

import typer
from pydantic import BaseModel
from rich.console import Console

from bids_scrapper.workflow.bid_scraper import BidScraper

from .constants import dfgg_url_collection, zygg_url_collection
from .parallel_execute import ParallelExecutor
from .utils import scrape_url_text


class ExecuteConfig(BaseModel):
    starting_index: int
    ending_index: int


app = typer.Typer()
console = Console()


@app.command()
def main():
    """main entry point for the CLI."""
    # Disable at the moment until we have multiple steps
    # args = parse_args()
    # runtime_args = _parse_runtime_args(args.runtime_args)
    # _setup_logger(args, runtime_args)

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    start = time.perf_counter()

    # Create list of URLs
    urls = [f"https://www.ccgp.gov.cn/cggg/dfgg/gzgg/202601/t20260118_{i}.htm" for i in range(26087598, 26087811)]
    # urls = [f"https://www.ccgp.gov.cn/cggg/dfgg/jzxcs/202601/t20260118_{i}.htm" for i in range(26087598, 26087811)]

    # Execute in parallel with 3 workers (Chrome is resource-intensive)
    with ParallelExecutor(max_workers=20) as executor:
        results = executor.execute(scrape_url_text, urls, "vF_detail_content_container", "错误页面！中国政府采购网")

    # Count valid results
    valid = sum(1 for result in results if result)

    logging.info("Finished scraping for %s urls and found %s valid ones", len(urls), valid)
    elapsed = time.perf_counter() - start
    logging.info(f"{elapsed:.4f} seconds")


@app.command()
def execute_anchor():
    """main entry point for the CLI."""
    _setup_logger(None, None)

    start = time.perf_counter()
    scraper = BidScraper()
    results = scraper.anchor_index()

    # Count valid results
    logging.info("Anchor urls found: %s", results)
    elapsed = time.perf_counter() - start
    logging.info(f"{elapsed:.4f} seconds")


@app.command()
def execute(
    starting_index: int = typer.Option(...),
    ending_index: int = typer.Option(...),
):
    """main entry point for the CLI."""
    cfg = ExecuteConfig(starting_index=starting_index, ending_index=ending_index)
    _setup_logger(None, cfg.dict())

    start = time.perf_counter()
    urls = []
    today = datetime.now(ZoneInfo("Asia/Shanghai"))
    year_month = today.strftime("%Y%m")
    year_month_date = today.strftime("%Y%m%d")
    # year_month = 202601
    # year_month_date = 20260118
    # Create list of URLs
    for index in range(cfg.starting_index, cfg.ending_index + 1):
        for url in zygg_url_collection:
            urls.append(url.format(year_month=year_month, year_month_date=year_month_date, index=index))
        for url in dfgg_url_collection:
            urls.append(url.format(year_month=year_month, year_month_date=year_month_date, index=index))
    logging.info("Total urls to scrape: %s", len(urls))

    with ParallelExecutor(max_workers=5) as executor:
        results = executor.execute(scrape_url_text, urls, "vF_detail_content_container", "错误页面！中国政府采购网")

    # Count valid results
    valid = sum(1 for result in results if result)

    logging.info("Finished scraping for %s urls and found %s valid ones", len(urls), valid)
    elapsed = time.perf_counter() - start
    logging.info(f"{elapsed:.4f} seconds")


# def parse_args() -> argparse.Namespace:
#     """Parse command line arguments."""
#     parser = argparse.ArgumentParser(description="Bids scraper CLI")

#     parser.add_argument(
#         "--step",
#         "-s",
#         required=True,
#         choices=list(),
#         help="Step to execute",
#     )

#     parser.add_argument(
#         "--runtime-args",
#         "-rargs",
#         action="append",
#         help="runtime arguments in the form key=value",
#     )
#     return parser.parse_args()


# def _parse_runtime_args(raw_runtime_args: list[str]) -> dict[str, str]:
#     """Parse runtime arguments from command line arguments."""
#     runtime_args: dict[str, str] = {}
#     if not raw_runtime_args:
#         return runtime_args
#     for raw_runtime_arg in raw_runtime_args:
#         key, value = raw_runtime_arg.split("=", 1)
#         runtime_args[key] = value
#     return runtime_args


def _setup_logger(*_args, **_kwargs) -> None:
    """Setup logger based on runtime arguments."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


if __name__ == "__main__":
    app()
