USE university_record_system;

-- Insert sample departments
INSERT INTO departments (department_name, faculty, research_area)
VALUES
('Computer Science', 'Faculty of Science and Technology', 'Artificial Intelligence'),
('Mathematics', 'Faculty of Science and Technology', 'Applied Mathematics'),
('Business', 'Faculty of Business and Management', 'Digital Business'),
('Engineering', 'Faculty of Engineering', 'Sustainable Engineering'),
('Health Sciences', 'Faculty of Health and Life Sciences', 'Healthcare Technology');

-- Insert sample academic programme records linked to departments.
INSERT INTO programs (
    program_name,
    degree_awarded,
    duration_years,
    department_id
)
VALUES
('Computer Science', 'BSc Computer Science', 3, 1),
('Data Science', 'MSc Data Science', 1, 1),
('Applied Mathematics', 'BSc Applied Mathematics', 3, 2),
('Business Analytics', 'MBA Business Analytics', 2, 3),
('Mechanical Engineering', 'BEng Mechanical Engineering', 4, 4),
('Healthcare Informatics', 'MSc Healthcare Informatics', 2, 5);

-- Insert programme credit requirements.
INSERT INTO program_requirements (
    program_id,
    required_credits,
    minimum_pass_mark
)
VALUES
(1, 360, 40.00),
(2, 180, 40.00),
(3, 360, 40.00),
(4, 180, 40.00),
(5, 480, 40.00),
(6, 180, 40.00);

-- Insert sample lecturer records linked to academic departments.
INSERT INTO lecturers (
    first_name,
    last_name,
    email,
    phone,
    department_id,
    area_of_expertise,
    course_load,
    research_interest
)
VALUES
('James', 'Walker', 'j.walker@university.edu', '07748 291635', 1, 'Artificial Intelligence', 3, 'Machine Learning'),
('Ananya', 'Patel', 'a.patel@university.edu', '07912 564873', 2, 'Applied Mathematics', 2, 'Numerical Analysis'),
('Omar', 'Khalid', 'o.khalid@university.edu', '07563 184920', 3, 'Business Analytics', 4, 'Digital Transformation'),
('Sarah', 'Ahmed', 's.ahmed@university.edu', '07825 937416', 4, 'Mechanical Engineering', 3, 'Renewable Energy'),
('Kwame', 'Mensah', 'k.mensah@university.edu', '07481 620557', 5, 'Healthcare Technology', 2, 'Health Data Systems'),
('Michael', 'Taylor', 'm.taylor@university.edu', '07394 458261', 1, 'Cyber Security', 3, 'Network Security'),
('Chen', 'Wei', 'c.wei@university.edu', '07811 223344', 1, 'Data Science', 2, 'Big Data Analytics'),
('Amara', 'Ndlovu', 'a.ndlovu@university.edu', '07566 778899', 4, 'Civil Engineering', 3, 'Smart Infrastructure');

-- Insert sample student records linked to programmes and faculty advisors.
INSERT INTO students (
    first_name,
    last_name,
    date_of_birth,
    email,
    phone,
    program_id,
    year_of_study,
    graduation_status,
    advisor_id
)
VALUES
('Aisha', 'Rahman', '2003-05-14', 'a.rahman@student.edu', '07812 345671', 1, 2, 'Active', 1),
('Daniel', 'Evans', '2002-11-22', 'd.evans@student.edu', '07934 567812', 1, 3, 'Active', 6),
('Priyanka', 'Sharma', '2001-08-09', 'p.sharma@student.edu', '07521 456783', 2, 1, 'Active', 2),
('Samuel', 'Okoro', '2000-03-17', 's.okoro@student.edu', '07483 219654', 3, 3, 'Pending Graduation', 2),
('Fatima', 'Hassan', '2002-07-30', 'f.hassan@student.edu', '07790 112233', 4, 2, 'Active', 3),
('Jacob', 'Miller', '2001-12-11', 'j.miller@student.edu', '07345 667788', 5, 4, 'Active', 4),
('Grace', 'Mensah', '2003-01-25', 'g.mensah@student.edu', '07865 998877', 6, 1, 'Active', 5),
('Noah', 'Wilson', '2002-09-18', 'n.wilson@student.edu', '07544 332211', 1, 2, 'Active', 1),
('Zainab', 'Ali', '2001-06-03', 'z.ali@student.edu', '07988 221144', 2, 1, 'Active', 7),
('Ethan', 'Clarke', '2002-10-27', 'e.clarke@student.edu', '07411 556677', 5, 3, 'Active', 8),
('Leah', 'Robinson', '2003-04-19', 'l.robinson@student.edu', '07844 112255', 3, 2, 'Active', 2),
('Arjun', 'Mehta', '2001-09-07', 'a.mehta@student.edu', '07555 334466', 2, 1, 'Active', 7),
('Mariam', 'Saleh', '2002-02-11', 'm.saleh@student.edu', '07766 778899', 4, 2, 'Active', 3),
('Tendai', 'Moyo', '2000-12-03', 't.moyo@student.edu', '07422 889900', 5, 4, 'Pending Graduation', 8),
('Olivia', 'Green', '2003-06-28', 'o.green@student.edu', '07911 445566', 1, 1, 'Active', 1);

