"""Tests verifying correctness of query outputs - function correctness"""

import pytest
from sqlalchemy import text
from engine.test_engine import engine

@pytest.fixture(scope="module")
def db_connect():

    connection = engine.connect()
    yield connection
    connection.close()

#function to help load sql queries
#function returns queries as string

def load_sql_test_queries (path):
    with open(path,"r") as file:
        return file.read()


# Test query 1: Find all students enrolled in a specific course taught by a particular lecturer.

def test_find_students_enrolled_in_course (db_connect):

    query = load_sql_test_queries("tests/sql_test_queries/find_students_enrolled_in_course.sql")

    result = db_connect.execute(
        text(query)
    )

    rows = result.mappings().all()

    print (f"Query 1: Find all students enrolled in course taught by a particular lecturer")
    print(f"Rows: {len(rows)}")

    # check rows exist
    assert len(rows) > 0

    for row in rows:
        assert row["lecturer_first_name"] == "James"
        assert row ["lecturer_last_name"] == "Walker"

   # first_row = rows[0]

    # query specific assert statements
    #assert first_row["lecturer_last_name"] == "Walker"


# Test query 2: List all final-year students with an average grade above 70%.

def test_final_year_students_with_high_grade(db_connect):

    query = load_sql_test_queries("tests/sql_test_queries/find_all_final-year_with_high_grade.sql")

    result = db_connect.execute(
        text(query)
    )
    rows = result.mappings().all()

    print(f"Query 2: Find final-year students with average grade above 70%")
    print(f"Rows: {len(rows)}")

    #check rows exist
    assert len(rows) > 0

    for row in rows:
        assert row["year_of_study"] >= 3
        assert row["average_grade"] > 70

# Test query 3: Identify students who have not registered for any courses.

def test_find_students_no_enrolments (db_connect):

    query = load_sql_test_queries("tests/sql_test_queries/find_students_no_enrolments.sql")

    result = db_connect.execute(
        text(query)
    )
    rows = result.mappings().all()

    print(f"Query 3: Find students who have not registered for any courses")
    print(f"Rows: {len(rows)}")

    # check rows exist
    assert len(rows) > 0

    expected = [
        {'student_id': 14, 'first_name': 'Tendai', 'last_name': 'Moyo'},
         {'student_id': 15, 'first_name': 'Olivia', 'last_name': 'Green'}]

    assert rows == expected


# Test query 4: Retrieve the contact information for the faculty advisor of a specific student.

def test_find_contact_info_advisor (db_connect):

    query = load_sql_test_queries("tests/sql_test_queries/find_contact_info_advisor.sql")

    result = db_connect.execute(
        text(query)
    )
    rows = result.mappings().all()

    print(f"Query 4: Retrieve contact information for faculty advisor of specific student")
    print(f"Rows: {len(rows)}")

    # check rows exist
    assert len(rows) > 0

    for row in rows:
        assert "email" in row
        assert "phone" in row
        assert row["student_last_name"] == "Rahman"

# Test query 5: Generate a report on the publications of lecturers in the past year.


def test_generate_report_publications (db_connect):

    query = load_sql_test_queries("tests/sql_test_queries/generate_report_publications.sql")

    result = db_connect.execute(
        text(query)
    )
    rows = result.mappings().all()

    print(f"Query 5: Generate report on publications of lecturers in past year")
    print(f"Rows: {len(rows)}")

    # check rows exist
    assert len(rows) > 0

    for row in rows:
        assert row ["publication_year"] == 2025

#Test query 6: Identify students who failed at least one course.

def test_find_students_failed_course (db_connect):

    query = load_sql_test_queries("tests/sql_test_queries/find_students_failed_course.sql")

    result = db_connect.execute(
        text(query)
    )
    rows = result.mappings().all()

    print(f"Query 6: Identify students who failed at least one course")
    print(f"Rows: {len(rows)}")

    # check rows exist
    assert len(rows) > 0

    for row in rows:
        assert row["grade_percentage"] < 40



#Test query 7: Identify the top-performing courses based on average student grades.

def test_find_top_performing_courses (db_connect):

    query = load_sql_test_queries("tests/sql_test_queries/find_top-performing_courses.sql")

    result = db_connect.execute(
        text(query)
    )
    rows = result.mappings().all()

    print(f"Query 7: Identify the top-performing courses based on average student grades")
    print(f"Rows: {len(rows)}")

    # check rows exist
    assert len(rows) > 0

    grades = [row["average_course_grade"] for row in rows]

    assert grades == sorted (grades, reverse=True)


#Test query 8: Identify students and lecturers involved in research projects.

def test_find_students_lecturers_in_projects (db_connect):

    query = load_sql_test_queries("tests/sql_test_queries/find_students_lecturers_in_projects.sql")

    result = db_connect.execute(
        text(query)
    )
    rows = result.mappings().all()

    print(f"Query 8: Identify students and lecturers involved in research projects")
    print(f"Rows: {len(rows)}")

    # check rows exist
    assert len(rows) > 0

    for row in rows:
        assert row["member_role"] is not None

#Test Query 9: Collect statistics on course popularity

def test_find_stats_on_course_popularity (db_connect):

    query = load_sql_test_queries("tests/sql_test_queries/find_stats_on_course_popularity.sql")

    result = db_connect.execute(
        text(query)
    )
    rows = result.mappings().all()

    print(f"Query 9: Collect statistics on course popularity")
    print(f"Rows: {len(rows)}")

    # check rows exist
    assert len(rows) > 0

    course_rank = [row["course_ranking"] for row in rows]

    assert course_rank == sorted(course_rank, reverse=False)


# Test query 10: Collect statistics on lecturer workload

def test_find_stats_on_lecturer_workload (db_connect):

    query = load_sql_test_queries("tests/sql_test_queries/find_stats_on_lecturer_workload.sql")

    result = db_connect.execute(
        text(query)
    )
    rows = result.mappings().all()

    print(f"Query 10: Collect statistics on lecturer workload")
    print(f"Rows: {len(rows)}")

    # check rows exist
    assert len(rows) > 0

    workload_rank = [row["lecturer_ranking"] for row in rows]

    assert workload_rank == sorted(workload_rank, reverse=False)

#Test query 11: Identify members of the university with the same name

#def test_find_duplicate_names (db_connect):

 #    query = load_sql_test_queries("tests/sql_test_queries/find_duplicate_names.sql")

 #    result = db_connect.execute(
 #       text(query)
  #  )
  #   rows = result.mappings().all()

 #    print(f"Rows: {len(rows)}")

     # check rows exist

  #   assert len(rows)>0
















