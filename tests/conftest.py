from dataclasses import dataclass

from pathlib import Path

import pytest

import shutil

import sqlite3 as sqlite

import typing

import time


CPD = Path(__file__).parents[1].resolve()


@dataclass
class Context:
    test_tmp_path: typing.ClassVar[Path] = CPD / "tmp"
    test_db_path: typing.ClassVar[Path] = CPD / "tmp" / "test.db"


@pytest.fixture(scope = "session")
def context() -> Context:
    return Context()


@pytest.fixture(scope = "session")
def tmp_setup_teardown(context: Context) -> typing.Iterator[None]:
    context.test_tmp_path.mkdir(exist_ok = True)
    yield
    shutil.rmtree(context.test_tmp_path)
