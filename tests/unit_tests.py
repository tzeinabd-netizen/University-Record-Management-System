import os
import uuid
import datetime
import pytest
from sqlalchemy.exc import IntegrityError, OperationalError
from backend.db import engine, SessionLocal

from backend.models import (
    Base, Student, Department, Lecturer, Program, Program_Requirement,
    Course, Course_Schedule, Course_Lecturer, Enrolment, Grade,
    Non_Academic_Staff, Emergency_Contact, Research_Project,
    Research_Project_Member, Lecturer_Qualification, Lecturer_Publication,
    Disciplinary_Record, GraduationStatus
)
 
# ──────────────────────────────────────────────
# PYTEST FIXTURE
# Sets up a clean database session for each test module.
# ──────────────────────────────────────────────

@pytest.fixture(scope="module")
def db_session():
    """MODULE-SCOPED SESSIONL SCHEMA CREATED ONCE, DROPPED AFTER ALL TESTS IN MODULE."""
    Base.metadata.create_all(bind=engine)  # Create tables once for the module
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)  # Clean up after all tests in the module   

# ─────────────────────────────────────────────
# HELPER FUNCTIONS
# These functions create test data with unique identifiers to avoid collisions.
# ─────────────────────────────────────────────

def uid():
    """Generate a short unique identifier to avoid constraint collisions."""
    return str(uuid.uuid4())[:8]

def make_department(session, name=None, faculty="Engineering"):
    """Helper to create a department with a unique name."""
    dept_name = name or f"Dept_{uid()}"
    dept = Department(department_name=dept_name, faculty=faculty)
    session.add(dept)
    session.flush()
    return dept

def make_program(session, name=None, dept=None):
    """Helper to create a program with a unique name."""
    prog = Program(
        program_name=name or f"Program_{uid()}",
        degree_awarded="BSc",
        duration_years=4,
        department_id=dept.department_id if dept else make_department(session).department_id
    )
    session.add(prog)
    session.flush()
    return prog

def make_lecturer(db_session, dept):
    """Helper to create a lecturer with a unique name."""
    lec = Lecturer(
        first_name="Jane",
        last_name="Smith",
        email=f"lecturer_{uid()}@university.com",
        phone=f"555-{uid()}",
        department_id=dept.department_id,
        course_load=3
    )
    db_session.add(lec)
    db_session.flush()
    return lec

def make_student(db_session, prog, lecturer):
    """Helper to create a student with a unique name."""
    student = Student(
        first_name="John",
        last_name="Doe",
        date_of_birth=datetime.date(2000, 1, 1),
        email=f"student_{uid()}@university.com",
        program_id=prog.program_id,
        advisor_id=lecturer.lecturer_id,
        year_of_study=1,
        graduation_status=GraduationStatus.ACTIVE.value

    )
    db_session.add(student)
    db_session.flush()
    return student

def make_course(db_session, dept):
    """Helper to create a course with a unique code."""
    course = Course(
        course_code=f"CS101_{uid()}",
        course_name="Intro to Programming",
        department_id=dept.department_id,
        level=1,
        credits=3
    )
    db_session.add(course)
    db_session.flush()
    return course

# ─────────────────────────────────────────────
# PRE-TEST SETUP
# This section can be used to set up any necessary data or configurations before tests run.
# ─────────────────────────────────────────────

@pytest.fixture()
def dept(db_session):
    """Fixture to create a department for tests that need it."""
    return make_department(db_session)

@pytest.fixture()
def prog(db_session, dept):
    """Fixture to create a program for tests that need it."""
    return make_program(db_session, dept=dept)

@pytest.fixture()
def lecturer(db_session, dept):
    """Fixture to create a lecturer for tests that need it."""
    return make_lecturer(db_session, dept)

@pytest.fixture()
def student(db_session, prog, lecturer):
    """Fixture to create a student for tests that need it."""
    return make_student(db_session, prog, lecturer)

@pytest.fixture()
def course(db_session, dept):
    """Fixture to create a course for tests that need it."""
    return make_course(db_session, dept)    


# == TEST CLASSES ==
# Each class tests a specific model. Tests use the helper functions to create necessary data.
# ==================

