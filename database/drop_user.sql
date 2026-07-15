-- Purpose:
-- Remove the dedicated MySQL application user before database reinitialization.
-- Database concepts are based on Chapters 23 and 24 of the assigned textbook.
DROP USER IF EXISTS 'language_learning_app'@'localhost';