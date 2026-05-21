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
- Data validation using constraints

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

## How to Run the Project

1. Open MySQL Workbench.
2. Run 'create_database.sql'.
3. Run 'create_tables.sql'.
4. Run 'insert_dummy_data.sql'.

The scripts should be executed in the above order to correctly create the database, tables, relationships, constraints, and sample data.

---

## Backend 

## Project Structure

backend/
├── db.py          # Database connection, session setup, and Base declaration
├── models.py      # SQLAlchemy ORM models
└── queries.py     # Reusable database query functions

## Tech Stack

Language: Python
Database ORM: sqlAlchemy
Database: MySQL Wokbench

## Getting the Backend Started

1. Install dependencies
bash 
- pip(3) install sqlalchemy python-dotenv
- pip(3) install sqlalchemy

2. Configure environment:
   Set your connection string in db.py: mysql+pymysql://root:@localhost/university_record_system

3. Initialize the database (db.py)
Tables are created automatically on startup via Base.metadata.create_all() at the bottom of models.py.

## Data Models (models.py) 

-Department — faculty, research area, links to programs, lecturers, courses, and staff
-Program — degree info, duration, linked to a department and its graduation requirements
-Program_Requirement — required credits and minimum pass mark per program
-Student — personal info, program, advisor, year of study, and graduation status
-Lecturer — personal info, department, expertise, course load, and research interests
-Non_Academic_Staff — job title, employment type, salary, and department
-Course — code, level, credits, prerequisites, and department
-Course_Schedule — day, time, room, and capacity per course
-Enrolment — student–course link per semester and academic year
-Course_Lecturer — many-to-many between courses and lecturers
-Grade — grade percentage per student per course
-Research_Project — title, PI, funding source, dates, and outcome
-Research_Project_Member — lecturers or students on a project with their role
-Lecturer_Qualification — degree credentials per lecturer
-Lecturer_Publication — publications with type, year, and journal/conference
-Disciplinary_Record — incident log per student
-Emergency_Contact — contact linked to a student, lecturer, or staff member

## Queries Menu (queries.py) 

-all_course_students(db, course_id, lecturer_id) — students enrolled in a course taught by a specific lecturer
-final_year_students_above_70(db) — final-year students averaging above 70%
-students_not_enrolled_this_semester(db, semester, academic_year) — students with no active enrolment this semester
-student_faculty_advisor_information(db, student_id) — advisor contact info for a given student
-expert_lecturers_in_research_area(db, area_of_expertise) — lecturers matching a research area (case-insensitive)
-courses_by_department(db, department_id) — all courses taught by lecturers in a department
-lecturers_most_student_projects(db, limit) — lecturers ranked by number of student projects supervised
-lecturer_publications_report(db, lecturer_id) — a lecturer's publications from the previous year
-students_advised_by_lecturer(db, lecturer_id) — all students under a specific advisor
-department_staff_members(db, department_id) — all lecturers and non-academic staff in a department
-lecturers_supervising_in_program(db, program_id) — lecturers advising students in a specific program
-display_all_student_records(db) — all student records
-display_all_course_records(db) — all course records
-display_all_lecturer_records(db) — all lecturer records


--- 


