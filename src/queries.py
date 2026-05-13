from sqlalchemy.sql import func
from sqlalchemy.orm import Session
from .models import *
from datetime import datetime

def final_year_students_above_70(db: Session):
    return(
        db.query(Student)
        .join(Grade, Grade.student_id == Student.student_id)
        .join(Program, Program.program_id == Student.program_id)
        .filter(Student.year_of_studer == Program.duration_years)
        .group_by(Student.student_id)
        .having(func.avg(Grade.grade_percentage) > 70)
        .all()
    )

def student_faculty_advisor_information(db: Session, student_id: int):
    return(
        db.query(Lecturer)
        .join(Student, Student.advisor_id== Lecturer.lecturer_id)
        .filter(Student.student_id == student_id)
        .first()
    )

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

def lecturer_publications_report (db: Session, lecturer_id: int ):
    return(
        db.query(Lecturer_Publication)
        .filter(Lecturer_Publication.lecturer_id == lecturer_id)
        .filter(Lecturer_Publication.publication_year == datetime.now().year - 1)
        .all()
    )

def all_course_students(db: Session, course_id: int, lecturer_id: int):
    return(
        db.query(Student)
        .join(Enrolment, Enrolment.student_id == Student.student_id)
        .join(Course_Lecturer, Course_Lecturer.course_id == Enrolment.course_id)
        .join(Lecturer, Lecturer.lectuer_id == Course_Lecturer.lecturer_id)
        .filter(
            Course_Lecturer.course_id == course_id,
            Lecturer.lecturer_id == lecturer_id
        )
        .all()
    )

def expert_lecturers_in_research_area(db: Session, area_of_expertise: str):
    return(
        db.query(Lecturer)
        .filter(Lecturer.area_of_expertise.ilike(f"%{area_of_expertise}%"))
        .all()
    )
