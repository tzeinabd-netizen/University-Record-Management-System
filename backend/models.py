from sqlalchemy import Column, Integer, String, Date, Text, TIMESTAMP, ForeignKey, CheckConstraint, DECIMAL, Time
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .db import Base, engine
import enum

class GraduationStatus(enum.Enum):
    ACTIVE             = "Active"
    PENDING_GRADUATION = "Pending Graduation"
    GRADUATED          = "Graduated"
    WITHDRAWN          = "Withdrawn"

class Department(Base):
    __tablename__= "departments"

    department_id= Column(Integer, primary_key= True, autoincrement= True)
    department_name= Column(String(100), nullable= False, unique=True)
    faculty= Column(String(100), nullable= False)
    research_area = Column(String(150))
    created_at= Column(TIMESTAMP, server_default=func.now())
    updated_at= Column(TIMESTAMP, server_default= func.now(), onupdate=func.now())
    
    programs= relationship("Program", back_populates="department")
    lecturers= relationship("Lecturer", back_populates="department")
    non_academic_staff = relationship("Non_Academic_Staff", back_populates="department")
    courses= relationship('Course', back_populates="department")

class Program(Base):
    __tablename__= "programs"
    
    # __table_args__ = (
        #CheckConstraint("duration_years > 0 AND duration_years <= 10", name="valid_duration"),
        #CheckConstraint("degree_awarded IN ('BSc, MSc, 'PhD')", name="valid_degree")
    #)

    program_id= Column(Integer, primary_key= True, autoincrement= True)
    program_name= Column(String(100), nullable= False, unique=True)
    degree_awarded= Column(String(100), nullable= False) 
    duration_years= Column(Integer, nullable= False) 
    department_id= Column(Integer, ForeignKey("departments.department_id", ondelete="CASCADE"), nullable=False)
    created_at= Column(TIMESTAMP, server_default=func.now())
    updated_at= Column(TIMESTAMP, server_default= func.now(), onupdate=func.now())

    #Relationships
    department= relationship("Department", back_populates= "programs")
    students= relationship("Student", back_populates="program")
    program_requirement=relationship("Program_Requirement", back_populates="program", uselist=False)

class Program_Requirement(Base):
    __tablename__="program_requirements"

    requirement_id= Column(Integer, primary_key=True, autoincrement=True)
    program_id= Column(Integer, ForeignKey("programs.program_id", ondelete="CASCADE"), nullable=False)
    required_credits= Column(Integer, nullable=False)
    minimum_pass_mark= Column(DECIMAL(5, 2), nullable=False, server_default="40.00")
    created_at= Column(TIMESTAMP, server_default=func.now())
    updated_at= Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    #Relationships
    program= relationship("Program", back_populates="program_requirement")

    __table_args__ = (
        CheckConstraint("required_credits > 0",name="ck_required_credits_positive"),
        CheckConstraint("minimum_pass_mark >= 0 AND minimum_pass_mark <= 100", name="ck_pass_mark_range"),
    )


class Lecturer(Base):
    __tablename__= "lecturers"

    lecturer_id= Column(Integer, primary_key= True, autoincrement= True)
    first_name= Column(String(50), nullable= False)
    last_name= Column(String(50), nullable= False)
    email= Column(String(100), unique= True, nullable= False)
    phone= Column(String(20), unique=True)
    department_id= Column(Integer, ForeignKey("departments.department_id", ondelete="CASCADE"), nullable= False)
    area_of_expertise= Column(String(150))
    course_load= Column(Integer) #nullable= False once DB updated
    research_interest= Column(String(150))
    created_at= Column(TIMESTAMP, server_default=func.now())
    updated_at= Column(TIMESTAMP, server_default= func.now(), onupdate=func.now())

    #Relationships
    department= relationship("Department", back_populates= "lecturers")
    students= relationship("Student", back_populates="advisor")
    research_projects= relationship("Research_Project", back_populates="principal_investigator")
    course_lecturer= relationship("Course_Lecturer", back_populates="lecturer")
    lecturer_qualification= relationship("Lecturer_Qualification", back_populates="lecturer")
    lecturer_publication= relationship("Lecturer_Publication", back_populates="lecturer")
    research_project_members = relationship("Research_Project_Member", back_populates="lecturer")
    emergency_contacts= relationship("Emergency_Contact", back_populates="lecturer")

    __table_args__ = (
        CheckConstraint("course_load >= 0", name="ck_course_load_non_negative"),
    )


