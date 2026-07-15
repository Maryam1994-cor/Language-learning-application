-- File: insert_data.sql
-- Purpose:
-- Insert initial sample records into the Language Learning application.

-- The script demonstrates INSERT statements, unique values, foreign-key
-- relationships, and data insertion through SELECT queries as discussed
-- in Chapters 23 and 24 of the assigned course textbook.

USE language_learning_db;

-- Insert students.
-- ON DUPLICATE KEY UPDATE allows this script to be executed repeatedly
-- without creating duplicate email records.

INSERT INTO students (
    student_name,
    email
)
VALUES
    ('Ayesha Khan', 'ayesha.khan@example.com'),
    ('Bilal Ahmed', 'bilal.ahmed@example.com'),
    ('Fatima Ali', 'fatima.ali@example.com'),
    ('Hamza Malik', 'hamza.malik@example.com')
ON DUPLICATE KEY UPDATE
    student_name = VALUES(student_name);

-- Insert available languages.
-- language_name has a UNIQUE constraint, so repeated execution will not
-- create duplicate language records.

INSERT INTO languages (
    language_name
)
VALUES
    ('English'),
    ('French'),
    ('German'),
    ('Spanish')
ON DUPLICATE KEY UPDATE
    language_name = VALUES(language_name);

-- Connect students with languages.
-- Student and language IDs are selected from their respective tables,
-- avoiding assumptions about AUTO_INCREMENT values.

INSERT INTO student_language_xref (
    student_id,
    language_id,
    proficiency
)
SELECT
    students.student_id,
    languages.language_id,
    'Intermediate'
FROM students
INNER JOIN languages
    ON languages.language_name = 'English'
WHERE students.email = 'ayesha.khan@example.com'
ON DUPLICATE KEY UPDATE
    proficiency = VALUES(proficiency);

INSERT INTO student_language_xref (
    student_id,
    language_id,
    proficiency
)
SELECT
    students.student_id,
    languages.language_id,
    'Beginner'
FROM students
INNER JOIN languages
    ON languages.language_name = 'French'
WHERE students.email = 'ayesha.khan@example.com'
ON DUPLICATE KEY UPDATE
    proficiency = VALUES(proficiency);

INSERT INTO student_language_xref (
    student_id,
    language_id,
    proficiency
)
SELECT
    students.student_id,
    languages.language_id,
    'Advanced'
FROM students
INNER JOIN languages
    ON languages.language_name = 'English'
WHERE students.email = 'bilal.ahmed@example.com'
ON DUPLICATE KEY UPDATE
    proficiency = VALUES(proficiency);

INSERT INTO student_language_xref (
    student_id,
    language_id,
    proficiency
)
SELECT
    students.student_id,
    languages.language_id,
    'Beginner'
FROM students
INNER JOIN languages
    ON languages.language_name = 'German'
WHERE students.email = 'fatima.ali@example.com'
ON DUPLICATE KEY UPDATE
    proficiency = VALUES(proficiency);

INSERT INTO student_language_xref (
    student_id,
    language_id,
    proficiency
)
SELECT
    students.student_id,
    languages.language_id,
    'Intermediate'
FROM students
INNER JOIN languages
    ON languages.language_name = 'Spanish'
WHERE students.email = 'hamza.malik@example.com'
ON DUPLICATE KEY UPDATE
    proficiency = VALUES(proficiency);