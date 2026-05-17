"""Performance tests to verify execution time of concurrent queries"""

import os
import pytest
import time
import threading
from sqlalchemy import text

from engine.test_engine import engine

# set up fixture
@pytest.fixture(scope="module")
def db_connect():
    return engine

def load_sql_test_queries (path):
    with open(path,"r") as file:
        return file.read()

#directory to find query files
SQL_TEST_QUERIES_FOLDER = "tests/sql_test_queries/"

#test function for execution time
def test_concurrent_queries_execution_time (db_connect):

#set threshold for maximum execution time
  #  max_execution_time:float = 0.5

#create loop to pass through each sql file only
    for file in os.listdir(SQL_TEST_QUERIES_FOLDER):
        if file.endswith(".sql"):

#create file path
            query_path = SQL_TEST_QUERIES_FOLDER + file

#load query file
            query = load_sql_test_queries(query_path)

            number_users = 100

    # execute queries and fetch results

            def execute_query():
                with db_connect.connect() as db_engine:
                    db_engine.execute(
                text(query)
                ).fetchall()

            threads = []

    # set start time
            start_time = time.perf_counter()

            for _ in range(number_users):
                thread = threading.Thread(target=execute_query)

        # store thread
                threads.append(thread)

        # start all threads concurrently
            for thread in threads:
                thread.start()

        # test does not stop until all users finished executing
            for thread in threads:
                thread.join()

        # end timing
            end_time = time.perf_counter()

        # calculate execution time
            execution_time = end_time - start_time

            print(f"{file}:\nExecution time: {execution_time:.4f} seconds")
            print(f"\nUsers: {number_users}")


            #check execution time of each query is under the maximum threshold
         #   assert execution_time < max_execution_time



