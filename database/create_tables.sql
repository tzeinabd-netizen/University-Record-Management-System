USE university_record_system;

-- Departments table stores information about each academic department within the university.
CREATE TABLE departments (
    department_id INT AUTO_INCREMENT PRIMARY KEY,
    department_name VARCHAR(100) NOT NULL,
    faculty VARCHAR(100) NOT NULL,
    research_area VARCHAR(150)
);

-- Programs table stores academic programmes offered by departments.
CREATE TABLE programs (
    program_id INT AUTO_INCREMENT PRIMARY KEY,
    program_name VARCHAR(100) NOT NULL,
    degree_awarded VARCHAR(100) NOT NULL,
    duration_years INT NOT NULL,
    department_id INT NOT NULL,
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
);

-- Lecturers table stores lecturer details including department, expertise, and research interests.
CREATE TABLE lecturers (
    lecturer_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20),
    department_id INT NOT NULL,
    area_of_expertise VARCHAR(150),
    course_load INT,
    research_interest VARCHAR(150),
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
);

-- Students table stores student details and links each student to a programme and faculty advisor.
CREATE TABLE students (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    date_of_birth DATE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20),
    program_id INT NOT NULL,
    year_of_study INT NOT NULL,
    graduation_status VARCHAR(50),
    advisor_id INT NOT NULL,
    FOREIGN KEY (program_id) REFERENCES programs(program_id),
    FOREIGN KEY (advisor_id) REFERENCES lecturers(lecturer_id)
);

-- Non-academic staff table stores administrative and support staff information linked to departments.
CREATE TABLE non_academic_staff (
    staff_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    job_title VARCHAR(100) NOT NULL,
    department_id INT NOT NULL,
    employment_type VARCHAR(50),
    contract_details TEXT,
    salary DECIMAL(10,2),
    emergency_contact_name VARCHAR(100),
    emergency_contact_phone VARCHAR(20),
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
);

-- Courses table stores course details offered by academic departments.
CREATE TABLE courses (
    course_id INT AUTO_INCREMENT PRIMARY KEY,
    course_code VARCHAR(20) UNIQUE NOT NULL,
    course_name VARCHAR(100) NOT NULL,
    description TEXT,
    department_id INT NOT NULL,
    level INT,
    credits INT,
    schedule VARCHAR(100),
    prerequisites VARCHAR(150),
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
);

-- Research projects table stores project details and links each project to a principal investigator.
CREATE TABLE research_projects (
    project_id INT AUTO_INCREMENT PRIMARY KEY,
    project_title VARCHAR(150) NOT NULL,
    principal_investigator_id INT NOT NULL,
    funding_source VARCHAR(150),
    outcome TEXT,
    start_date DATE,
    end_date DATE,
    FOREIGN KEY (principal_investigator_id) REFERENCES lecturers(lecturer_id)
);

-- Enrolments table records student registrations on courses across semesters and academic years.
CREATE TABLE enrolments (
    enrolment_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    course_id INT NOT NULL,
    semester VARCHAR(50),
    academic_year VARCHAR(20),
    enrolment_status VARCHAR(50),
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
);

-- Course_lecturers table resolves the many-to-many relationship between lecturers and courses.
CREATE TABLE course_lecturers (
    course_id INT NOT NULL,
    lecturer_id INT NOT NULL,
    PRIMARY KEY (course_id, lecturer_id),
    FOREIGN KEY (course_id) REFERENCES courses(course_id),
    FOREIGN KEY (lecturer_id) REFERENCES lecturers(lecturer_id)
);

-- Grades table stores student grade records for individual courses.
CREATE TABLE grades (
    grade_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    course_id INT NOT NULL,
    grade_percentage DECIMAL(5,2),
    grade_date DATE,
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
);

-- Disciplinary records table stores student misconduct incidents and actions taken.
CREATE TABLE disciplinary_records (
    record_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    incident_date DATE,
    description TEXT,
    action_taken TEXT,
    FOREIGN KEY (student_id) REFERENCES students(student_id)
);

-- Lecturer qualifications table stores academic qualifications achieved by lecturers.
CREATE TABLE lecturer_qualifications (
    qualification_id INT AUTO_INCREMENT PRIMARY KEY,
    lecturer_id INT NOT NULL,
    qualification_name VARCHAR(150) NOT NULL,
    institution VARCHAR(150),
    year_awarded INT,
    FOREIGN KEY (lecturer_id) REFERENCES lecturers(lecturer_id)
);

-- Lecturer publications table stores research publications authored by lecturers.
CREATE TABLE lecturer_publications (
    publication_id INT AUTO_INCREMENT PRIMARY KEY,
    lecturer_id INT NOT NULL,
    publication_title VARCHAR(200) NOT NULL,
    publication_year INT,
    publication_type VARCHAR(100),
    journal_or_conference VARCHAR(150),
    FOREIGN KEY (lecturer_id) REFERENCES lecturers(lecturer_id)
);

-- Research project members table stores lecturer or student participation in research projects.
CREATE TABLE research_project_members (
    member_id INT AUTO_INCREMENT PRIMARY KEY,
    project_id INT NOT NULL,
    lecturer_id INT NULL,
    student_id INT NULL,
    member_role VARCHAR(100),
    FOREIGN KEY (project_id) REFERENCES research_projects(project_id),
    FOREIGN KEY (lecturer_id) REFERENCES lecturers(lecturer_id),
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    CHECK (
        (lecturer_id IS NOT NULL AND student_id IS NULL)
        OR
        (lecturer_id IS NULL AND student_id IS NOT NULL)
    )
);