-- Insert sample non-academic staff records linked to departments.
INSERT INTO non_academic_staff (
    first_name,
    last_name,
    job_title,
    department_id,
    employment_type,
    contract_details,
    salary
)
VALUES
('Helen', 'Carter', 'Department Administrator', 1, 'Full-Time', 'Permanent Contract', 32500.00),

('Imran', 'Yusuf', 'IT Support Technician', 1, 'Full-Time', 'Permanent Contract', 34800.00),

('Rebecca', 'Jones', 'Finance Assistant', 3, 'Part-Time', '2-Year Fixed-Term Contract', 24500.00),

('Ahmed', 'Farouk', 'Laboratory Technician', 4, 'Full-Time', 'Permanent Contract', 30200.00),

('Nomsa', 'Dube', 'Student Services Coordinator', 5, 'Full-Time', 'Permanent Contract', 34100.00),

('Claire', 'Bennett', 'Research Support Officer', 2, 'Part-Time', '1-Year Fixed-Term Contract', 27800.00);

-- Insert emergency contact records.
INSERT INTO emergency_contacts (
    first_name,
    last_name,
    phone,
    relationship_to_person,
    student_id,
    lecturer_id,
    staff_id
)
VALUES

-- Student emergency contacts
('Mark', 'Rahman', '07888 112233', 'Father', 1, NULL, NULL),
('Sophia', 'Evans', '07991 223344', 'Mother', 2, NULL, NULL),
('Raj', 'Sharma', '07567 445566', 'Brother', 3, NULL, NULL),
('Miriam', 'Okoro', '07455 667788', 'Mother', 4, NULL, NULL),
('Khalid', 'Hassan', '07789 334455', 'Father', 5, NULL, NULL),
('Laura', 'Miller', '07333 112244', 'Mother', 6, NULL, NULL),
('Peter', 'Mensah', '07877 889900', 'Father', 7, NULL, NULL),
('Angela', 'Wilson', '07544 778899', 'Sister', 8, NULL, NULL),
('Fatima', 'Ali', '07922 334466', 'Mother', 9, NULL, NULL),
('Robert', 'Clarke', '07499 112255', 'Father', 10, NULL, NULL),
('Sanjay', 'Mehta', '07511 667755', 'Father', 12, NULL, NULL),
('Ahmed', 'Saleh', '07755 223344', 'Brother', 13, NULL, NULL),

-- Lecturer emergency contacts
('Amina', 'Walker', '07821 667701', 'Spouse', NULL, 1, NULL),
('Daniel', 'Patel', '07440 556612', 'Brother', NULL, 2, NULL),
('Leila', 'Khalid', '07560 778845', 'Spouse', NULL, 3, NULL),
('Michael', 'Ahmed', '07830 445577', 'Husband', NULL, 4, NULL),
('Esther', 'Mensah', '07470 889955', 'Sister', NULL, 5, NULL),
('Grace', 'Taylor', '07380 112288', 'Mother', NULL, 6, NULL),
('Ying', 'Wei', '07891 223355', 'Spouse', NULL, 7, NULL),

