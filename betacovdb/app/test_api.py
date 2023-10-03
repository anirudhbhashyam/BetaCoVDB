from betacovdb import db_entry

from fastapi.testclient import TestClient
from fastapi.responses import JSONResponse

from main import app

import pytest


client = TestClient(app)


def _delete_entries_using_query(query_response: JSONResponse) -> None:
    for entry in query_response.json()["entries"]:
        delete_response = client.delete(f"/ab_ic/{entry['id']}")
        assert delete_response.status_code == 200
        assert delete_response.json()["message"] == f"Successfully deleted entry with id_ = {entry['id']}."


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "BETACOVDB API"}


@pytest.mark.parametrize(
    "ab_name, expected_response",
    [
        (
            "CC95.108", 
            {
                "entries": [
                    {
                        "name": "CC95.108",
                        "virus": "sars-cov-2",
                        "ic50": 1.5,
                        "source": "https://doi.org/10.1016/j.immuni.2023.02.005",
                        "virus_state": "pseudovirus",
                    },
                    {
                        "name": "CC95.108",
                        "virus": "sars-cov-1",
                        "ic50": 7.5,
                        "source": "https://doi.org/10.1016/j.immuni.2023.02.005",
                        "virus_state": "pseudovirus",
                    },
                    {
                        "name": "CC95.108",
                        "virus": "mers-cov",
                        "ic50": 0.5,
                        "source": "https://doi.org/10.1016/j.immuni.2023.02.005",
                        "virus_state": "pseudovirus",
                    },
                ],
            },
        ),
    ],
)
def test_read_ab_ic(ab_name: str, expected_response: dict[str, str]) -> None:
    response = client.get(f"/ab_ic/{ab_name}")
    assert response.status_code == 200
    response_data = response.json()
    for entry in response_data["entries"]:
        del entry["id"]
    assert response_data == expected_response


@pytest.mark.parametrize(
    "data_dict",
    [
        {
            "name": "testnab",
            "virus": "sars-cov-2",
            "ic50": 0,
            "source": {
                "prefix": "10.1016",
                "suffix": "j.immuni.2021.10.019",
            },
            "virus_state": "pseudovirus",
        },
    ],
)
def test_add_ab_ic(data_dict: dict[str, str]) -> None:
    response = client.post("/ab_ic", json = data_dict)
    query_response = client.get(f"/ab_ic/{data_dict['name']}")
    assert response.status_code == 200
    assert response.json()["message"] == "Successfully added entry."
    assert query_response.status_code == 200
    for entry in query_response.json()["entries"]:
        assert entry["name"] == data_dict["name"]
        assert entry["virus"] == data_dict["virus"]
        assert entry["ic50"] == data_dict["ic50"]
        assert entry["source"] == f"https://doi.org/{data_dict['source']['prefix']}/{data_dict['source']['suffix']}"
    _delete_entries_using_query(query_response)


@pytest.mark.parametrize(
    "data_dict",
    [
        {
            "name": "testnab",
            "virus": "sars-cov-2",
            "ic50": 0,
            "source": {
                "prefix": "10.1016",
                "suffix": "j.immuni.2021.10.019",
            },
            "virus_state": "pseudovirus",
        },
    ], 
)
def test_delete_ab_ic(data_dict: dict[str, str]) -> None:
    response = client.post("/ab_ic", json = data_dict)
    assert response.status_code == 200
    query_response = client.get(f"/ab_ic/{data_dict['name']}")
    assert query_response.status_code == 200
    id_to_delete = query_response.json()["entries"][0]["id"]
    delete_response = client.delete(f"/ab_ic/{id_to_delete}")
    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == f"Successfully deleted entry with id_ = {id_to_delete}."


@pytest.mark.parametrize(
    "id_",
    [
        10000000,
        -1,
    ],
)
def test_delete_entry_non_existent_id(id_: int) -> None:
    with pytest.raises(ValueError):
        _ = client.delete(f"/ab_ic/{id_}")


@pytest.mark.parametrize(
    "entries",
    (
        [
            {
                "name": "testnab",
                "virus": "sars-cov-2",
                "ic50": 0.2340,
                "source": {
                "prefix": "10.11111",
                "suffix": "febs.16777",
                "_header": "https://doi.org"
                },
                "virus_state": "pseudovirus"
            },
            {
                "name": "testnab",
                "virus": "sars-cov-2",
                "ic50": 0.2345,
                "source": {
                "prefix": "10.11111",
                "suffix": "febs.16777",
                "_header": "https://doi.org"
                },
                "virus_state": "pseudovirus"
            }
        ],
    ),
)
def test_batch_add_entries(entries: list[db_entry.IC50Entry]) -> None:
    response = client.post("/ab_ic/batch", json = entries)
    assert response.status_code == 200
    assert response.json()["message"] == "Successfully added entries."
    for entry in entries:
        query_response = client.get(f"/ab_ic/{entry['name']}")
        assert query_response.status_code == 200
        for query_entry in query_response.json()["entries"]:
            assert query_entry["name"] in (x["name"] for x in entries)
            assert query_entry["virus"] in (x["virus"] for x in entries)
            assert query_entry["ic50"] in (x["ic50"] for x in entries)
    _delete_entries_using_query(query_response)
