from betacovdb import db_utils
from betacovdb import db_entry

import conftest

from dataclasses import astuple

import pytest

import sqlite3 as sqlite

import typing


@pytest.mark.usefixtures("tmp_setup_teardown")
def test_db_setup(context: conftest.Context) -> None:
    db_utils.setup(context.test_db_path)
    assert (context.test_db_path).exists()


def test_table_creation(context: conftest.Context) -> None:
    with sqlite.connect(context.test_db_path) as conn:
        db_utils.create_table_ic_table(conn)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type = 'table';")
        assert cursor.fetchone()[0] == "ab_ic"
    conn.close()


@pytest.mark.parametrize(
    "row, expected_entry",
    [
        (
            db_entry.IC50Entry(
                "10-40",
                db_entry.Virus.SARS_COV_2_B_1_1_7,
                0.0450,
                db_entry.DOILink("10.1126", "scitranslmed.abn6859"),
                db_entry.VirusState.PSEUDO,
            ),
            (
                "10-40",
                "sars-cov-2-b-1-1-7",
                0.0450,
                "https://doi.org/10.1126/scitranslmed.abn6859",
                "pseudovirus",
            ),
        ),
        (
            db_entry.IC50Entry(
                "10-40",
                db_entry.Virus.SARS_COV_2_BA_4,
                2.414,
                db_entry.DOILink("10.1016", "j.cell.2022.12.018"),
                db_entry.VirusState.LIVE,
            ),
            (
                "10-40",
                "sars-cov-2-ba-4",
                2.414,
                "https://doi.org/10.1016/j.cell.2022.12.018",
                "livevirus",
            ),
        ),
    ],
)
def test_add_delete_row(context: conftest.Context, row: db_entry.IC50Entry, expected_entry: tuple[str, str, float, str]) -> None:
    with sqlite.connect(context.test_db_path) as conn:
        db_utils.add_row(conn, row)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM ab_ic")
        assert cursor.fetchone() == (1,) + expected_entry
        db_utils.delete_row(conn, 1)
    conn.close()


@pytest.mark.parametrize(
    "entry, id_, updated_entry",
    [
        (
            db_entry.IC50Entry(
                "10-40",
                db_entry.Virus.SARS_COV_2_B_1_1_7,
                0.0450,
                db_entry.DOILink("10.1126", "scitranslmed.abn6859"),
                db_entry.VirusState.PSEUDO,
            ),
            1,
            db_entry.IC50Entry(
                "10-40",
                db_entry.Virus.SARS_COV_2_BA_2,
                0.0550,
                db_entry.DOILink("10.1126", "scitranslmed.abn6859"),
                db_entry.VirusState.LIVE,
            ),
        ),
        (
            db_entry.IC50Entry(
                "10-40",
                db_entry.Virus.SARS_COV_2_BA_4,
                2.414,
                db_entry.DOILink("10.1016", "j.cell.2022.12.018"),
                db_entry.VirusState.LIVE,
            ),
            1,
            db_entry.IC50Entry(
                "CV3-25",
                db_entry.Virus.SARS_COV_1,
                2.412,
                db_entry.DOILink("10.1016", "j.cell.2022.12.018"),
                db_entry.VirusState.LIVE,
            ),
        ),
    ],
)
def test_update_row(
    context: conftest.Context,
    entry: db_entry.IC50Entry,
    id_: int,
    updated_entry: db_entry.IC50Entry
) -> None:
    with sqlite.connect(context.test_db_path) as conn:
        db_utils.add_row(conn, entry)
        db_utils.update_row(conn, id_, updated_entry)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM ab_ic")
        assert db_entry.IC50Entry(*cursor.fetchone()[1 :]) == updated_entry
        db_utils.delete_row(conn, 1)
    conn.close()
