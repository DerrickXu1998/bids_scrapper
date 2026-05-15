# bids_scrapper

![PyPI version](https://img.shields.io/pypi/v/bids-scrapper.svg)
[![Documentation Status](https://readthedocs.org/projects/bids-scrapper/badge/?version=latest)](https://bids-scrapper.readthedocs.io/en/latest/?version=latest)

bids_scrapper helps scrape bid announcements.

* PyPI package: https://pypi.org/project/bids-scrapper/
* Free software: MIT License
* Documentation: https://bids-scrapper.readthedocs.io.

## Project structure (canonical)

Use this repository map as the source of truth for where changes should go:

- `src/bids_scrapper/`: application and scraping implementation
- `tests/`: test suites
- `docs/`: user and contributor-facing docs
- `.github/`: CI workflows and repository automation/config
- `makefile`: canonical quality workflow commands

## Quality workflow (canonical commands)

Run quality checks through Make targets:

- `make check` — lint
- `make format` — format
- `make type` — mypy type check
- `make test` — test execution
- `make cov` — test coverage report
- `make allci` — full local CI gate

For contributor setup and PR workflow details, see `CONTRIBUTING.md`.

## Features

- Web scraping framework for bid announcements
- Selenium-based browser automation
- Python 3.14 runtime baseline

## Credits

This package was created with [Cookiecutter](https://github.com/audreyfeldroy/cookiecutter) and the [audreyfeldroy/cookiecutter-pypackage](https://github.com/audreyfeldroy/cookiecutter-pypackage) project template.

