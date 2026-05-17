SELECT 
    c.course_name,
    ROUND(AVG(g.grade_percentage), 2) AS average_course_grade
FROM courses c
JOIN grades g
    ON c.course_id = g.course_id
GROUP BY c.course_id, c.course_name
ORDER BY average_course_grade DESC;