# ────────────────────────────────────────────-
# DEPARTMENT TESTS
# ─────────────────────────────────────────────
@pytest.mark.department
class TestDepartment:
    """Tests for the Department Model"""

    @pytest.fixture(autouse=True, scope="class")
    def header(self):
        print("\n" + "="*40)
        print(" TESTING: DEPARTMENT MODEL ")
        print("="*40)

    def test_create_department(self, db_session):
        dept = make_department(db_session)
        assert dept.department_id is not None, (
            "[Deparment] FAILED test_create_department: "
            "department_id should be auto-generated  but got None."
        )
    
    def test_timestamps_auto_generated(self, db_session):
        dept = make_department(db_session)
        assert dept.created_at is not None, (
            "[Department] FAILED test_timestamps_auto_generated: "
            "created_at should be auto-generated but got None."
        )
        assert dept.updated_at is not None, (
            "[Department] FAILED test_timestamps_auto_generated: "
            "updated_at should be auto-generated but got None."
        )

    def test_missing_faculty_raises(self, db_session):
        dept = Department(department_name=f"NoDept_{uid()}")
        db_session.add(dept)
        with pytest.raises(IntegrityError):
            db_session.commit()
        db_session.rollback()

    
    def test_duplicate_name(self, db_session):
        name = f"Unique_{uid()}"
        make_department(db_session, name=name)
        dept2 = Department(department_name=name, faculty="Science")
        db_session.add(dept2)
        with pytest.raises(IntegrityError):
            db_session.commit()
        db_session.rollback()
# ────────────────────────────────────────────-
# PROGRAM TESTS
# ─────────────────────────────────────────────
@pytest.mark.program
class TestProgram:
    """Tests for the Program Model"""

    @pytest.fixture(autouse=True, scope="class")
    def header(self):
        print("\n" + "="*40)
        print(" TESTING: PROGRAM MODEL ")
        print("="*40)

    def test_create_program(self, db_session, dept):
        prog = make_program(db_session, dept=dept)
        assert prog.program_id is not None, (
            "[Program] FAILED test_create_program: "
            "program_id should be auto-generated but got None."
        )
    def test_program_requirements(self, db_session):
        prog = Program(
            program_name=None,
            degree_awarded="BSc",
            duration_years=4,
            department_id=make_department(db_session).department_id
        )
        db_session.add(prog)
        with pytest.raises((IntegrityError, OperationalError)):
            db_session.commit()
        db_session.rollback()

    def test_program_name_unique(self, db_session, dept):
        name = f"UniqueProg_{uid()}"
        make_program(db_session, name=name, dept=dept)
        prog2 = Program(
            program_name=name,
            degree_awarded="BA",
            duration_years=3,
            department_id=dept.department_id
        )
        db_session.add(prog2)
        with pytest.raises(IntegrityError):
            db_session.commit()
        db_session.rollback()
# ────────────────────────────────────────────-
# PROGRAM REQUIREMENT TESTS
# ─────────────────────────────────────────────
@pytest.mark.program_requirement
class TestProgramRequirement:
    """Tests for the Program_Requirement Model"""

    @pytest.fixture(autouse=True, scope="class")
    def header(self):
        print("\n" + "="*40)
        print(" TESTING: PROGRAM REQUIREMENT MODEL ")
        print("="*40)

    def test_create_program_requirement(self, db_session, prog):
        req = Program_Requirement(
            program_id=prog.program_id,
            required_credits=120
        )
        db_session.add(req)
        db_session.commit()
        assert req.requirement_id is not None, (
            "[Program_Requirement] FAILED test_create_program_requirement: "
            "requirement_id should be auto-generated but got None."
        )

    def test_invalid_credit(self, db_session, prog):
        req = Program_Requirement(
            program_id=prog.program_id,
            required_credits=None  # Invalid negative credits
        )
        db_session.add(req)
        with pytest.raises(IntegrityError):
            db_session.commit()
        db_session.rollback()
