from betacovdb import db_entry
from betacovdb import db_utils

from fastapi import FastAPI

import sqlite3 as sqlite

import typing

import uvicorn


app = FastAPI()


@app.get("/")
async def read_root() -> dict[str, str]:
    return {"message": "BETACOVDB API"}


@app.get("/ab_ic/{ab_name}")
async def read_ab_ic(ab_name: str) -> dict[str, list[dict[str, typing.Any]]]:
    with sqlite.connect(db_utils.DB_PATH) as conn:
        data = db_utils.get_ab_data(conn, ab_name)
    response_data = [
        {
            "id": id_,
            "name": name,
            "virus": virus,
            "ic50": ic50,
            "source": source,
            "virus_state": virus_state,
        }
        for id_, name, virus, ic50, source, virus_state in data
    ]
    return {"entries": response_data}


@app.post("/ab_ic")
async def add_ab_ic(entry: db_entry.IC50Entry) -> dict[str, str]:
    with sqlite.connect(db_utils.DB_PATH) as conn:
        db_utils.add_row(conn, entry)
    return {"message": "Successfully added entry."}


@app.post("/ab_ic/batch")
async def add_ab_ic_batch(entries: list[db_entry.IC50Entry]) -> dict[str, str]:
    # convert the data in the post request to entry types.
    with sqlite.connect(db_utils.DB_PATH) as conn:
        db_utils.add_rows(conn, entries)
    return {"message": "Successfully added entries."}


@app.delete("/ab_ic/{id_}")
async def delete_ab_ic(id_: int) -> dict[str, str]:
    with sqlite.connect(db_utils.DB_PATH) as conn:
        possible_id_ = db_utils.delete_row(conn, id_)
    if possible_id_ is None:
        raise ValueError(f"Entry with {id_ = } does not exist.")
    return {"message": f"Successfully deleted entry with {id_ = }."}


@app.put("/ab_ic")
async def replace_ab_ic(id_: int, entry: db_entry.IC50Entry) -> dict[str, str]:
    with sqlite.connect(db_utils.DB_PATH) as conn:
        db_utils.update_row(conn, id_, entry)
    return {"message": "Successfully updated entry."}


def main() -> int:
    uvicorn.run(app)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
