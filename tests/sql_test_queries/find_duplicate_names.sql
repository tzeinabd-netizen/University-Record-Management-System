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