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