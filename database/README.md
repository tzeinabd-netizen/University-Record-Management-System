# University Database Management System

## Project Overview
This project implements a relational university database management system using MySQL. The system was designed to manage university operations including students, lecturers, departments, academic programmes, courses, enrolments, grades, research projects, and staff records.

The database follows a normalised relational structure and includes realistic sample data to support testing and query execution.

## Features
- Relational database design using MySQL
- Entity Relationship Diagram (ERD)
- Primary and foreign key relationships
- Normalised database schema
- Realistic university dataset
- Multi-table SQL queries
- Student enrolment and grade management
- Lecturer publications and qualifications tracking
- Research project participation management

## Technologies Used
- MySQL
- MySQL Workbench
- SQL
- draw.io
- GitHub

## Project Files
- create_database.sql
- create_tables.sql
- insert_dummy_data.sql
- queries.sql
- ERD_database.drawio.png

## Example Queries
The project includes queries such as:
Query 1. Students enrolled in a specific course taught by a lecturer
Query 2. Final-year students with average grades above 70%
Query 3. Students with no enrolments
Query 4. Faculty advisor lookup
Query 5. Lecturer publications in the past year
Query 6. Students who failed at least one course
Query 7. Top-performing courses based on average grades
Query 8. Research project member reports

## Database Entities
The database contains the following entities:
- Departments
- Programmes
- Lecturers
- Students
- Courses
- Enrolments
- Grades
- Research Projects
- Lecturer Publications
- Lecturer Qualifications
- Non-Academic Staff
- Disciplinary Records
- Research Project Members

## How to Run the Project

1. Open MySQL Workbench.
2. Run `create_database.sql`.
3. Run `create_tables.sql`.
4. Run `insert_dummy_data.sql`.
5. Run `queries.sql`.

The scripts should be executed in the above order to correctly create the database, tables, relationships, sample data, and SQL queries.
