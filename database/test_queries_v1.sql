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
    rpm.member_role,
     CASE
		WHEN l.lecturer_id IS NOT NULL THEN 'Lecturer'
        WHEN s.student_id IS NOT NULL THEN 'Student'
        ELSE 'n/a'
	END AS member_type
FROM research_project_members rpm
JOIN research_projects rp
    ON rpm.project_id = rp.project_id
LEFT JOIN lecturers l
    ON rpm.lecturer_id = l.lecturer_id
LEFT JOIN students s
    ON rpm.student_id = s.student_id
ORDER BY rp.project_title;

-- Query 9: Collect statistics on course popularity

WITH course_stats AS (
	SELECT
		c.course_id,
		c.course_name,
		COUNT(e.enrolment_id) AS number_enrolments,
		COUNT(DISTINCT e.student_id) AS course_size
	FROM courses c
    LEFT JOIN enrolments e
		ON c.course_id = e.course_id
	GROUP BY c.course_id, c.course_id
)
SELECT
	course_id,
    course_name,
    number_enrolments,
    course_size,

    RANK () OVER (
		ORDER BY course_size DESC
	) AS course_ranking

FROM course_stats;

--Query 10: Collect statistics on lecturer workload

WITH lecturer_stats AS (
	SELECT
		l.lecturer_id,
		l.first_name,
		l.last_name,
		COUNT(DISTINCT e.student_id) AS students_taught,
		COUNT(DISTINCT cl.course_id) AS courses_taught
	FROM lecturers l
    LEFT JOIN course_lecturers cl
		ON l.lecturer_id = cl.lecturer_id
	LEFT JOIN enrolments e
		ON cl.course_id = e.course_id
	GROUP BY l.lecturer_id, l.last_name
   )
	SELECT
	lecturer_id,
    first_name,
    last_name,
    students_taught,
    courses_taught,

    RANK () OVER (
		ORDER BY students_taught DESC
	) AS lecturer_ranking

FROM lecturer_stats;

-- Query 11: Identify members of the university with the same name

SELECT
    first_name,
    last_name,
    COUNT(*) AS duplicates
FROM (
    SELECT first_name, last_name
	FROM students

    UNION ALL

    SELECT first_name, last_name
    FROM lecturers

    UNION ALL

    SELECT first_name, last_name
    FROM non_academic_staff

) AS all_uni_members

GROUP BY first_name, last_name
HAVING COUNT(*) > 1;












