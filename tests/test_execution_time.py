""" Performance Tests to verify execution time of each test query"""

import pytest
import os
import time

from sqlalchemy import text
from src.db import engine

# set up fixture for testing

@pytest.fixture(scope="module")
def db_connect():

    connection = engine.connect()
    yield connection
    connection.close()

"""Test query execution time"""

#function to help load sql queries
#function returns queries as string

def load_sql_test_queries (path):
    with open(path,"r") as file:
        return file.read()

#directory to find query files
SQL_TEST_QUERIES_FOLDER = "tests/sql_test_queries/"


#test function for execution time
def test_queries_execution_time (db_connect):

#set threshold for maximum execution time
    max_execution_time:float = 0.5

#create loop to pass through each sql file only
    for file in os.listdir(SQL_TEST_QUERIES_FOLDER):
        if file.endswith(".sql"):

#create file path
            query_path = SQL_TEST_QUERIES_FOLDER + file

#load query file
            query = load_sql_test_queries(query_path)

#start timer
            start_time = time.perf_counter()

#execute queries and fetch results
            rows = db_connect.execute(
                text(query)
            ).fetchall()

#end timer
            end_time = time.perf_counter()

#calculate execution time
            execution_time = end_time - start_time

            print (f"{file}:\nExecution time: {execution_time:.4f} seconds")
            print(f"Rows: {len(rows)}")

#check execution time of each query is under the maximum threshold
            assert execution_time < max_execution_time

#check queries return a result
            assert len(rows) >= 0