# ────────────────────────────────────────────-
# LECTURER TESTS
# ────────────────────────────────────────────-
@pytest.mark.lecturer
class TestLecturer:
    """Tests for the Lecturer model."""
 
    @pytest.fixture(autouse=True, scope="class")
    def header(self):
        print("\n" + "=" * 40)
        print("  TESTING: LECTURER MODEL")
        print("=" * 40)
 
    def test_create_lecturer(self, db_session, dept):
        lec = make_lecturer(db_session, dept)
        assert lec.lecturer_id is not None, (
            "[Lecturer] FAILED test_create_lecturer: "
            "Expected lecturer_id to be auto-generated but got None."
        )
 
    def test_duplicate_email_raises(self, db_session, dept):
        email = f"lec_{uid()}@uni.ac"
        lec1 = Lecturer(first_name="A", last_name="B", email=email, department_id=dept.department_id, course_load=1)
        db_session.add(lec1)
        db_session.commit()
 
        lec2 = Lecturer(first_name="C", last_name="D", email=email, department_id=dept.department_id, course_load=1)
        db_session.add(lec2)
        with pytest.raises(IntegrityError):
            db_session.commit()
        db_session.rollback()
 
    def test_negative_course_load_raises(self, db_session, dept):
        lec = Lecturer(
            first_name="X", last_name="Y",
            email=f"lec_{uid()}@uni.ac",
            department_id=dept.department_id,
            course_load=-1
        )
        db_session.add(lec)
        with pytest.raises((IntegrityError, OperationalError)):
            db_session.commit()
        db_session.rollback()
 
    def test_missing_email_raises(self, db_session, dept):
        lec = Lecturer(first_name="A", last_name="B", department_id=dept.department_id, course_load=1)
        db_session.add(lec)
        with pytest.raises(IntegrityError):
            db_session.commit()
        db_session.rollback()
# ────────────────────────────────────────────-
# STUDENT TESTS
# ─────────────────────────────────────────────
@pytest.mark.student
class TestStudent:
    """Tests for the Student Model"""

    @pytest.fixture(autouse=True, scope="class")
    def header(self):
        print("\n" + "="*40)
        print(" TESTING: STUDENT MODEL ")
        print("="*40)

    def test_create_student(self, db_session, prog, lecturer):
        student = make_student(db_session, prog, lecturer)
        assert student.student_id is not None, (
            "[Student] FAILED test_create_student: "
            "student_id should be auto-generated but got None."
        )

    def test_missing_email_raises(self, db_session, prog, lecturer):
        student = Student(
            first_name="John", last_name="Doe",
            date_of_birth=datetime.date(2000, 1, 1),
            program_id=prog.program_id,
            advisor_id=lecturer.lecturer_id,
            year_of_study=1,
            graduation_status="Active"
            # email is omitted
        )
        db_session.add(student)
        with pytest.raises(IntegrityError):
            db_session.commit()
        db_session.rollback()
        
# ────────────────────────────────────────────-
# COURSE TESTS
# ────────────────────────────────────────────-
@pytest.mark.course
class TestCourse:
    """Tests for the Course model."""
 
    @pytest.fixture(autouse=True, scope="class")
    def header(self):
        print("\n" + "=" * 40)
        print("  TESTING: COURSE MODEL")
        print("=" * 40)
 
    def test_create_course(self, db_session, dept):
        course = make_course(db_session, dept)
        assert course.course_id is not None, (
            "[Course] FAILED test_create_course: "
            "Expected course_id to be auto-generated but got None."
        )

    def test_duplicate_course_code_raises(self, db_session, dept):
        code = f"C{uid()}"
        c1 = Course(course_code=code, course_name="C1", department_id=dept.department_id, level=1, credits=3)
        db_session.add(c1)
        db_session.commit()
 
        c2 = Course(course_code=code, course_name="C2", department_id=dept.department_id, level=1, credits=3)
        db_session.add(c2)
        with pytest.raises(IntegrityError):
            db_session.commit()
        db_session.rollback()

    def test_invalid_level_raises(self, db_session, dept):
        c = Course(course_code=f"C{uid()}", course_name="Bad", department_id=dept.department_id, level=0, credits=3)
        db_session.add(c)
        with pytest.raises((IntegrityError, OperationalError)):
            db_session.commit()
        db_session.rollback()
 
    def test_invalid_credits_raises(self, db_session, dept):
        c = Course(course_code=f"C{uid()}", course_name="Bad", department_id=dept.department_id, level=1, credits=0)
        db_session.add(c)
        with pytest.raises((IntegrityError, OperationalError)):
            db_session.commit()
        db_session.rollback()