class Student(Base):
    __tablename__="students"

    student_id= Column(Integer, primary_key=True, autoincrement=True)
    first_name= Column(String(50), nullable=False)
    last_name= Column(String(50), nullable=False)
    date_of_birth= Column(Date, nullable=False)
    email= Column(String(100), unique=True, nullable=False)
    phone= Column(String(20), unique=True)
    program_id= Column(Integer, ForeignKey("programs.program_id", ondelete= "CASCADE"), nullable=False)
    advisor_id= Column(Integer, ForeignKey("lecturers.lecturer_id", ondelete="CASCADE"), nullable=True)
    year_of_study= Column(Integer, nullable=False)
    graduation_status= Column(String(50), nullable=False)
    created_at= Column(TIMESTAMP, server_default=func.now())
    updated_at= Column(TIMESTAMP, server_default= func.now(), onupdate=func.now())

    #Relationships
    program= relationship("Program", back_populates="students")
    advisor= relationship("Lecturer", back_populates="students")
    enrolments = relationship("Enrolment", back_populates="student")
    grades = relationship("Grade", back_populates="student")
    disciplinary_records= relationship("Disciplinary_Record", back_populates="student")
    research_project_members = relationship("Research_Project_Member", back_populates="student")
    emergency_contacts= relationship("Emergency_Contact", back_populates="student")

    __table_args__ = (
        CheckConstraint("year_of_study > 0", name="ck_year_of_study_positive"),
    )

class Non_Academic_Staff(Base):
    __tablename__="non_academic_staff"

    staff_id= Column(Integer, primary_key=True, autoincrement=True)
    first_name= Column(String(50), nullable=False)
    last_name= Column(String(50), nullable=False)
    job_title= Column(String(100), nullable=False)
    department_id= Column(Integer, ForeignKey("departments.department_id", ondelete="CASCADE"), nullable=False)
    employment_type = Column(String(50), nullable=False) #add a nullable=False once the db is updated
    contract_details= Column(String(150), nullable=False) #Own seperate class to be updated once made
    salary= Column(DECIMAL(10, 2), nullable=False)
    created_at= Column(TIMESTAMP, server_default=func.now())
    updated_at= Column(TIMESTAMP, server_default= func.now(), onupdate=func.now())

   

    #Relationships
    department= relationship('Department', back_populates="non_academic_staff")
    emergency_contacts= relationship("Emergency_Contact", back_populates="staff")

    __table_args__ = (
        CheckConstraint("salary >= 0", name="ck_salary"),
    )

class Emergency_Contact(Base):
    __tablename__="emergency_contacts"

    emergency_contact_id= Column(Integer, primary_key=True, autoincrement=True)
    first_name= Column(String(50), nullable=False)
    last_name= Column(String(50), nullable=False)
    phone= Column(String(20), nullable=False)
    relationship_to_person= Column(String(50), nullable=False)
    student_id= Column(Integer, ForeignKey("students.student_id", ondelete="CASCADE"), nullable=True)
    lecturer_id= Column(Integer, ForeignKey("lecturers.lecturer_id", ondelete="CASCADE"), nullable=True)
    staff_id= Column(Integer, ForeignKey("non_academic_staff.staff_id", ondelete="CASCADE"), nullable=True)
    created_at= Column(TIMESTAMP, server_default=func.now())
    updated_at= Column(TIMESTAMP, server_default= func.now(), onupdate=func.now())

    #Relationships
    student= relationship("Student", back_populates="emergency_contacts")
    lecturer= relationship("Lecturer", back_populates="emergency_contacts")
    staff= relationship("Non_Academic_Staff", back_populates="emergency_contacts")

    __table_args__ = (
        CheckConstraint(
            "(student_id IS NOT NULL AND lecturer_id IS NULL AND staff_id IS NULL) OR "
            "(student_id IS NULL AND lecturer_id IS NOT NULL AND staff_id IS NULL) OR "
            "(student_id IS NULL AND lecturer_id IS NULL AND staff_id IS NOT NULL)",
            name="ck_exactly_one_person"
        ),
    )

