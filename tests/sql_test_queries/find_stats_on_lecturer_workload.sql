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