"""Tests verifying correctness of query outputs"""

import pytest
from sqlalchemy import text
from backend.db import engine

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

# ──────────────────────────────────────────────
# QUERY TESTS
# Verifies queries return results
# Verifies query outputs match expected results
#   with query specific assert statements
# ──────────────────────────────────────────────

# Test query 1: Find all students enrolled in a specific course taught by a particular lecturer.

def test_find_students_enrolled_in_course (db_connect):

    query = load_sql_test_queries("tests/sql_test_queries/find_students_enrolled_in_course.sql")

    result = db_connect.execute(
        text(query)
    )

    rows = result.mappings().all()

    assert len(rows) > 0

    for row in rows:
        assert "lecturer_first_name" in row
        assert row["lecturer_first_name"] == "James"
        assert "lecturer_last_name" in row
        assert row ["lecturer_last_name"] == "Walker"
        assert "course_name" in row
        assert row ["course_name"] == "Database Systems"

    print (f"Query 1: Find all students enrolled in course taught by a particular lecturer")
    print(f"Rows: {len(rows)}")

# Test query 2: List all final-year students with an average grade above 70%.

def test_final_year_students_with_high_grade(db_connect):

    query = load_sql_test_queries("tests/sql_test_queries/find_all_final-year_with_high_grade.sql")

    result = db_connect.execute(
        text(query)
    )
    rows = result.mappings().all()

    assert len(rows) > 0

    for row in rows:
        assert "year_of_study" in row
        assert row["year_of_study"] == 4
        assert "average_grade" in row
        assert row["average_grade"] > 70

    print(f"Query 2: Find final-year students with average grade above 70%")
    print(f"Rows: {len(rows)}")

# Test query 3: Identify students who have not registered for any courses.

def test_find_students_no_enrolments (db_connect):

    query = load_sql_test_queries("tests/sql_test_queries/find_students_no_enrolments.sql")

    result = db_connect.execute(
        text(query)
    )
    rows = result.mappings().all()

    assert len(rows) > 0

    expected = [
        {'student_id': 14, 'first_name': 'Tendai', 'last_name': 'Moyo'},
         {'student_id': 15, 'first_name': 'Olivia', 'last_name': 'Green'}]

    assert rows == expected

    print(f"Query 3: Find students who have not registered for any courses")
    print(f"Rows: {len(rows)}")

# Test query 4: Retrieve the contact information for the faculty advisor of a specific student.

def test_find_contact_info_advisor (db_connect):

    query = load_sql_test_queries("tests/sql_test_queries/find_contact_info_advisor.sql")

    result = db_connect.execute(
        text(query)
    )
    rows = result.mappings().all()

    assert len(rows) > 0

    for row in rows:
        assert "email" in row
        assert row ["email"] is not None
        assert "phone" in row
        assert row ["phone"] is not None
        assert "student_first_name" in row
        assert row["student_first_name"] == "Aisha"
        assert "student_last_name" in row
        assert row["student_last_name"] == "Rahman"

    print(f"Query 4: Retrieve contact information for faculty advisor of specific student")
    print(f"Rows: {len(rows)}")

# Test query 5: Generate a report on the publications of lecturers in the past year.

def test_generate_report_publications (db_connect):

    query = load_sql_test_queries("tests/sql_test_queries/generate_report_publications.sql")

    result = db_connect.execute(
        text(query)
    )
    rows = result.mappings().all()

    assert len(rows) > 0

    for row in rows:
        assert "publication_year" in row
        assert row ["publication_year"] == 2025
        assert "publication_title" in row
        assert row ["publication_title"] is not None
        assert "publication_year" in row
        assert row ["publication_year"] is not None
        assert "publication_type" in row
        assert row ["publication_type"] is not None
        assert "journal_or_conference" in row
        assert row ["journal_or_conference"] is not None

    print(f"Query 5: Generate report on publications of lecturers in past year")
    print(f"Rows: {len(rows)}")

#Test query 6: Identify students who failed at least one course.

def test_find_students_failed_course (db_connect):

    query = load_sql_test_queries("tests/sql_test_queries/find_students_failed_course.sql")

    result = db_connect.execute(
        text(query)
    )
    rows = result.mappings().all()

    assert len(rows) > 0

    for row in rows:
        assert "grade_percentage" in row
        assert row["grade_percentage"] < 40
        assert "course_name" in row
        assert row ["course_name"] is not None

    print(f"Query 6: Identify students who failed at least one course")
    print(f"Rows: {len(rows)}")

#Test query 7: Identify the top-performing courses based on average student grades.

def test_find_top_performing_courses (db_connect):

    query = load_sql_test_queries("tests/sql_test_queries/find_top-performing_courses.sql")

    result = db_connect.execute(
        text(query)
    )
    rows = result.mappings().all()

    assert len(rows) > 0

    grades = [row["average_course_grade"] for row in rows]

    assert grades == sorted (grades, reverse=True)

    print(f"Query 7: Identify the top-performing courses based on average student grades")
    print(f"Rows: {len(rows)}")

#Test query 8: Identify students and lecturers involved in research projects.

def test_find_students_lecturers_in_projects (db_connect):

    query = load_sql_test_queries("tests/sql_test_queries/find_students_lecturers_in_projects.sql")

    result = db_connect.execute(
        text(query)
    )
    rows = result.mappings().all()

    assert len(rows) > 0

    for row in rows:
        assert "member_role" in row
        assert row["member_role"] is not None
        assert "project_title" in row
        assert row["project_title"] is not None
        assert "member_name" in row
        assert row["member_name"] is not None

    print(f"Query 8: Identify students and lecturers involved in research projects")
    print(f"Rows: {len(rows)}")

#Test Query 9: Collect statistics on course popularity

def test_find_stats_on_course_popularity (db_connect):

    query = load_sql_test_queries("tests/sql_test_queries/find_stats_on_course_popularity.sql")

    result = db_connect.execute(
        text(query)
    )
    rows = result.mappings().all()

    assert len(rows) > 0

    course_rank = [row["course_ranking"] for row in rows]

    assert course_rank == sorted(course_rank, reverse=False)

    print(f"Query 9: Collect statistics on course popularity")
    print(f"Rows: {len(rows)}")

# Test query 10: Collect statistics on lecturer workload

def test_find_stats_on_lecturer_workload (db_connect):

    query = load_sql_test_queries("tests/sql_test_queries/find_stats_on_lecturer_workload.sql")

    result = db_connect.execute(
        text(query)
    )
    rows = result.mappings().all()

    assert len(rows) > 0

    workload_rank = [row["lecturer_ranking"] for row in rows]
    assert workload_rank == sorted(workload_rank, reverse=False)

    print(f"Query 10: Collect statistics on lecturer workload")
    print(f"Rows: {len(rows)}")