# ────────────────────────────────────────────-
# COURSE SCHEDULE TESTS
# ────────────────────────────────────────────-
@pytest.mark.course_schedule
class TestCourseSchedule:
    """Tests for the Course_Schedule model."""
 
    @pytest.fixture(autouse=True, scope="class")
    def header(self):
        print("\n" + "=" * 40)
        print("  TESTING: COURSE SCHEDULE MODEL")
        print("=" * 40)
 
    def test_create_schedule(self, db_session, course):
        sched = Course_Schedule(
            course_id=course.course_id,
            day_of_week="Monday",
            start_time="09:00:00",
            end_time="11:00:00",
            room="Room 101",
            class_capacity=30
        )
        db_session.add(sched)
        db_session.commit()
        assert sched.schedule_id is not None, (
            "[Course_Schedule] FAILED test_create_schedule: "
            "Expected schedule_id to be auto-generated but got None."
        )
 
    def test_invalid_time_range_raises(self, db_session, course):
        sched = Course_Schedule(
            course_id=course.course_id,
            day_of_week="Monday",
            start_time="11:00:00",
            end_time="09:00:00",  # end before start
            room="Room 101",
            class_capacity=30
        )
        db_session.add(sched)
        with pytest.raises((IntegrityError, OperationalError)):
            db_session.commit()
        db_session.rollback()
 
    def test_invalid_capacity_raises(self, db_session, course):
        sched = Course_Schedule(
            course_id=course.course_id,
            day_of_week="Tuesday",
            start_time="09:00:00",
            end_time="10:00:00",
            room="Room 102",
            class_capacity=0  # violates ck_class_capacity_positive
        )
        db_session.add(sched)
        with pytest.raises((IntegrityError, OperationalError)):
            db_session.commit()
        db_session.rollback()
# ────────────────────────────────────────────-
# NON-ACADEMIC STAFF TESTS
# ────────────────────────────────────────────-
@pytest.mark.non_academic_staff
class TestNonAcademicStaff:
    """Tests for the Non_Academic_Staff model."""
 
    @pytest.fixture(autouse=True, scope="class")
    def header(self):
        print("\n" + "=" * 40)
        print("  TESTING: NON-ACADEMIC STAFF MODEL")
        print("=" * 40)
 
    def test_create_staff(self, db_session, dept):
        staff = Non_Academic_Staff(
            first_name="Alice",
            last_name="Jones",
            job_title="Administrator",
            department_id=dept.department_id,
            employment_type="Full-Time",
            contract_details="Permanent contract, 40hrs/week",
            salary=30000.00
        )
        db_session.add(staff)
        db_session.commit()
        assert staff.staff_id is not None, (
            "[Non_Academic_Staff] FAILED test_create_staff: "
            "Expected staff_id to be auto-generated but got None."
        )
 
    def test_negative_salary_raises(self, db_session, dept):
        staff = Non_Academic_Staff(
            first_name="Bob", last_name="Hill",
            job_title="Technician",
            department_id=dept.department_id,
            employment_type="Part-Time",
            contract_details="Fixed term, 20hrs/week",
            salary=-500.00
        )
        db_session.add(staff)
        with pytest.raises((IntegrityError, OperationalError)):
            db_session.commit()
        db_session.rollback()
 
    def test_missing_job_title_raises(self, db_session, dept):
        staff = Non_Academic_Staff(
            first_name="Carol", last_name="Fox",
            # job_title intentionally omitted
            department_id=dept.department_id,
            employment_type="Full-Time",
            contract_details="Permanent contract, 40hrs/week",
            salary=25000.00
        )
        db_session.add(staff)
        with pytest.raises(IntegrityError):
            db_session.commit()
        db_session.rollback()
 
    def test_missing_employment_type_raises(self, db_session, dept):
        staff = Non_Academic_Staff(
            first_name="Dave", last_name="Green",
            job_title="Cleaner",
            department_id=dept.department_id,
            # employment_type intentionally omitted
            contract_details="Permanent contract, 40hrs/week",
            salary=20000.00
        )
        db_session.add(staff)
        with pytest.raises(IntegrityError):
            db_session.commit()
        db_session.rollback()
 
    def test_missing_contract_details_raises(self, db_session, dept):
        staff = Non_Academic_Staff(
            first_name="Eve", last_name="White",
            job_title="Security",
            department_id=dept.department_id,
            employment_type="Full-Time",
            # contract_details intentionally omitted
            salary=22000.00
        )
        db_session.add(staff)
        with pytest.raises(IntegrityError):
            db_session.commit()
        db_session.rollback()
