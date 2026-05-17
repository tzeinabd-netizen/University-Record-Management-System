USE university_record_system;

-- Departments table stores information about each academic department within the university.
CREATE TABLE departments (
    department_id INT AUTO_INCREMENT PRIMARY KEY,
    department_name VARCHAR(100) NOT NULL UNIQUE,
    faculty VARCHAR(100) NOT NULL,
    research_area VARCHAR(150),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
        ON UPDATE CURRENT_TIMESTAMP
);

-- Programs table stores academic programmes offered by departments.
CREATE TABLE programs (
    program_id INT AUTO_INCREMENT PRIMARY KEY,
    program_name VARCHAR(100) NOT NULL UNIQUE,
    degree_awarded VARCHAR(100) NOT NULL,
    duration_years INT NOT NULL,
    department_id INT NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
        ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (department_id)
        REFERENCES departments(department_id)
        ON DELETE CASCADE,
        
        CHECK (duration_years > 0 AND duration_years <= 4)
);

-- Program_requirements table to store credit requirements for each programme.
CREATE TABLE program_requirements (
    requirement_id INT AUTO_INCREMENT PRIMARY KEY,
    program_id INT NOT NULL,
    required_credits INT NOT NULL,
    minimum_pass_mark DECIMAL(5,2) NOT NULL DEFAULT 40.00,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
        ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (program_id)
        REFERENCES programs(program_id)
        ON DELETE CASCADE,

    CHECK (required_credits > 0),
    CHECK (minimum_pass_mark >= 0 AND minimum_pass_mark <= 100)
);

-- Lecturers table stores lecturer details including department, expertise, and research interests.
CREATE TABLE lecturers (
    lecturer_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20) UNIQUE,
    department_id INT NOT NULL,
    area_of_expertise VARCHAR(150),
    course_load INT,
    research_interest VARCHAR(150),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
        ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (department_id)
        REFERENCES departments(department_id)
        ON DELETE CASCADE,

    CHECK (course_load >= 0)
);

-- Students table stores student details and links each student to a programme and faculty advisor.
CREATE TABLE students (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    date_of_birth DATE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20) UNIQUE,
    program_id INT NOT NULL,
    year_of_study INT NOT NULL,

    graduation_status ENUM(
        'Active',
        'Pending Graduation',
        'Graduated',
        'Withdrawn'
    ) NOT NULL,

    advisor_id INT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
        ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (program_id)
        REFERENCES programs(program_id),

    FOREIGN KEY (advisor_id)
        REFERENCES lecturers(lecturer_id)
        ON DELETE CASCADE,

    CHECK (year_of_study > 0)
);

-- Non-academic staff table stores administrative and support staff information linked to departments.
CREATE TABLE non_academic_staff (
    staff_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    job_title VARCHAR(100) NOT NULL,
    department_id INT NOT NULL,
    employment_type VARCHAR(50) NOT NULL,
    contract_details VARCHAR(150) NOT NULL,
    salary DECIMAL(10,2) NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
        ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (department_id)
        REFERENCES departments(department_id)
        ON DELETE CASCADE,

    CHECK (salary >= 0)
);

-- Emergency_contacts table to store emergency contact details for students, lecturers, and non-academic staff.
CREATE TABLE emergency_contacts (
    emergency_contact_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    relationship_to_person VARCHAR(50) NOT NULL,

    student_id INT NULL,
    lecturer_id INT NULL,
    staff_id INT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
        ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (student_id)
        REFERENCES students(student_id)
        ON DELETE CASCADE,

    FOREIGN KEY (lecturer_id)
        REFERENCES lecturers(lecturer_id)
        ON DELETE CASCADE,

    FOREIGN KEY (staff_id)
        REFERENCES non_academic_staff(staff_id)
        ON DELETE CASCADE,

    CHECK (
        (student_id IS NOT NULL AND lecturer_id IS NULL AND staff_id IS NULL)
        OR
        (student_id IS NULL AND lecturer_id IS NOT NULL AND staff_id IS NULL)
        OR
        (student_id IS NULL AND lecturer_id IS NULL AND staff_id IS NOT NULL)
    )
);

-- Courses table stores course details offered by academic departments.
CREATE TABLE courses (
    course_id INT AUTO_INCREMENT PRIMARY KEY,
    course_code VARCHAR(20) UNIQUE NOT NULL,
    course_name VARCHAR(100) NOT NULL,
    description TEXT,
    department_id INT NOT NULL,
    level INT NOT NULL,
    credits INT NOT NULL,
    prerequisites VARCHAR(150),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
        ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (department_id)
        REFERENCES departments(department_id)
        ON DELETE CASCADE,

    CHECK (level > 0),
    CHECK (credits > 0)
);