class Course(Base):
    __tablename__="courses"

    course_id= Column(Integer, primary_key=True, autoincrement=True)
    course_code= Column(String(20), unique=True, nullable=False)
    course_name= Column(String(100), nullable=False)
    description= Column(Text)
    department_id= Column(Integer, ForeignKey("departments.department_id", ondelete="CASCADE"), nullable=False)
    level= Column(Integer, nullable=False)
    credits= Column(Integer, nullable=False)
    prerequisites= Column(String(150))
    created_at= Column(TIMESTAMP, server_default=func.now())
    updated_at= Column(TIMESTAMP, server_default= func.now(), onupdate=func.now())

    #Relationships
    department= relationship('Department', back_populates= "courses")
    enrolments = relationship("Enrolment", back_populates="course")
    course_lecturer= relationship("Course_Lecturer", back_populates="course")
    grades = relationship("Grade", back_populates="course")
    course_schedules = relationship("Course_Schedule", back_populates="course")

    __table_args__ = (
        CheckConstraint("credits > 0", name="valid_credits"),
        CheckConstraint("level > 0", name="valid_level"), #level from undergraduate to PhD
    )

class Course_Schedule(Base):
    __tablename__="course_schedules"

    schedule_id= Column(Integer, primary_key=True, autoincrement=True)
    course_id= Column(Integer, ForeignKey("courses.course_id", ondelete="CASCADE"), nullable=False)
    day_of_week= Column(String(20), nullable=False)
    start_time= Column(Time, nullable=False)
    end_time= Column(Time, nullable=False)
    room= Column(String(50), nullable=False)
    class_capacity= Column(Integer, nullable=False)
    created_at= Column(TIMESTAMP, server_default=func.now())
    updated_at= Column(TIMESTAMP, server_default= func.now(), onupdate=func.now())

    #Relationships
    course= relationship("Course", back_populates="course_schedules")

    __table_args__ = (
        CheckConstraint("class_capacity > 0",name="ck_class_capacity_positive"),
        CheckConstraint("start_time < end_time",name="ck_valid_time_range"),
    )

class Research_Project(Base):
    __tablename__="research_projects"

    project_id= Column(Integer, primary_key=True, autoincrement=True)
    project_title= Column(String(150), nullable=False)
    principal_investigator_id= Column(Integer, ForeignKey("lecturers.lecturer_id", ondelete="CASCADE"), nullable=False)
    funding_source= Column(String(150))
    outcome= Column(Text)
    start_date= Column(Date, nullable=False)
    end_date= Column(Date)
    created_at= Column(TIMESTAMP, server_default=func.now())
    updated_at= Column(TIMESTAMP, server_default= func.now(), onupdate=func.now())

    __table_args__ = (
        CheckConstraint("end_date IS NULL OR end_date >= start_date", name="ck_valid_dates"),
    )

    #Relationships
    principal_investigator= relationship("Lecturer", back_populates="research_projects")
    research_project_members = relationship("Research_Project_Member", back_populates="research_project")

class Enrolment(Base):
    __tablename__="enrolments"

    #__table_args__= (
        #CheckConstraint("semester IN('Fall', 'Spring', 'Summer')", name="valid-semester"),
        #CheckConstraint("enrolment_status IN ('Not enroled', 'Enroled', 'On Sabbatical')")
    #)

    enrolment_id= Column(Integer, primary_key=True, autoincrement=True)
    student_id= Column(Integer, ForeignKey("students.student_id", ondelete="CASCADE"), nullable=False)
    course_id= Column(Integer, ForeignKey("courses.course_id", ondelete="CASCADE"), nullable=False)
    semester= Column(String(50), nullable=False) #needs a nullable=False
    academic_year= Column(String(20), nullable=False)
    enrolment_status= Column(String(50), nullable=False) # needs a nullable=False
    created_at= Column(TIMESTAMP, server_default=func.now())
    updated_at= Column(TIMESTAMP, server_default= func.now(), onupdate=func.now())

    #Relationships
    student = relationship("Student", back_populates="enrolments")
    course = relationship("Course", back_populates="enrolments")

class Course_Lecturer(Base):
    __tablename__="course_lecturers"

    course_id= Column(Integer, ForeignKey("courses.course_id", ondelete="CASCADE"), primary_key=True)
    lecturer_id= Column(Integer, ForeignKey("lecturers.lecturer_id", ondelete="CASCADE"), primary_key=True)
    created_at= Column(TIMESTAMP, server_default=func.now())
    updated_at= Column(TIMESTAMP, server_default= func.now(), onupdate=func.now())

    #Relationships
    course= relationship("Course", back_populates="course_lecturer")
    lecturer= relationship("Lecturer", back_populates="course_lecturer")

