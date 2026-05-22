from sqlalchemy.orm import Session
from sqlalchemy import case, text, literal
from sqlalchemy.sql import func
from models import *
 
 
# Query 1: Find all students enrolled in a specific course taught by a particular lecturer.
def all_course_students(db: Session, course_name: str, lecturer_last_name: str):
    return (
        db.query(
            Student.first_name.label("student_first_name"),
            Student.last_name.label("student_last_name"),
            Course.course_name,
            Lecturer.first_name.label("lecturer_first_name"),
            Lecturer.last_name.label("lecturer_last_name"),
        )
        .select_from(Student)
        .join(Enrolment,       Enrolment.student_id       == Student.student_id)
        .join(Course,          Course.course_id            == Enrolment.course_id)
        .join(Course_Lecturer, Course_Lecturer.course_id   == Course.course_id)
        .join(Lecturer,        Lecturer.lecturer_id        == Course_Lecturer.lecturer_id)
        .filter(
            Course.course_name == course_name,
            Lecturer.last_name == lecturer_last_name,
        )
        .all()
    )
 
 
# Query 2: List all final-year students with an average grade above 70%.
def final_year_students_above_70(db: Session):
    return (
        db.query(
            Student.student_id,
            Student.first_name,
            Student.last_name,
            Student.year_of_study,
            func.round(func.avg(Grade.grade_percentage), 2).label("average_grade"),
        )
        .select_from(Student)
        .join(Grade, Grade.student_id == Student.student_id)
        .filter(Student.year_of_study == 4)
        .group_by(
            Student.student_id,
            Student.first_name,
            Student.last_name,
            Student.year_of_study,
        )
        .having(func.avg(Grade.grade_percentage) > 70)
        .all()
    )
 
 
# Query 3: Identify students who have not registered for any courses.
def students_not_enrolled(db: Session):
    return (
        db.query(
            Student.student_id,
            Student.first_name,
            Student.last_name,
        )
        .select_from(Student)
        .outerjoin(Enrolment, Enrolment.student_id == Student.student_id)
        .filter(Enrolment.student_id.is_(None))
        .all()
    )
 
 
# Query 4: Retrieve the contact information for the faculty advisor of a specific student.
def student_faculty_advisor_information(db: Session, student_last_name: str):
    return (
        db.query(
            Student.first_name.label("student_first_name"),
            Student.last_name.label("student_last_name"),
            Lecturer.first_name.label("advisor_first_name"),
            Lecturer.last_name.label("advisor_last_name"),
            Lecturer.email,
            Lecturer.phone,
        )
        .select_from(Student)
        .join(Lecturer, Lecturer.lecturer_id == Student.advisor_id)
        .filter(Student.last_name == student_last_name)
        .first()
    )
 
 
# Query 5: Generate a report on the publications of lecturers in the past year.
def lecturer_publications_report(db: Session, publication_year: int):
    return (
        db.query(
            Lecturer.first_name,
            Lecturer.last_name,
            Lecturer_Publication.publication_title,
            Lecturer_Publication.publication_year,
            Lecturer_Publication.publication_type,
            Lecturer_Publication.journal_or_conference,
        )
        .select_from(Lecturer)
        .join(Lecturer_Publication, Lecturer_Publication.lecturer_id == Lecturer.lecturer_id)
        .filter(Lecturer_Publication.publication_year == publication_year)
        .order_by(Lecturer.last_name, Lecturer_Publication.publication_title)
        .all()
    )
 
 
# Query 6: Identify students who failed at least one course (grade < 40%).
def students_failed_courses(db: Session):
    return (
        db.query(
            Student.first_name.label("student_first_name"),
            Student.last_name.label("student_last_name"),
            Course.course_name,
            Grade.grade_percentage,
        )
        .select_from(Student)
        .join(Grade,  Grade.student_id  == Student.student_id)
        .join(Course, Course.course_id  == Grade.course_id)
        .filter(Grade.grade_percentage < 40)
        .order_by(Grade.grade_percentage.asc())
        .all()
    )
 
 
# Query 7: Identify the top-performing courses based on average student grades.
def top_performing_courses(db: Session):
    return (
        db.query(
            Course.course_name,
            func.round(func.avg(Grade.grade_percentage), 2).label("average_course_grade"),
        )
        .select_from(Course)
        .join(Grade, Grade.course_id == Course.course_id)
        .group_by(Course.course_id, Course.course_name)
        .order_by(func.avg(Grade.grade_percentage).desc())
        .all()
    )
 
 
# Query 8: Identify students and lecturers involved in research projects.
def research_project_members(db: Session):
    member_name = func.coalesce(
        func.concat(Lecturer.first_name, literal(" "), Lecturer.last_name),
        func.concat(Student.first_name,  literal(" "), Student.last_name),
    ).label("member_name")
 
    member_type = case(
        (Lecturer.lecturer_id.isnot(None), "Lecturer"),
        (Student.student_id.isnot(None),   "Student"),
        else_="n/a",
    ).label("member_type")
 
    return (
        db.query(
            Research_Project.project_title,
            member_name,
            Research_Project_Member.member_role,
            member_type,
        )
        .select_from(Research_Project_Member)
        .join(Research_Project,
              Research_Project.project_id    == Research_Project_Member.project_id)
        .outerjoin(Lecturer,
                   Lecturer.lecturer_id      == Research_Project_Member.lecturer_id)
        .outerjoin(Student,
                   Student.student_id        == Research_Project_Member.student_id)
        .order_by(Research_Project.project_title)
        .all()
    )
 
 
# Query 9: Course popularity statistics with ranking.
def course_popularity_stats(db: Session):
    return db.execute(text("""
        WITH course_stats AS (
            SELECT
                c.course_id,
                c.course_name,
                COUNT(e.enrolment_id)        AS number_enrolments,
                COUNT(DISTINCT e.student_id) AS course_size
            FROM courses c
            LEFT JOIN enrolments e ON c.course_id = e.course_id
            GROUP BY c.course_id, c.course_name
        )
        SELECT
            course_id,
            course_name,
            number_enrolments,
            course_size,
            RANK() OVER (ORDER BY course_size DESC) AS course_ranking
        FROM course_stats
    """)).fetchall()
 
 
# Query 10: Lecturer workload statistics with ranking.
def lecturer_workload_stats(db: Session):
    return db.execute(text("""
        WITH lecturer_stats AS (
            SELECT
                l.lecturer_id,
                l.first_name,
                l.last_name,
                COUNT(DISTINCT e.student_id) AS students_taught,
                COUNT(DISTINCT cl.course_id) AS courses_taught
            FROM lecturers l
            LEFT JOIN course_lecturers cl ON l.lecturer_id = cl.lecturer_id
            LEFT JOIN enrolments e        ON cl.course_id  = e.course_id
            GROUP BY l.lecturer_id, l.first_name, l.last_name
        )
        SELECT
            lecturer_id,
            first_name,
            last_name,
            students_taught,
            courses_taught,
            RANK() OVER (ORDER BY students_taught DESC) AS lecturer_ranking
        FROM lecturer_stats
    """)).fetchall()
 
  
def display_all_student_records(db: Session):
    return db.query(Student).all()
 
def display_all_course_records(db: Session):
    return db.query(Course).all()
 
def display_all_lecturer_records(db: Session):
    return db.query(Lecturer).all()
