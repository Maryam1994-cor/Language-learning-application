-- Purpose:
-- Create the relational tables used by the Language Learning application.
-- The design follows the relational-database concepts from Chapters 23 and 24:
-- primary keys, foreign keys, entity integrity, referential integrity,
-- required columns, uniqueness, and a junction table for a many-to-many
-- relationship.

USE language_learning_db;

CREATE TABLE IF NOT EXISTS students (
    student_id INT UNSIGNED AUTO_INCREMENT,
    student_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL,

    CONSTRAINT pk_students
        PRIMARY KEY (student_id),

    CONSTRAINT uq_students_email
        UNIQUE (email)
) ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS languages (
    language_id INT UNSIGNED AUTO_INCREMENT,
    language_name VARCHAR(100) NOT NULL,

    CONSTRAINT pk_languages
        PRIMARY KEY (language_id),

    CONSTRAINT uq_languages_language_name
        UNIQUE (language_name)
) ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS student_language_xref (
    student_id INT UNSIGNED NOT NULL,
    language_id INT UNSIGNED NOT NULL,
    proficiency ENUM(
        'Beginner',
        'Intermediate',
        'Advanced'
    ) NOT NULL,

    CONSTRAINT pk_student_language_xref
        PRIMARY KEY (student_id, language_id),

    CONSTRAINT fk_student_language_student
        FOREIGN KEY (student_id)
        REFERENCES students (student_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    CONSTRAINT fk_student_language_language
        FOREIGN KEY (language_id)
        REFERENCES languages (language_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
) ENGINE = InnoDB;