# ────────────────────────────────────────────-
# EMERGENCY CONTACT TESTS
# ────────────────────────────────────────────-
@pytest.mark.emergency_contact
class TestEmergencyContact:
    """Tests for the Emergency_Contact model."""
 
    @pytest.fixture(autouse=True, scope="class")
    def header(self):
        print("\n" + "=" * 40)
        print("  TESTING: EMERGENCY CONTACT MODEL")
        print("=" * 40)
 
    def test_create_contact_for_student(self, db_session, student):
        ec = Emergency_Contact(
            first_name="Parent",
            last_name="Smith",
            phone=f"07{uid()}",
            relationship_to_person="Parent",
            student_id=student.student_id
        )
        db_session.add(ec)
        db_session.commit()
        assert ec.emergency_contact_id is not None, (
            "[Emergency_Contact] FAILED test_create_contact_for_student: "
            "Expected emergency_contact_id to be auto-generated but got None."
        )
 
    def test_create_contact_for_lecturer(self, db_session, lecturer):
        ec = Emergency_Contact(
            first_name="Spouse",
            last_name="Doe",
            phone=f"07{uid()}",
            relationship_to_person="Spouse",
            lecturer_id=lecturer.lecturer_id
        )
        db_session.add(ec)
        db_session.commit()
        assert ec.emergency_contact_id is not None, (
            "[Emergency_Contact] FAILED test_create_contact_for_lecturer: "
            "Expected emergency_contact_id to be auto-generated but got None."
        )
 
    def test_multiple_persons_raises(self, db_session, student, lecturer):
        ec = Emergency_Contact(
            first_name="Parent",
            last_name="Smith",
            phone=f"07{uid()}",
            relationship_to_person="Parent",
            student_id=student.student_id,
            lecturer_id=lecturer.lecturer_id  # both set — violates ck_exactly_one_person
        )
        db_session.add(ec)
        with pytest.raises((IntegrityError, OperationalError)):
            db_session.commit()
        db_session.rollback()
 
    def test_missing_phone_raises(self, db_session, student):
        ec = Emergency_Contact(
            first_name="Parent",
            last_name="Smith",
            # phone intentionally omitted
            relationship_to_person="Parent",
            student_id=student.student_id
        )
        db_session.add(ec)
        with pytest.raises(IntegrityError):
            db_session.commit()
        db_session.rollback()
 
    def test_missing_relationship_raises(self, db_session, student):
        ec = Emergency_Contact(
            first_name="Parent",
            last_name="Smith",
            phone=f"07{uid()}",
            # relationship_to_person intentionally omitted
            student_id=student.student_id
        )
        db_session.add(ec)
        with pytest.raises(IntegrityError):
            db_session.commit()
        db_session.rollback()
