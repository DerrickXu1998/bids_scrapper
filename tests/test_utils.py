#!/usr/bin/env python
import datetime

from python_boilerplate.utils import format_bids_url

def test_format_bids_url():
    template = "https://example.com/{year_month}/t{year_month_date}_{index}.htm"
    now = datetime.datetime.now()
    year_month = now.strftime("%Y%m")
    year_month_date = now.strftime("%Y%m%d")

    result = format_bids_url(template)

    expected = template.format(
        year_month=year_month,
        year_month_date=year_month_date,
        index="{index}",
    )

    assert result == expected
    assert "{index}" in result
