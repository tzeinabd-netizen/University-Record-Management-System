# University Database Management System

## Project Overview

This project implements a relational university database management system using MySQL. The system manages core university operations including students, lecturers, academic programmes, departments, courses, enrolments, grades, research projects, and staff records.

The database follows a normalised relational structure and includes realistic sample data for testing and query execution.

## Features

- Relational database design using MySQL
- Entity Relationship Diagram (ERD)
- Primary and foreign key relationships
- Normalised database schema
- Realistic university sample dataset
- Student enrolment and grade management
- Research project and publication management
- Course scheduling and programme requirement tracking
- Emergency contact management
- Data validation using NOT NULL, UNIQUE, CHECK and ON DELETE constraints

## Technologies Used

- MySQL
- MySQL Workbench
- SQL
- draw.io
- GitHub

## Database Entities

- Departments
- Programs
- Program Requirements
- Lecturers
- Students
- Non-Academic Staff
- Emergency Contacts
- Courses
- Course Schedules
- Enrolments
- Grades
- Research Projects
- Research Project Members
- Lecturer Qualifications
- Lecturer Publications
- Disciplinary Records
- Course Lecturers

## How to Run the Database

1. Open MySQL Workbench.
2. Run 'create_database.sql'.
3. Run 'create_tables.sql'.
4. Run 'insert_dummy_data.sql'.

The scripts should be executed in the above order to correctly create the database, tables, relationships, constraints, and sample data.

---

## App Structure

```
main.py
requirements.txt
backend/
├── db.py
├── models.py
└── queries.py
frontend/
└── ui.py
```

## Tech Stack

| | |
|---|---|
| **Language** | Python |
| **Database ORM** | SQLAlchemy |
| **Database** | MySQL Workbench |
| **UI** | PyQt6 |


## Getting Started

1. **Create a virtual environment** *(optional)*:
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Configure environment variables**:
Copy `.env.example` to `.env` and set your database URL

4. **Run the app**:
```bash
python main.py
```

## Data Models (models.py)
- `Department` — faculty, research area, links to programs, lecturers, courses, and staff
- `Program` — degree info, duration, linked to a department and its graduation requirements
- `Program_Requirement` — required credits and minimum pass mark per program
- `Student` — personal info, program, advisor, year of study, and graduation status
- `Lecturer` — personal info, department, expertise, course load, and research interests
- `Non_Academic_Staff` — job title, employment type, salary, and department
- `Course` — code, level, credits, prerequisites, and department
- `Course_Schedule` — day, time, room, and capacity per course
- `Enrolment` — student–course link per semester and academic year
- `Course_Lecturer` — many-to-many between courses and lecturers
- `Grade` — grade percentage per student per course
- `Research_Project` — title, PI, funding source, dates, and outcome
- `Research_Project_Member` — lecturers or students on a project with their role
- `Lecturer_Qualification` — degree credentials per lecturer
- `Lecturer_Publication` — publications with type, year, and journal/conference
- `Disciplinary_Record`— incident log per student
- `Emergency_Contact` — contact linked to a student, lecturer, or staff member

## Queries Menu (queries.py)
`all_course_students`(db, course_name, lecturer_last_name) — students enrolled in a specific course taught by a particular lecturer, filtered by course name and lecturer surname
`final_year_students_above_70`(db) — students in year 4 averaging above 70%, returning student ID, name, year of study and rounded average grade
`students_not_enrolled` (db) — students with no enrolment records at all, using an outer join and NULL check
`student_faculty_advisor_information` (db, student_last_name) — advisor contact details for a student matched by surname, returning both student and advisor names, email and phone
`lecturer_publications_report` (db, publication_year) — all lecturer publications for a given year, ordered by lecturer surname and publication title
`students_failed_courses`(db) — students who failed at least one course with a grade below 40%, ordered by grade ascending
`top_performing_courses` (db) — courses ranked by average student grade in descending order
`research_project_members` (db) — all students and lecturers involved in research projects, with dynamically built full names and member type derived from a case statement
`course_popularity_stats` (db) — course enrolment counts and unique student sizes ranked using a SQL CTE and RANK() window function
`lecturer_workload_stats` (db) — lecturer teaching load ranked by students taught, using a SQL CTE and RANK() window function
`display_all_student_records` (db) — all student records
`display_all_course_records` (db) — all course records
`display_all_lecturer_records` (db) — all lecturer records

