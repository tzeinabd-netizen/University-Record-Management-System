SELECT 
    l.first_name,
    l.last_name,
    p.publication_title,
    p.publication_year,
    p.publication_type,
    p.journal_or_conference
FROM lecturers l
JOIN lecturer_publications p
    ON l.lecturer_id = p.lecturer_id
WHERE p.publication_year = 2025
ORDER BY l.last_name, p.publication_title;