# ────────────────────────────────────────────-
# ENROLLMENT TESTS
# ────────────────────────────────────────────-
@pytest.mark.enrolment
class TestEnrolment:
    """Tests for the Enrolment model."""
 
    @pytest.fixture(autouse=True, scope="class")
    def header(self):
        print("\n" + "=" * 40)
        print("  TESTING: ENROLMENT MODEL")
        print("=" * 40)
 
    def test_create_enrolment(self, db_session, student, course):
        enrolment = Enrolment(
            student_id=student.student_id,
            course_id=course.course_id,
            semester="Fall",
            academic_year="2024/25",
            enrolment_status="Enrolled"
        )
        db_session.add(enrolment)
        db_session.commit()
        assert enrolment.enrolment_id is not None, (
            "[Enrolment] FAILED test_create_enrolment: "
            "Expected enrolment_id to be auto-generated but got None."
        )
 
    def test_enrolment_requires_valid_student(self, db_session, course):
        enrolment = Enrolment(
            student_id=999999,  # non-existent FK
            course_id=course.course_id,
            semester="Fall",
            academic_year="2024/25",
            enrolment_status="Enrolled"
        )
        db_session.add(enrolment)
        with pytest.raises((IntegrityError, OperationalError)):
            db_session.commit()
        db_session.rollback()
 
    def test_missing_semester_raises(self, db_session, student, course):
        enrolment = Enrolment(
            student_id=student.student_id,
            course_id=course.course_id,
            # semester intentionally omitted
            academic_year="2024/25",
            enrolment_status="Enrolled"
        )
        db_session.add(enrolment)
        with pytest.raises(IntegrityError):
            db_session.commit()
        db_session.rollback()
 
    def test_missing_academic_year_raises(self, db_session, student, course):
        enrolment = Enrolment(
            student_id=student.student_id,
            course_id=course.course_id,
            semester="Fall",
            # academic_year intentionally omitted
            enrolment_status="Enrolled"
        )
        db_session.add(enrolment)
        with pytest.raises(IntegrityError):
            db_session.commit()
        db_session.rollback()
# ────────────────────────────────────────────-
# GRADE TESTS
# ────────────────────────────────────────────-
@pytest.mark.grade
class TestGrade:
    """Tests for the Grade model."""
 
    @pytest.fixture(autouse=True, scope="class")
    def header(self):
        print("\n" + "=" * 40)
        print("  TESTING: GRADE MODEL")
        print("=" * 40)
 
    def test_create_grade(self, db_session, student, course):
        grade = Grade(
            student_id=student.student_id,
            course_id=course.course_id,
            grade_percentage=75.50,
            grade_date=datetime.date(2025, 5, 1)
        )
        db_session.add(grade)
        db_session.commit()
        assert grade.grade_id is not None, (
            "[Grade] FAILED test_create_grade: "
            "Expected grade_id to be auto-generated but got None."
        )
 
    def test_missing_grade_date_raises(self, db_session, student, course):
        grade = Grade(
            student_id=student.student_id,
            course_id=course.course_id,
            grade_percentage=75.50
            # grade_date intentionally omitted
        )
        db_session.add(grade)
        with pytest.raises(IntegrityError):
            db_session.commit()
        db_session.rollback()
 
    def test_grade_above_100_raises(self, db_session, student, course):
        grade = Grade(
            student_id=student.student_id,
            course_id=course.course_id,
            grade_percentage=110.00,
            grade_date=datetime.date(2025, 5, 1)
        )
        db_session.add(grade)
        with pytest.raises((IntegrityError, OperationalError)):
            db_session.commit()
        db_session.rollback()
 
    def test_negative_grade_raises(self, db_session, student, course):
        grade = Grade(
            student_id=student.student_id,
            course_id=course.course_id,
            grade_percentage=-5.00,
            grade_date=datetime.date(2025, 5, 1)
        )
        db_session.add(grade)
        with pytest.raises((IntegrityError, OperationalError)):
            db_session.commit()
        db_session.rollback()
