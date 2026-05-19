SELECT 
    s.student_id,
    s.first_name,
    s.last_name,
    s.year_of_study,
    ROUND(AVG(g.grade_percentage), 2) AS average_grade
FROM students s
JOIN grades g
    ON s.student_id = g.student_id
WHERE s.year_of_study = 4
GROUP BY s.student_id, s.first_name, s.last_name, s.year_of_study
HAVING AVG(g.grade_percentage) > 70;