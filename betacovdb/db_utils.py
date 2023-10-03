from betacovdb import db_entry

from pathlib import Path

import sqlite3 as sqlite

import typing


DB_PATH = Path(__file__).parents[1] / "betac.db"


def setup(db_path: Path) -> None:
    with sqlite.connect(db_path) as conn: ...
    conn.close()


def create_table_ic_table(conn: sqlite.Connection) -> None:
    cursor = conn.cursor()
    cursor.execute(
        """\
        CREATE TABLE IF NOT EXISTS ab_ic (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            virus TEXT NOT NULL,
            ic50 REAL NOT NULL,
            source TEXT NOT NULL,
            state TEXT NOT NULL
        )\
        """
    )


def add_row(conn: sqlite.Connection, entry: db_entry.IC50Entry) -> None:
    cursor = conn.cursor()
    cursor.execute(
        """\
        INSERT INTO ab_ic (name, virus, ic50, source, state)
        VALUES (?, ?, ?, ?, ?)\
        """,
        (
            entry.name,
            entry.virus,
            entry.ic50,
            str(entry.source),
            str(entry.virus_state),
        ),

    )


def delete_row(conn: sqlite.Connection, id_: int) -> None:
    cursor = conn.cursor()
    # Make sure that the row exists.
    cursor.execute(
        """\
        SELECT * FROM ab_ic WHERE id = ?\
        """,
        (id_,),
    )
    if not cursor.fetchall():
        return None
    cursor.execute(
        """\
        DELETE FROM ab_ic WHERE id = ?\
        """,
        (id_,),
    )
    return id_


def update_row(conn: sqlite.Connection, id_: int, entry: db_entry.IC50Entry) -> None:
    cursor = conn.cursor()
    cursor.execute(
        """\
        UPDATE ab_ic
        SET name = ?, virus = ?, ic50 = ?, source = ?, state = ?
        WHERE id = ?\
        """,
        (
            entry.name,
            entry.virus,
            entry.ic50,
            str(entry.source),
            str(entry.virus_state),
            id_,
        ),
    )


def add_rows(conn: sqlite.Connection, entries: typing.Iterable[db_entry.IC50Entry]) -> None:
    for entry in entries:
        add_row(conn, entry)


def get_ab_data(conn: sqlite.Connection, ab_name: str) -> list[typing.Any]:
    cursor = conn.cursor()
    cursor.execute(
        """\
        SELECT * FROM ab_ic WHERE name = ?\
        """,
        (ab_name,),
    )
    return cursor.fetchall()