# ────────────────────────────────────────────-
# RESEARCH PROJECT TESTS
# ────────────────────────────────────────────-
@pytest.mark.research_project
class TestResearchProject:
    """Tests for the Research_Project model."""
 
    @pytest.fixture(autouse=True, scope="class")
    def header(self):
        print("\n" + "=" * 40)
        print("  TESTING: RESEARCH PROJECT MODEL")
        print("=" * 40)
 
    def test_create_project(self, db_session, lecturer):
        project = Research_Project(
            project_title=f"Project_{uid()}",
            principal_investigator_id=lecturer.lecturer_id,
            start_date=datetime.date(2024, 1, 1)
        )
        db_session.add(project)
        db_session.commit()
        assert project.project_id is not None, (
            "[Research_Project] FAILED test_create_project: "
            "Expected project_id to be auto-generated but got None."
        )
 
    def test_missing_start_date_raises(self, db_session, lecturer):
        project = Research_Project(
            project_title=f"Project_{uid()}",
            principal_investigator_id=lecturer.lecturer_id
            # start_date intentionally omitted
        )
        db_session.add(project)
        with pytest.raises(IntegrityError):
            db_session.commit()
        db_session.rollback()
 
    def test_missing_title_raises(self, db_session, lecturer):
        project = Research_Project(
            # project_title intentionally omitted
            principal_investigator_id=lecturer.lecturer_id,
            start_date=datetime.date(2024, 1, 1)
        )
        db_session.add(project)
        with pytest.raises(IntegrityError):
            db_session.commit()
        db_session.rollback()
 
    def test_end_before_start_raises(self, db_session, lecturer):
        project = Research_Project(
            project_title=f"Project_{uid()}",
            principal_investigator_id=lecturer.lecturer_id,
            start_date=datetime.date(2024, 6, 1),
            end_date=datetime.date(2024, 1, 1)  # end before start
        )
        db_session.add(project)
        with pytest.raises((IntegrityError, OperationalError)):
            db_session.commit()
        db_session.rollback()
# ────────────────────────────────────────────-
# DISCIPLINARY RECORD TESTS
# ────────────────────────────────────────────-
@pytest.mark.disciplinary_record
class TestDisciplinaryRecord:
    """Tests for the Disciplinary_Record model."""
 
    @pytest.fixture(autouse=True, scope="class")
    def header(self):
        print("\n" + "=" * 40)
        print("  TESTING: DISCIPLINARY RECORD MODEL")
        print("=" * 40)
 
    def test_create_record(self, db_session, student):
        record = Disciplinary_Record(
            student_id=student.student_id,
            incident_date=datetime.date(2025, 3, 10),
            description="Missed exam without notice.",
            action_taken="Formal warning issued."
        )
        db_session.add(record)
        db_session.commit()
        assert record.record_id is not None, (
            "[Disciplinary_Record] FAILED test_create_record: "
            "Expected record_id to be auto-generated but got None."
        )
 
    def test_missing_description_raises(self, db_session, student):
        record = Disciplinary_Record(
            student_id=student.student_id,
            incident_date=datetime.date(2025, 3, 10),
            # description intentionally omitted
            action_taken="Warning issued."
        )
        db_session.add(record)
        with pytest.raises(IntegrityError):
            db_session.commit()
        db_session.rollback()
 
    def test_missing_action_taken_raises(self, db_session, student):
        record = Disciplinary_Record(
            student_id=student.student_id,
            incident_date=datetime.date(2025, 3, 10),
            description="Cheating in exam."
            # action_taken intentionally omitted
        )
        db_session.add(record)
        with pytest.raises(IntegrityError):
            db_session.commit()
        db_session.rollback()
 
    def test_missing_incident_date_raises(self, db_session, student):
        record = Disciplinary_Record(
            student_id=student.student_id,
            # incident_date intentionally omitted
            description="Cheating in exam.",
            action_taken="Suspension."
        )
        db_session.add(record)
        with pytest.raises(IntegrityError):
            db_session.commit()
        db_session.rollback()
# ────────────────────────────────────────────-
# LECTURER QUALIFICATION TESTS
# ────────────────────────────────────────────-
@pytest.mark.lecturer_qualification
class TestLecturerQualification:
    """Tests for the Lecturer_Qualification model."""
 
    @pytest.fixture(autouse=True, scope="class")
    def header(self):
        print("\n" + "=" * 40)
        print("  TESTING: LECTURER QUALIFICATION MODEL")
        print("=" * 40)
 
    def test_create_qualification(self, db_session, lecturer):
        qual = Lecturer_Qualification(
            lecturer_id=lecturer.lecturer_id,
            qualification_name="PhD Computer Science",
            institution="MIT",
            year_awarded=2015
        )
        db_session.add(qual)
        db_session.commit()
        assert qual.qualification_id is not None, (
            "[Lecturer_Qualification] FAILED test_create_qualification: "
            "Expected qualification_id to be auto-generated but got None."
        )
 
    def test_year_before_1900_raises(self, db_session, lecturer):
        qual = Lecturer_Qualification(
            lecturer_id=lecturer.lecturer_id,
            qualification_name="BSc",
            institution="Oxford",
            year_awarded=1800  # violates ck_valid_year_awarded
        )
        db_session.add(qual)
        with pytest.raises((IntegrityError, OperationalError)):
            db_session.commit()
        db_session.rollback()
