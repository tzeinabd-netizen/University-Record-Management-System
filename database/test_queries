-- Use the university database
USE university_record_system;

-- Display all student records
SELECT * FROM students;

-- Display all course records
SELECT * FROM courses;

-- Display all lecturer records
SELECT * FROM lecturers;

-- Query 1: Find all students enrolled in a specific course taught by a particular lecturer.
SELECT 
    s.first_name,
    s.last_name,
    c.course_name,
    l.first_name AS lecturer_first_name,
    l.last_name AS lecturer_last_name
FROM students s
JOIN enrolments e
    ON s.student_id = e.student_id
JOIN courses c
    ON e.course_id = c.course_id
JOIN course_lecturers cl
    ON c.course_id = cl.course_id
JOIN lecturers l
    ON cl.lecturer_id = l.lecturer_id
WHERE c.course_name = 'Database Systems'
AND l.last_name = 'Walker';

-- Query 2: List all final-year students with an average grade above 70%.
SELECT 
    s.student_id,
    s.first_name,
    s.last_name,
    s.year_of_study,
    ROUND(AVG(g.grade_percentage), 2) AS average_grade
FROM students s
JOIN grades g
    ON s.student_id = g.student_id
WHERE s.year_of_study >= 3
GROUP BY s.student_id, s.first_name, s.last_name, s.year_of_study
HAVING AVG(g.grade_percentage) > 70;

-- Query 3: Identify students who have not registered for any courses.
SELECT 
    s.student_id,
    s.first_name,
    s.last_name
FROM students s
LEFT JOIN enrolments e
    ON s.student_id = e.student_id
WHERE e.student_id IS NULL;

-- Query 4: Retrieve the contact information for the faculty advisor of a specific student.
SELECT 
    s.first_name AS student_first_name,
    s.last_name AS student_last_name,
    l.first_name AS advisor_first_name,
    l.last_name AS advisor_last_name,
    l.email,
    l.phone
FROM students s
JOIN lecturers l
    ON s.advisor_id = l.lecturer_id
WHERE s.last_name = 'Rahman';

-- Query 5: Generate a report on the publications of lecturers in the past year.
SELECT 
    l.first_name,
    l.last_name,
    p.publication_title,
    p.publication_year,
    p.publication_type,
    p.journal_or_conference
FROM lecturers l
JOIN lecturer_publications p
    ON l.lecturer_id = p.lecturer_id
WHERE p.publication_year = 2025
ORDER BY l.last_name, p.publication_title;

-- Query 6: Identify students who failed at least one course.
SELECT 
    s.first_name,
    s.last_name,
    c.course_name,
    g.grade_percentage
FROM students s
JOIN grades g
    ON s.student_id = g.student_id
JOIN courses c
    ON g.course_id = c.course_id
WHERE g.grade_percentage < 40
ORDER BY g.grade_percentage ASC;

-- Query 7: Identify the top-performing courses based on average student grades.
SELECT 
    c.course_name,
    ROUND(AVG(g.grade_percentage), 2) AS average_course_grade
FROM courses c
JOIN grades g
    ON c.course_id = g.course_id
GROUP BY c.course_id, c.course_name
ORDER BY average_course_grade DESC;

-- Query 8: Identify students and lecturers involved in research projects.
SELECT 
    rp.project_title,
    COALESCE(
        CONCAT(l.first_name, ' ', l.last_name),
        CONCAT(s.first_name, ' ', s.last_name)
    ) AS member_name,
    rpm.member_role
FROM research_project_members rpm
JOIN research_projects rp
    ON rpm.project_id = rp.project_id
LEFT JOIN lecturers l
    ON rpm.lecturer_id = l.lecturer_id
LEFT JOIN students s
    ON rpm.student_id = s.student_id
ORDER BY rp.project_title;