--- 
## Testing

## Project Structure

```
tests/
├── sql_test_queries          # Queries in separate .sql files used for running tests
├── test_concurrent_users.py  # Execution time of queries run concurrently
├── test_execution_time.py    # Execution time of queries run individually
├── test_models.py            # Database schema, boundary violation, and integrity constraint tests
└── test_queries.py           # Correctness of database query results
└── pytest.ini                # Testing runner confirguration and custom marker registration
```

## Test descriptions 

**unit_tests** This file targets the distinct business logic and constraints of each domain:
* `TestDepartment` – Asserts name uniqueness and auto-generated timestamp creation.
* `TestProgram` & `TestProgramRequirement` – Validates cascade rules, positive credit thresholds, and pass mark boundaries (0–100%).
* `TestLecturer` – Enforces unique email and phone constraints and rejects negative course loads.
* `TestStudent` – Validates mandatory fields, advisor links, and rejects non-positive year of study values.
* `TestCourse` & `TestCourseSchedule` – Enforces unique course codes, capacity floors, and valid class time ordering.
* `TestNonAcademicStaff` – Validates mandatory fields (job title, contract details) and non-negative salary boundaries.
* `TestEmergencyContact` – Ensures each contact links to exactly one person and blocks fully orphaned records.
* `TestEnrolment` – Confirms valid student and course FK references and rejects missing mandatory fields.
* `TestGrade` – Confirms valid student and course FK references and rejects missing mandatory fields.
* `TestResearchProject` – Enforces mandatory titles, start dates, and chronologically valid project lifecycles.
* `TestDisciplinaryRecord` – Ensures every record captures a description, incident date, and action taken.
* `TestLecturerQualification` & `TestLecturerPublication` – Rejects award and publication years predating 1900.
* `TestResearchProjectMember` – Enforces single-person exclusivity and blocks role mismatches between entity type and assigned role.

**Execution Instructions for Unit Testing**
1. To Run All Discover Tests:
   `pytest -v`
2. To Run the Unit Test File Explicitly:
   `pytest tests/unit_tests.py -v`
3. Isolate Specifc Test Module:
   `pytest -m student -v`
4. Run a Single Isolated Test Scenario:
   `pytest tests/unit_test.py::TestDepartment::test_duplicate_name -v`

**Test_queries**
This file tests the running of queries in the database. Each query is ran once. A test for each 
query use specific assert statements to verify that a) results are returned and b) the results 
are the correct expected outputs.

* `test_find_students_enrolled_in_course` - Test query 1: Find all students enrolled in a specific course taught by a particular lecturer.
* `test_final_year_students_with_high_grade`- Test query 2: List all final-year students with an average grade above 70%.
* `test_find_students_no_enrolments`- Test query 3: Identify students who have not registered for any courses.
* `test_find_contact_info_advisor`- Test query 4: Retrieve the contact information for the faculty advisor of a specific student.
* `test_generate_report_publications`- Test query 5: Generate a report on the publications of lecturers in the past year.
* `test_find_students_failed_course` - Test query 6: Identify students who failed at least one course.
* `test_find_top_performing_courses`- Test query 7: Identify the top-performing courses based on average student grades.
* `test_find_students_lecturers_in_projects`- Test query 8: Identify students and lecturers involved in research projects.
* `test_find_stats_on_course_popularity`- Test query 9: Collect statistics on course popularity.
* `test_find_stats_on_lecturer_workload`- Test query 10: Collect statistics on lecturer workload. 


**Test_execution_time**
This file tests the execution time of running the queries in the database. Each query is run once.
The time that it takes to execute the query and return results is measured. The number of rows 
retrieved by each query is also returned to verify that they have been executed correctly. 

* `test_queries_execution_time` - Tests execution time of each query. 

**Test_concurrent_users**
This file tests the execution time of running each query multiple times at the same time, 
simulating multiple users concurrently executing queries in the database. The number of 
simulated users is automatically set to 10 but can be modified when the test is repeated. 
The time that it takes to execute each query concurrently for the given number of users
is measured. Queries per second is also calculated as the throughput.

* `test_concurrent_users` - Tests execution time of each query run
  concurrently. 




