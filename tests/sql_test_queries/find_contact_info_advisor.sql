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
