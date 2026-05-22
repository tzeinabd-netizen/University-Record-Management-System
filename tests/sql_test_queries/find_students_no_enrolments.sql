SELECT 
    s.student_id,
    s.first_name,
    s.last_name
FROM students s
LEFT JOIN enrolments e
    ON s.student_id = e.student_id
WHERE e.student_id IS NULL;