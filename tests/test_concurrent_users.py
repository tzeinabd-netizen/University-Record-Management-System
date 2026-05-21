"""Performance tests to verify execution time of concurrent queries"""

import os
import pytest
import time
import threading
from sqlalchemy import text
from src.db import engine

# ──────────────────────────────────────────────
# PYTEST FIXTURE
# Sets up a clean database session.
# ──────────────────────────────────────────────

@pytest.fixture(scope="module")
def db_connect():
    return engine

# ──────────────────────────────────────────────
# HELPER FUNCTION
# Helps to load sql queries
# ──────────────────────────────────────────────

def load_sql_test_queries (path):
    with open(path,"r") as file:
        return file.read()

#directory path to find query files
SQL_TEST_QUERIES_FOLDER = "tests/sql_test_queries/"

# ──────────────────────────────────────────────
# CONCURRENCY TESTS
# Simulates multiples users executing each
#   query concurrently
# Measures execution time and calculates
#   throughput
# Number of simulated users can be changed
# ──────────────────────────────────────────────

def test_concurrent_queries_execution_time (db_connect):
    """function to test execution time of concurrent queries"""

    for file in os.listdir(SQL_TEST_QUERIES_FOLDER):
        if file.endswith(".sql"):

            query_path = SQL_TEST_QUERIES_FOLDER + file

            query = load_sql_test_queries(query_path)

            #number of concurrent users set to 10
            number_users = 10

            def execute_query():
                """function to execute concurrent queries"""
                with db_connect.connect() as db_engine:
                    db_engine.execute(
                text(query)
                ).fetchall()

            threads = []

            start_time = time.perf_counter()

            for _ in range(number_users):
                thread = threading.Thread(target=execute_query)

                threads.append(thread)

            for thread in threads:
                thread.start()

            for thread in threads:
                thread.join()

            end_time = time.perf_counter()

            execution_time = end_time - start_time

            throughput = number_users / execution_time

            print(f"\nUsers: {number_users}")
            print(f"{file}:\nExecution time: {execution_time:.4f} seconds")
            print (f"{file}:\nThroughput: {throughput:.4f} queries per second")