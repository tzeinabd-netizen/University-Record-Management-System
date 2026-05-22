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