class Grade(Base):
    __tablename__="grades"

    grade_id= Column(Integer, primary_key=True, autoincrement=True)
    student_id= Column(Integer, ForeignKey("students.student_id", ondelete="CASCADE"), nullable=False)
    course_id= Column(Integer, ForeignKey("courses.course_id", ondelete="CASCADE"), nullable=False)
    grade_percentage= Column(DECIMAL(5,2), nullable=False)
    grade_date= Column(Date, nullable=False)
    created_at= Column(TIMESTAMP, server_default=func.now())
    updated_at= Column(TIMESTAMP, server_default= func.now(), onupdate=func.now())

    #Relationships
    student = relationship("Student", back_populates="grades")
    course = relationship("Course", back_populates="grades")

    __table_args__= (
        CheckConstraint("grade_percentage >= 0 AND grade_percentage <= 100", name="ck_valid_grade_percentage"),
    )

class Disciplinary_Record(Base):
        __tablename__="disciplinary_records"

        record_id= Column(Integer, primary_key=True, autoincrement=True)
        student_id= Column(Integer, ForeignKey("students.student_id", ondelete="CASCADE"), nullable=False)
        incident_date= Column(Date, nullable=False)
        description= Column(Text, nullable=False)
        action_taken= Column(Text, nullable=False)
        created_at= Column(TIMESTAMP, server_default=func.now())
        updated_at= Column(TIMESTAMP, server_default= func.now(), onupdate=func.now())

        #Relationships
        student= relationship("Student", back_populates="disciplinary_records")

class Lecturer_Qualification(Base):
    __tablename__="lecturer_qualifications"

    qualification_id=Column(Integer, primary_key=True, autoincrement=True)
    lecturer_id= Column(Integer, ForeignKey("lecturers.lecturer_id", ondelete="CASCADE"), nullable=False)
    qualification_name= Column(String(150), nullable=False)
    institution=Column(String(150), nullable=False)
    year_awarded=Column(Integer, nullable=False)
    created_at= Column(TIMESTAMP, server_default=func.now())
    updated_at= Column(TIMESTAMP, server_default= func.now(), onupdate=func.now())

    #Relationships 
    lecturer= relationship("Lecturer", back_populates="lecturer_qualification")

    __table_args__= (
        CheckConstraint("year_awarded >= 1900", name="ck_valid_year_awarded"),
    )

class Lecturer_Publication(Base):
    __tablename__="lecturer_publications"

    #__table_args__= (
        #CheckConstraint("publication_type IN('Journal Article', 'Book', 'Technical Report', 'Patent', 'Conference Paper')")
    #)

    publication_id= Column(Integer, primary_key=True, autoincrement=True)
    lecturer_id=Column(Integer, ForeignKey("lecturers.lecturer_id",ondelete="CASCADE"), nullable=False)
    publication_title= Column(String(200), nullable=False)
    publication_year= Column(Integer, nullable=False) #needs a nullable=False
    publication_type= Column(String(100), nullable=False) #needs a nullable=False
    journal_or_conference= Column(String(150), nullable=False) 
    created_at= Column(TIMESTAMP, server_default=func.now())
    updated_at= Column(TIMESTAMP, server_default= func.now(), onupdate=func.now())

    #Relationships
    lecturer= relationship("Lecturer", back_populates="lecturer_publication")

    __table_args__= (
        CheckConstraint("publication_year >= 1900", name="ck_publication_year"),
    )
 
class Research_Project_Member(Base):
    __tablename__="research_project_members"

    membership_id=Column(Integer, primary_key=True, autoincrement=True)
    project_id=Column(Integer, ForeignKey("research_projects.project_id", ondelete="CASCADE"), nullable=False)
    lecturer_id=Column(Integer, ForeignKey("lecturers.lecturer_id", ondelete="CASCADE"))
    student_id= Column(Integer, ForeignKey("students.student_id", ondelete="CASCADE"))
    member_role= Column(String(100), nullable=False)
    created_at= Column(TIMESTAMP, server_default=func.now())
    updated_at= Column(TIMESTAMP, server_default= func.now(), onupdate=func.now())

    #Relationships
    research_project = relationship("Research_Project", back_populates="research_project_members")
    lecturer = relationship("Lecturer", back_populates="research_project_members", foreign_keys=[lecturer_id])
    student = relationship("Student", back_populates="research_project_members", foreign_keys=[student_id])

    __table_args__ = (
        CheckConstraint("(lecturer_id IS NOT NULL AND student_id IS NULL) OR (lecturer_id IS NULL AND student_id IS NOT NULL)", name="valid_member_check"),
         CheckConstraint(
        "(student_id IS NOT NULL AND member_role = 'Student') OR (lecturer_id IS NOT NULL AND member_role = 'Project Leader')",
        name="valid_member_role"
    ),
    )

Base.metadata.create_all(bind=engine)
