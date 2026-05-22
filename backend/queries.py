from sqlalchemy.sql import func
from sqlalchemy.orm import Session
from .models import *
from datetime import datetime


# Query 1: Find all students enrolled in a specific course taught by a particular lecturer.
def all_course_students(db: Session, course_id: int, lecturer_id: int):
    return (
        db.query(Student)
        .join(Enrolment, Enrolment.student_id == Student.student_id)
        .join(Course_Lecturer, (Course_Lecturer.course_id == Enrolment.course_id) & (Course_Lecturer.lecturer_id == lecturer_id))
        .join(Lecturer, Lecturer.lecturer_id == Course_Lecturer.lecturer_id)
        .filter(
            Course_Lecturer.course_id == course_id,
            Lecturer.lecturer_id == lecturer_id
        )
        .all()
    )
 
 
# Query 2: List all students with an average grade above 70% who are in their final year of studies.
def final_year_students_above_70(db: Session):
    return (
        db.query(Student)
        .join(Grade, Grade.student_id == Student.student_id)
        .join(Program, Program.program_id == Student.program_id)
        .filter(Student.year_of_study == Program.duration_years)
        .group_by(Student.student_id)
        .having(func.avg(Grade.grade_percentage) > 70)
        .all()
    )
 
 
# Query 3: Identify students who haven't registered for any courses in the current semester.
def students_not_enrolled_this_semester(db: Session, semester: str, academic_year: str):
    enrolled_student_ids = (
        db.query(Enrolment.student_id)
        .filter(
            Enrolment.semester == semester,
            Enrolment.academic_year == academic_year,
            Enrolment.enrolment_status == "Enrolled"
        )
        .subquery()
    )
    return (
        db.query(Student)
        .filter(Student.student_id.notin_(enrolled_student_ids))
        .all()
    )
 
 
# Query 4: Retrieve the contact information for the faculty advisor of a specific student.
def student_faculty_advisor_information(db: Session, student_id: int):
    return (
        db.query(Lecturer)
        .join(Student, Student.advisor_id == Lecturer.lecturer_id)
        .filter(Student.student_id == student_id)
        .first()
    )
 
 
# Query 5: Search for lecturers with expertise in a particular research area.
def expert_lecturers_in_research_area(db: Session, area_of_expertise: str):
    return (
        db.query(Lecturer)
        .filter(Lecturer.area_of_expertise.ilike(f"%{area_of_expertise}%"))
        .all()
    )
 
 
# Query 6: List all courses taught by lecturers in a specific department.
def courses_by_department(db: Session, department_id: int):
    return (
        db.query(Course)
        .join(Course_Lecturer, Course_Lecturer.course_id == Course.course_id)
        .join(Lecturer, Lecturer.lecturer_id == Course_Lecturer.lecturer_id)
        .filter(Lecturer.department_id == department_id)
        .distinct()
        .all()
    )
 
 
# Query 7: Identify lecturers who have supervised the most student research projects.
def lecturers_most_student_projects(db: Session, limit: int = 10):
    student_project_counts = (
        db.query(
            Research_Project.principal_investigator_id.label("lecturer_id"),
            func.count(func.distinct(Research_Project_Member.project_id)).label("project_count")
        )
        .join(Research_Project_Member, Research_Project_Member.project_id == Research_Project.project_id)
        .filter(Research_Project_Member.student_id.isnot(None))
        .group_by(Research_Project.principal_investigator_id)
        .subquery()
    )
    return (
        db.query(Lecturer, student_project_counts.c.project_count)
        .join(student_project_counts, student_project_counts.c.lecturer_id == Lecturer.lecturer_id)
        .order_by(student_project_counts.c.project_count.desc())
        .limit(limit)
        .all()
    )
 
 
# Query 8: Generate a report on the publications of lecturers in the past year.
def lecturer_publications_report(db: Session, lecturer_id: int):
    return (
        db.query(Lecturer_Publication)
        .filter(Lecturer_Publication.lecturer_id == lecturer_id)
        .filter(Lecturer_Publication.publication_year == datetime.now().year - 1)
        .all()
    )
 
 
# Query 9: Retrieve the names of students advised by a specific lecturer.
def students_advised_by_lecturer(db: Session, lecturer_id: int):
    return (
        db.query(Student)
        .filter(Student.advisor_id == lecturer_id)
        .all()
    )
 
 
# Query 10: Find all staff members employed in a specific department.
def department_staff_members(db: Session, department_id: int):
    lecturers = (
        db.query(Lecturer)
        .filter(Lecturer.department_id == department_id)
        .all()
    )
 
    non_academic_staff = (
        db.query(Non_Academic_Staff)
        .filter(Non_Academic_Staff.department_id == department_id)
        .all()
    )
 
    return lecturers, non_academic_staff
 
 
# Query 11: Identify employees who supervise student employees in a particular program.
def lecturers_supervising_in_program(db: Session, program_id: int):
    return (
        db.query(Lecturer)
        .join(Student, Student.advisor_id == Lecturer.lecturer_id)
        .filter(Student.program_id == program_id)
        .distinct()
        .all()
    )


def display_all_student_records(db: Session):
    return (
        db.query(Student)
        .all()
    )


def display_all_course_records(db: Session):
    return(
        db.query(Course)
        .all()
    )


def display_all_lecturer_records(db: Session):
    return(
        db.query(Lecturer)
        .all()
    )