-- Non-academic staff emergency contacts
('Grace', 'Carter', '07777 123456', 'Partner', NULL, NULL, 1),
('Ibrahim', 'Yusuf', '07666 998877', 'Brother', NULL, NULL, 2),
('Thomas', 'Jones', '07456 771122', 'Husband', NULL, NULL, 3),
('Layla', 'Farouk', '07567 881133', 'Spouse', NULL, NULL, 4),
('Sipho', 'Dube', '07812 664422', 'Brother', NULL, NULL, 5),
('James', 'Bennett', '07734 551199', 'Husband', NULL, NULL, 6);

-- Insert sample course records linked to departments.
INSERT INTO courses (
    course_code,
    course_name,
    description,
    department_id,
    level,
    credits,
    prerequisites
)
VALUES
('CS101', 'Introduction to Programming', 'Fundamentals of Python programming and problem solving.', 1, 4, 20, NULL),

('CS205', 'Database Systems', 'Relational database design, SQL, and normalisation concepts.', 1, 5, 20, 'CS101'),

('CS310', 'Machine Learning', 'Supervised and unsupervised machine learning techniques.', 1, 6, 20, 'CS205'),

('MA201', 'Statistical Modelling', 'Probability distributions and statistical modelling methods.', 2, 5, 15, NULL),

('BA220', 'Business Intelligence', 'Data-driven decision making and business reporting tools.', 3, 5, 15, NULL),

('ME301', 'Thermodynamics', 'Principles of heat transfer and thermodynamic systems.', 4, 6, 20, NULL),

('ME315', 'Renewable Energy Systems', 'Engineering approaches to renewable energy generation.', 4, 6, 20, 'ME301'),

('HS210', 'Healthcare Data Analytics', 'Analysis of healthcare datasets and digital health systems.', 5, 5, 15, NULL),

('CS330', 'Cyber Security Fundamentals', 'Network security, encryption, and cyber threat management.', 1, 6, 20, 'CS205'),

('MA320', 'Numerical Methods', 'Computational methods for solving mathematical problems.', 2, 6, 15, 'MA201');

-- Insert course schedule records.
INSERT INTO course_schedules (
    course_id,
    day_of_week,
    start_time,
    end_time,
    room,
    class_capacity
)
VALUES
(1, 'Monday', '10:00:00', '12:00:00', 'CS-LAB1', 40),
(1, 'Thursday', '14:00:00', '16:00:00', 'CS-LAB2', 25),

(2, 'Wednesday', '14:00:00', '16:00:00', 'DB-204', 35),

(3, 'Friday', '09:00:00', '11:00:00', 'AI-LAB2', 30),

(4, 'Tuesday', '11:00:00', '13:00:00', 'MA-301', 45),

(5, 'Thursday', '13:00:00', '15:00:00', 'BUS-LT1', 50),

(6, 'Monday', '14:00:00', '16:00:00', 'ENG-LAB2', 25),

(7, 'Friday', '12:00:00', '14:00:00', 'ENG-315', 25),

(8, 'Wednesday', '09:00:00', '11:00:00', 'HS-LAB1', 35),

(9, 'Thursday', '10:00:00', '12:00:00', 'CYB-LAB1', 30),

(10, 'Tuesday', '14:00:00', '16:00:00', 'COMP-203', 40);

-- Insert sample research project records.
INSERT INTO research_projects (
    project_title,
    principal_investigator_id,
    funding_source,
    outcome,
    start_date,
    end_date
)
VALUES
('AI for Early Disease Detection', 1, 'UK Research Council', 'Prototype diagnostic prediction model developed.', '2024-01-15', '2025-12-20'),

('Advanced Numerical Simulation Models', 2, 'National Mathematics Foundation', 'Improved computational modelling techniques.', '2023-09-01', '2025-06-30'),

('Digital Transformation in SMEs', 3, 'Innovate UK', 'Framework developed for digital adoption in small businesses.', '2024-03-10', '2025-11-15'),

