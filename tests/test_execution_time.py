""" Performance Tests to verify execution time of each test query"""

import pytest
import os
import time

from sqlalchemy import text
from src.db import engine

# ──────────────────────────────────────────────
# PYTEST FIXTURE
# Sets up a clean database session.
# ──────────────────────────────────────────────

@pytest.fixture(scope="module")
def db_connect():
    """create connection to database"""
    connection = engine.connect()
    yield connection
    connection.close()

# ──────────────────────────────────────────────
# HELPER FUNCTION
# Helps to load sql queries
# ──────────────────────────────────────────────

def load_sql_test_queries (path):
    with open(path,"r") as file:
        return file.read()

# directory path to find query files
SQL_TEST_QUERIES_FOLDER = "tests/sql_test_queries/"

# ──────────────────────────────────────────────
# EXECUTION TIME TESTS
# Measures how long it takes to execute each
#    query once
# Verifies that execution time of each query is
#   under 0.02 seconds.
# ──────────────────────────────────────────────

def test_queries_execution_time (db_connect):
    """function to test execution time of each query"""

    max_execution_time:float = 0.02

    for file in os.listdir(SQL_TEST_QUERIES_FOLDER):
        if file.endswith(".sql"):

            query_path = SQL_TEST_QUERIES_FOLDER + file

            query = load_sql_test_queries(query_path)

            start_time = time.perf_counter()

            rows = db_connect.execute(
                text(query)
            ).fetchall()

            end_time = time.perf_counter()

            execution_time = end_time - start_time

            assert execution_time < max_execution_time
            assert len(rows) >= 0

            print (f"{file}:\nExecution time: {execution_time:.4f} seconds")
            print(f"Rows: {len(rows)}")
