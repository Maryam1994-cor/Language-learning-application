-- Purpose:
-- Create a dedicated MySQL user for the Language Learning Application.
-- The application must use this account instead of the MySQL root account.
-- Database concepts are based on Chapters 23 and 24 of the assigned textbook.
CREATE USER IF NOT EXISTS 'language_learning_app' @'localhost' IDENTIFIED BY 'ChangeThisPassword123!';
GRANT SELECT,
    INSERT,
    UPDATE,
    DELETE ON language_learning_db.* TO 'language_learning_app' @'localhost';
FLUSH PRIVILEGES;