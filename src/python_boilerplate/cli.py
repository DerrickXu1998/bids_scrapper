"""Console script for python_boilerplate."""

import argparse
import logging
import time

import typer
from rich.console import Console

from .parallel_execute import ParallelExecutor
from .utils import scrape_url

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
        results = executor.execute(scrape_url, urls, "vF_detail_content_container", "错误页面！中国政府采购网")

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


def _setup_logger(args: argparse.Namespace, kwargs: dict[str, str]) -> None:
    """Setup logger based on runtime arguments."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


if __name__ == "__main__":
    app()