# ────────────────────────────────────────────-
# LECTURER PUBLICATION TESTS
# ────────────────────────────────────────────-
@pytest.mark.lecturer_publication
class TestLecturerPublication:
    """Tests for the Lecturer_Publication model."""
 
    @pytest.fixture(autouse=True, scope="class")
    def header(self):
        print("\n" + "=" * 40)
        print("  TESTING: LECTURER PUBLICATION MODEL")
        print("=" * 40)
 
    def test_create_publication(self, db_session, lecturer):
        pub = Lecturer_Publication(
            lecturer_id=lecturer.lecturer_id,
            publication_title="Deep Learning in Robotics",
            publication_year=2022,
            publication_type="Journal Article",
            journal_or_conference="IEEE Transactions"
        )
        db_session.add(pub)
        db_session.commit()
        assert pub.publication_id is not None, (
            "[Lecturer_Publication] FAILED test_create_publication: "
            "Expected publication_id to be auto-generated but got None."
        )
 
    def test_year_before_1900_raises(self, db_session, lecturer):
        pub = Lecturer_Publication(
            lecturer_id=lecturer.lecturer_id,
            publication_title="Old Paper",
            publication_year=1850,  # violates ck_publication_year
            publication_type="Book",
            journal_or_conference="N/A"
        )
        db_session.add(pub)
        with pytest.raises((IntegrityError, OperationalError)):
            db_session.commit()
        db_session.rollback()
# ────────────────────────────────────────────-
# RESEARCH PROJECT MEMBER TESTS
# ────────────────────────────────────────────-
@pytest.mark.research_project_member
class TestResearchProjectMember:
    """Tests for the Research_Project_Member model."""
 
    @pytest.fixture(autouse=True, scope="class")
    def header(self):
        print("\n" + "=" * 40)
        print("  TESTING: RESEARCH PROJECT MEMBER MODEL")
        print("=" * 40)
 
    @pytest.fixture()
    def project(self, db_session, lecturer):
        """Creates a fresh research project for each test in this class."""
        p = Research_Project(
            project_title=f"Proj_{uid()}",
            principal_investigator_id=lecturer.lecturer_id,
            start_date=datetime.date(2024, 1, 1)
        )
        db_session.add(p)
        db_session.commit()
        return p
 
    def test_add_lecturer_as_member(self, db_session, lecturer, project):
        member = Research_Project_Member(
            project_id=project.project_id,
            lecturer_id=lecturer.lecturer_id,
            member_role="Project Leader"
        )
        db_session.add(member)
        db_session.commit()
        assert member.membership_id is not None, (
            "[Research_Project_Member] FAILED test_add_lecturer_as_member: "
            "Expected membership_id to be auto-generated but got None."
        )
 
    def test_add_student_as_member(self, db_session, student, project):
        member = Research_Project_Member(
            project_id=project.project_id,
            student_id=student.student_id,
            member_role="Student"
        )
        db_session.add(member)
        db_session.commit()
        assert member.membership_id is not None, (
            "[Research_Project_Member] FAILED test_add_student_as_member: "
            "Expected membership_id to be auto-generated but got None."
        )
 
    def test_both_lecturer_and_student_raises(self, db_session, lecturer, student, project):
        member = Research_Project_Member(
            project_id=project.project_id,
            lecturer_id=lecturer.lecturer_id,
            student_id=student.student_id,  # both set — violates valid_member_check
            member_role="Project Leader"
        )
        db_session.add(member)
        with pytest.raises((IntegrityError, OperationalError)):
            db_session.commit()
        db_session.rollback()
