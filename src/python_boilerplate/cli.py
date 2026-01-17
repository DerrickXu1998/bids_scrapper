"""Console script for python_boilerplate."""

import logging

import typer
from rich.console import Console

from .parallel_execute import ParallelExecutor
from .utils import scrape_url

app = typer.Typer()
console = Console()


@app.command()
def main():
    """Console script for python_boilerplate."""
    # console.logging.info("Replace this message by putting your code into python_boilerplate.cli.main")
    # console.logging.info("See Typer documentation at https://typer.tiangolo.com/")
    # utils.do_something_useful()
    import time

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    start = time.perf_counter()
    # In your main() function:
    start = time.perf_counter()

    # Create list of URLs
    urls = [f"https://www.ccgp.gov.cn/cggg/dfgg/zbgg/202601/t20260116_{i}.htm" for i in range(26081801, 26081811)]

    # Execute in parallel with 3 workers (Chrome is resource-intensive)
    with ParallelExecutor(max_workers=3) as executor:
        results = executor.execute(scrape_url, urls, "vF_detail_content_container", "错误页面！中国政府采购网")

    # Count valid results
    valid = sum(1 for result in results if result)

    logging.info("Finished scraping for %s urls and found %s valid ones", len(urls), valid)
    elapsed = time.perf_counter() - start
    logging.info(f"{elapsed:.4f} seconds")


if __name__ == "__main__":
    app()
