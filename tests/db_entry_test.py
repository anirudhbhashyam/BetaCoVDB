from betacovdb import db_entry

import pytest


@pytest.mark.parametrize(
    "s",
    [
        "https://doi.org/10.1002/pro.3208",
        "https://doi.org/10.1016/j.immuni.2021.10.019",
        "https://doi.org/10.1016/j.cell.2021.10.027",
    ],
)
def test_doi_link_creation_from_string(s: str) -> None:
    prefix, suffix = s.split("/")[-2 :]
    assert db_entry.DOILink.from_string(s) == db_entry.DOILink(prefix, suffix)


@pytest.mark.parametrize(
    "s",
    [
        "https://doi.org/-10.1002/pro.3208",
        "https://doi.org/8.1016/j.immuni.2021.10.019",
        "https://doi.org/7.1016/j.cell.2021.10.027",
    ],
)
def test_doi_link_creation_from_bad_url(s: str) -> None:
    with pytest.raises(ValueError):
        db_entry.DOILink.from_string(s)