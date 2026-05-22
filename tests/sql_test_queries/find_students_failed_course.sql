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