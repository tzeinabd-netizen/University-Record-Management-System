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