('Smart Renewable Energy Systems', 4, 'Green Energy Initiative', 'Energy optimisation system tested successfully.', '2023-11-05', '2025-08-25'),

('Healthcare Data Integration Platform', 5, 'NHS Digital Innovation Fund', 'Centralised healthcare analytics platform proposed.', '2024-02-01', '2026-01-10');

-- Insert sample enrolment records linking students to courses.
INSERT INTO enrolments (
    student_id,
    course_id,
    semester,
    academic_year,
    enrolment_status
)
VALUES
(1, 1, 'Semester 1', '2025/26', 'Enrolled'),
(1, 2, 'Semester 1', '2025/26', 'Enrolled'),
(1, 9, 'Semester 2', '2025/26', 'Enrolled'),

(2, 2, 'Semester 1', '2025/26', 'Enrolled'),
(2, 3, 'Semester 2', '2025/26', 'Enrolled'),
(2, 9, 'Semester 2', '2025/26', 'Enrolled'),

(3, 2, 'Semester 1', '2025/26', 'Enrolled'),
(3, 3, 'Semester 2', '2025/26', 'Enrolled'),
(3, 8, 'Semester 2', '2025/26', 'Enrolled'),

(4, 4, 'Semester 1', '2025/26', 'Enrolled'),
(4, 10, 'Semester 2', '2025/26', 'Enrolled'),

(5, 5, 'Semester 1', '2025/26', 'Enrolled'),
(5, 8, 'Semester 2', '2025/26', 'Enrolled'),

(6, 6, 'Semester 1', '2025/26', 'Enrolled'),
(6, 7, 'Semester 2', '2025/26', 'Enrolled'),

(7, 8, 'Semester 1', '2025/26', 'Enrolled'),
(7, 5, 'Semester 2', '2025/26', 'Enrolled'),

(8, 1, 'Semester 1', '2025/26', 'Enrolled'),
(8, 2, 'Semester 1', '2025/26', 'Enrolled'),

(9, 3, 'Semester 2', '2025/26', 'Enrolled'),
(9, 9, 'Semester 2', '2025/26', 'Enrolled'),

(10, 6, 'Semester 1', '2025/26', 'Enrolled'),
(10, 7, 'Semester 2', '2025/26', 'Enrolled'),

(11, 4, 'Semester 1', '2025/26', 'Enrolled'),
(11, 10, 'Semester 2', '2025/26', 'Enrolled'),

(12, 2, 'Semester 1', '2025/26', 'Enrolled'),
(12, 3, 'Semester 2', '2025/26', 'Enrolled'),

(13, 5, 'Semester 1', '2025/26', 'Enrolled');

-- Insert lecturer-course teaching assignments.
INSERT INTO course_lecturers (
    course_id,
    lecturer_id
)
VALUES
(1, 1),
(2, 1),
(2, 6),
(3, 1),
(3, 7),
(4, 2),
(5, 3),
(6, 4),
(7, 4),
(8, 5),
(9, 6),
(10, 2);

-- Insert student grade records for courses.
INSERT INTO grades (
    student_id,
    course_id,
    grade_percentage,
    grade_date
)
VALUES
(1, 1, 72.5, '2025-12-10'),
(1, 2, 68.0, '2025-12-15'),
(1, 9, 74.0, '2026-01-12'),

(2, 2, 81.0, '2025-12-15'),
(2, 3, 78.5, '2026-01-18'),
(2, 9, 84.0, '2026-01-20'),

(3, 2, 66.0, '2025-12-16'),
(3, 3, 71.5, '2026-01-19'),
(3, 8, 73.0, '2026-01-22'),

(4, 4, 18.0, '2025-12-11'),
(4, 10, 41.5, '2026-01-17'),

(5, 5, 69.0, '2025-12-13'),
(5, 8, 72.0, '2026-01-21'),

(6, 6, 75.0, '2025-12-09'),
(6, 7, 79.5, '2026-01-25'),

(7, 8, 83.0, '2025-12-14'),
(7, 5, 80.0, '2026-01-20'),

(8, 1, 35.0, '2025-12-08'),
(8, 2, 53.5, '2025-12-15'),