-- Create course_schedules table to store course timetable and capacity details.
CREATE TABLE course_schedules (
    schedule_id INT AUTO_INCREMENT PRIMARY KEY,
    course_id INT NOT NULL,
    day_of_week VARCHAR(20) NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    room VARCHAR(50) NOT NULL,
    class_capacity INT NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
        ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (course_id)
        REFERENCES courses(course_id)
        ON DELETE CASCADE,

    CHECK (class_capacity > 0),
    CHECK (start_time < end_time)
);

-- Research projects table stores project details and links each project to a principal investigator.
CREATE TABLE research_projects (
    project_id INT AUTO_INCREMENT PRIMARY KEY,
    project_title VARCHAR(150) NOT NULL,
    principal_investigator_id INT NOT NULL,
    funding_source VARCHAR(150),
    outcome TEXT,
    start_date DATE NOT NULL,
    end_date DATE,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
        ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (principal_investigator_id)
        REFERENCES lecturers(lecturer_id)
        ON DELETE CASCADE,

    CHECK (end_date IS NULL OR end_date >= start_date)
);

-- Enrolments table records student registrations on courses across semesters and academic years.
CREATE TABLE enrolments (
    enrolment_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    course_id INT NOT NULL,
    semester VARCHAR(50) NOT NULL,
    academic_year VARCHAR(20) NOT NULL,
    enrolment_status VARCHAR(50) NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
        ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (student_id)
        REFERENCES students(student_id)
        ON DELETE CASCADE,

    FOREIGN KEY (course_id)
        REFERENCES courses(course_id)
        ON DELETE CASCADE
);

-- Course_lecturers table resolves the many-to-many relationship between lecturers and courses.
CREATE TABLE course_lecturers (
    course_id INT NOT NULL,
    lecturer_id INT NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
        ON UPDATE CURRENT_TIMESTAMP,

    PRIMARY KEY (course_id, lecturer_id),

    FOREIGN KEY (course_id)
        REFERENCES courses(course_id)
        ON DELETE CASCADE,

    FOREIGN KEY (lecturer_id)
        REFERENCES lecturers(lecturer_id)
        ON DELETE CASCADE
);

-- Grades table stores student grade records for individual courses.
CREATE TABLE grades (
    grade_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    course_id INT NOT NULL,
    grade_percentage DECIMAL(5,2) NOT NULL,
    grade_date DATE NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
        ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (student_id)
        REFERENCES students(student_id)
        ON DELETE CASCADE,

    FOREIGN KEY (course_id)
        REFERENCES courses(course_id)
        ON DELETE CASCADE,

    CHECK (grade_percentage >= 0 AND grade_percentage <= 100)
);

-- Disciplinary records table stores student misconduct incidents and actions taken.
CREATE TABLE disciplinary_records (
    record_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    incident_date DATE NOT NULL,
    description TEXT NOT NULL,
    action_taken TEXT NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
        ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (student_id)
        REFERENCES students(student_id)
        ON DELETE CASCADE
);

-- Lecturer qualifications table stores academic qualifications achieved by lecturers.
CREATE TABLE lecturer_qualifications (
    qualification_id INT AUTO_INCREMENT PRIMARY KEY,
    lecturer_id INT NOT NULL,
    qualification_name VARCHAR(150) NOT NULL,
    institution VARCHAR(150) NOT NULL,
    year_awarded INT NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
        ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (lecturer_id)
        REFERENCES lecturers(lecturer_id)
        ON DELETE CASCADE,

    CHECK (year_awarded >= 1900)
);

-- Lecturer publications table stores research publications authored by lecturers.
CREATE TABLE lecturer_publications (
    publication_id INT AUTO_INCREMENT PRIMARY KEY,
    lecturer_id INT NOT NULL,
    publication_title VARCHAR(200) NOT NULL,
    publication_year INT NOT NULL,
    publication_type VARCHAR(100) NOT NULL,
    journal_or_conference VARCHAR(150) NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
        ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (lecturer_id)
        REFERENCES lecturers(lecturer_id)
        ON DELETE CASCADE,

    CHECK (publication_year >= 1900)
);

-- Research project members table stores lecturer or student participation in research projects.
CREATE TABLE research_project_members (
    membership_id INT AUTO_INCREMENT PRIMARY KEY,
    project_id INT NOT NULL,
    lecturer_id INT,
    student_id INT,
    member_role VARCHAR(100) NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
        ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (project_id)
        REFERENCES research_projects(project_id)
        ON DELETE CASCADE,

    FOREIGN KEY (lecturer_id)
        REFERENCES lecturers(lecturer_id)
        ON DELETE CASCADE,

    FOREIGN KEY (student_id)
        REFERENCES students(student_id)
        ON DELETE CASCADE,

    CHECK (
        (lecturer_id IS NOT NULL AND student_id IS NULL)
        OR
        (lecturer_id IS NULL AND student_id IS NOT NULL)
    )
);
