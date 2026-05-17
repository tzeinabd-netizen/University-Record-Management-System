import os
import uuid
import datetime
import pytest
from sqlalchemy.exc import IntegrityError, OperationalError
from src.db import engine, SessionLocal


from src.models import (
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
    dept = Department(department_name=dept_name, faculty="Engineering")
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
        phone_number="1234567890",
        department_id=dept.department_id
        ,
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


# ─────────────────────────────────────────────
# TEST CLASSES
# Each class tests a specific model. Tests use the helper functions to create necessary data.
# ─────────────────────────────────────────────


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