(9, 3, 77.0, '2026-01-18'),
(9, 9, 82.0, '2026-01-23'),

(10, 6, 71.0, '2025-12-12'),
(10, 7, 74.5, '2026-01-24'),

(11, 4, 67.0, '2025-12-10'),
(11, 10, 69.5, '2026-01-19'),

(12, 2, 88.0, '2025-12-16'),
(12, 3, 91.0, '2026-01-20'),

(13, 5, 42.0, '2025-12-13');

-- Insert student disciplinary records.
INSERT INTO disciplinary_records (
    student_id,
    incident_date,
    description,
    action_taken
)
VALUES
(4, '2025-11-18', 'Missed multiple assessments without valid justification.', 'Formal academic warning issued'),

(8, '2025-10-05', 'Plagiarism detected in coursework submission.', 'Assessment mark capped and academic integrity training assigned'),

(13, '2025-12-01', 'Disruptive behaviour during laboratory session.', 'Meeting held with academic advisor');

-- Insert lecturer qualification records.
INSERT INTO lecturer_qualifications (
    lecturer_id,
    qualification_name,
    institution,
    year_awarded
)
VALUES
(1, 'PhD in Artificial Intelligence', 'University of Manchester', 2016),
(1, 'MSc Computer Science', 'University of Leeds', 2011),

(2, 'PhD in Applied Mathematics', 'Imperial College London', 2014),

(3, 'MBA Business Analytics', 'University of Warwick', 2015),

(4, 'PhD in Mechanical Engineering', 'University of Birmingham', 2013),
(4, 'MEng Mechanical Engineering', 'University of Sheffield', 2009),

(5, 'PhD in Health Informatics', 'King’s College London', 2018),

(6, 'MSc Cyber Security', 'University of Liverpool', 2017),

(7, 'PhD in Data Science', 'University of Edinburgh', 2019),

(8, 'PhD in Civil Engineering', 'University of Glasgow', 2012);

-- Insert lecturer publication records.
INSERT INTO lecturer_publications (
    lecturer_id,
    publication_title,
    publication_year,
    publication_type,
    journal_or_conference
)
VALUES
(1, 'Machine Learning Approaches for Early Diagnosis', 2025, 'Journal Article', 'Journal of AI in Healthcare'),
(1, 'Ethical Challenges in Applied Artificial Intelligence', 2024, 'Conference Paper', 'International AI Conference'),

(2, 'Numerical Methods for Complex Systems', 2025, 'Journal Article', 'Applied Mathematics Review'),

(3, 'Digital Transformation Strategies for SMEs', 2024, 'Journal Article', 'Business Technology Journal'),

(4, 'Energy Optimisation in Renewable Systems', 2025, 'Conference Paper', 'Sustainable Engineering Conference'),
(4, 'Thermal Efficiency in Mechanical Systems', 2023, 'Journal Article', 'Engineering Systems Journal'),

(5, 'Data Integration in Healthcare Systems', 2025, 'Journal Article', 'Health Informatics Journal'),

(6, 'Network Security Threats in Higher Education', 2024, 'Conference Paper', 'Cyber Security Research Forum'),

(7, 'Big Data Analytics for Student Performance Prediction', 2025, 'Journal Article', 'Data Science and Education Journal'),

(8, 'Smart Infrastructure Monitoring Using Sensor Data', 2023, 'Journal Article', 'Civil Engineering Innovations');

-- Insert research project member records.
INSERT INTO research_project_members (
    project_id,
    lecturer_id,
    student_id,
    member_role
)
VALUES
(1, 1, NULL, 'Principal Investigator'),
(1, NULL, 2, 'Research Assistant'),
(1, NULL, 12, 'Data Analyst'),

(2, 2, NULL, 'Principal Investigator'),
(2, NULL, 4, 'Research Assistant'),

(3, 3, NULL, 'Project Lead'),
(3, NULL, 5, 'Research Intern'),

(4, 4, NULL, 'Principal Investigator'),
(4, NULL, 10, 'Research Assistant'),

(5, 5, NULL, 'Project Lead'),
(5, NULL, 7, 'Data Researcher');


