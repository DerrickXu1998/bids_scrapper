"""Console script for python_boilerplate."""

import logging

import typer
from rich.console import Console

from .driver import selenium_driver

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

    i = 0
    valid = 0
    for i in range(26081000, 26081100):
        i += 1
        driver = selenium_driver()
        resp = driver.get_element_by_class_name_from_url(
            f"https://www.ccgp.gov.cn/cggg/dfgg/zbgg/202601/t20260116_{i}.htm",
            "vF_detail_content",
            void="错误页面！中国政府采购网",
        )
        if resp:
            # logging.info("Found valid page and content has:", resp.text)
            valid += 1

    logging.info("Finished scraping for %s urls and found %s valid ones", i, valid)
    elapsed = time.perf_counter() - start
    logging.info(f"{elapsed:.4f} seconds")


if __name__ == "__main__":
    app()
